#!/usr/bin/env python3

import argparse
from typing import Dict, Optional
from uuid import uuid4
from .logging import logger
from .keys import PrivateKeyFactory
from .configuration import config


def run(kid: str, params: Optional[Dict[str, str]]) -> None:
    filepath = f"{kid}.pem"
    with (
        open(filepath, "wb") as fd,
        PrivateKeyFactory({"kid": kid, **params}) as private_key_bytes,
    ):
        fd.write(private_key_bytes)
        logger.info(
            f"key_generator_file",
            extra={
                "filepath": filepath,
            },
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="conmotion_key_generator")
    parser.add_argument(
        "--private-key-instance-id",
        help="ID of individual key, if not default to UUID4",
        default=str(uuid4()),
    )
    parser.add_argument(
        "--private-key-creation-params",
        help="Parameters to generate key, else defaults from configuration file",
        default={}
    )
    parser.add_argument(
        "--private-key-deployment-context",
        help="Context type for this key, 'ts' or 'issuer', defaults to 'ts'",
        default="ts",
    )
    args = parser.parse_args()
    run(
        f"urn:scitt:{args.private_key_deployment_context}:key:{args.private_key_instance_id}",
        args.private_key_creation_params,
    )
