"""
An Reranker Only Model Worker. Using embedding api interface.
"""

import argparse
import base64
import json
import os
from typing import List, Optional
import uuid

import numpy
import torch
from FlagEmbedding import FlagReranker
import uvicorn

from fastchat.constants import ErrorCode, SERVER_ERROR_MSG
from fastchat.serve.base_model_worker import BaseModelWorker, app
from fastchat.utils import build_logger

worker_id = str(uuid.uuid4())[:8]
logger = build_logger("model_worker", f"model_worker_{worker_id}.log")


class FlagRerankerWorker(BaseModelWorker):
    def __init__(
        self,
        controller_addr: str,
        worker_addr: str,
        worker_id: str,
        model_path: str,
        model_names: List[str],
        limit_worker_concurrency: int,
        no_register: bool,
        batch_size: int = 256,
        max_length: int = 32 * 1024,
        debug: bool = False,
        **kwargs,
    ):
        self.model_path = model_path
        self.debug = debug
        self.batch_size = batch_size
        self.max_length = max_length

        super().__init__(
            controller_addr=controller_addr,
            worker_addr=worker_addr,
            worker_id=worker_id,
            model_path=model_path,
            model_names=model_names,
            limit_worker_concurrency=limit_worker_concurrency,
        )

        logger.info(
            f"Loading the FlagReranker {self.model_names} on worker {worker_id} ..."
        )

        self.context_len = 32 * 1024
        self.model = FlagReranker(
            self.model_path,
            **kwargs,
        )

        if not no_register:
            self.init_heart_beat()

    def count_token(self, params):
        ret = {
            "count": 0,
            "error_code": 0,
        }
        return ret

    def generate_stream_gate(self, params):
        ret = {
            "text": "Text-generation is NOT supported by Reranker Only Model.",
            "error_code": ErrorCode.INVALID_MODEL,
        }
        yield json.dumps(ret).encode() + b"\0"

    def generate_gate(self, params):
        for x in self.generate_stream_gate(params):
            pass
        return json.loads(x[:-1].decode())

    def __encode_base64(self, embeddings):
        return [
            base64.b64encode(
                numpy.array(
                    embeddings,
                    dtype=numpy.float32,
                ).tobytes()
            ).decode("utf-8")
        ]

    @torch.inference_mode()
    def get_embeddings(self, params):
        self.call_ct += 1
        try:
            if self.debug:
                logger.info("Calling get_embeddings with params=%s", params)
            inputs = params["input"]
            ret = {
                "embedding": [],
                "token_num": sum([len(x) for x in inputs]),
            }
            messages = []
            for i in range(0, len(inputs), 2):
                messages.append((inputs[i], inputs[i + 1]))
            normalized_embeddings = self.model.compute_score(
                messages,
                batch_size=self.batch_size,
                max_length=self.max_length,
                normalize=False,
            )
            if isinstance(normalized_embeddings, float):
                normalized_embeddings = [normalized_embeddings]
            if self.debug:
                logger.info(
                    "FlagReranker compute_score returns: %s",
                    normalized_embeddings,
                )
            base64_encode = params.get("encoding_format", None)
            if base64_encode == "base64":
                out_embeddings = self.__encode_base64(normalized_embeddings)
            else:
                out_embeddings = normalized_embeddings
            ret["embedding"] = out_embeddings
        except torch.cuda.OutOfMemoryError as e:
            ret = {
                "text": f"{SERVER_ERROR_MSG}\n\n({e})",
                "error_code": ErrorCode.CUDA_OUT_OF_MEMORY,
            }
        except (ValueError, RuntimeError) as e:
            ret = {
                "text": f"{SERVER_ERROR_MSG}\n\n({e})",
                "error_code": ErrorCode.INTERNAL_ERROR,
            }
        return ret


def create_model_worker():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--host",
        type=str,
        default="localhost",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=22003,
    )
    parser.add_argument(
        "--worker-address",
        type=str,
        default="http://localhost:22003",
    )
    parser.add_argument(
        "--controller-address",
        type=str,
        default="http://localhost:21001",
    )
    parser.add_argument(
        "--model-path",
        type=str,
        default="BAAI/bge-large-zh-v1.5",
        help="The path to the weights. This can be a local folder or a Hugging Face repo ID.",
    )
    parser.add_argument(
        "--model-names",
        type=lambda s: s.split(","),
        help="Optional display comma separated names.",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=256,
        help="FlagModel encode batch size.",
    )
    parser.add_argument(
        "--max-length",
        type=int,
        default=32 * 1024,
        help="FlagModel encode max length.",
    )
    parser.add_argument(
        "--limit-worker-concurrency",
        type=int,
        default=50,
        help="Limit the model concurrency to prevent OOM.",
    )
    parser.add_argument(
        "--no-register",
        action="store_true",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="Print debugging messages",
    )
    parser.add_argument(
        "--ssl",
        action="store_true",
        required=False,
        default=False,
        help="Enable SSL. Requires OS Environment variables 'SSL_KEYFILE' and 'SSL_CERTFILE'.",
    )
    args = parser.parse_args()

    logger.info(f"args: {args}")

    worker = FlagRerankerWorker(
        controller_addr=args.controller_address,
        worker_addr=args.worker_address,
        worker_id=worker_id,
        model_path=args.model_path,
        model_names=args.model_names or [args.model_path.split("/")[-1]],
        limit_worker_concurrency=args.limit_worker_concurrency,
        no_register=args.no_register,
        batch_size=args.batch_size,
        max_length=args.max_length,
        debug=args.debug,
    )
    return args, worker


if __name__ == "__main__":
    args, worker = create_model_worker()
    if args.ssl:
        uvicorn.run(
            app,
            host=args.host,
            port=args.port,
            log_level="info",
            ssl_keyfile=os.environ["SSL_KEYFILE"],
            ssl_certfile=os.environ["SSL_CERTFILE"],
        )
    else:
        uvicorn.run(app, host=args.host, port=args.port, log_level="info")
