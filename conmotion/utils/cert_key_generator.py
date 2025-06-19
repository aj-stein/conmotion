#!/usr/bin/env python3

import argparse
from typing import Dict, Optional
from uuid import uuid4
from .logging import logger
from .certs import CertificateFactory
from .keys import PrivateKeyFactory
from .configuration import config


def run(
    kid: str,
    private_key_params: Optional[Dict[str, str]],
    cid: str,
    public_cert_params: Optional[Dict[str, str]],
) -> None:
    private_key_filepath = f"{kid}.pem"
    public_cert_filepath = f"{cid}.pem"
    with (
        open(private_key_filepath, "wb") as key_fd,
        open(public_cert_filepath, "wb") as cert_fd,
        PrivateKeyFactory({"kid": kid, **private_key_params}) as private_key_bytes,
        CertificateFactory(private_key_bytes, public_cert_params) as public_cert_bytes,
    ):
        key_fd.write(private_key_bytes)
        logger.info(
            f"key_generator_file",
            extra={"filepath": private_key_filepath},
        )
        cert_fd.write(public_cert_bytes)
        logger.info(
            f"cert_generator_file",
            extra={"filepath": public_cert_filepath},
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="conmotion_cert_key_generator")
    instance_id = uuid4()
    parser.add_argument(
        "--private-key-instance-id",
        help="ID of individual key, if not default to UUID4",
        default=str(instance_id),
    )
    parser.add_argument(
        "--private-key-creation-params",
        help="Parameters to generate key, else defaults from configuration file",
        default={},
    )
    parser.add_argument(
        "--private-key-deployment-context",
        help="Context type for this key, 'ts' or 'issuer', defaults to 'ts'",
        default="ts",
    )
    parser.add_argument(
        "--public-cert-instance-id",
        help="ID of individual cert, if not default to UUID4",
        default=str(instance_id),
    )
    parser.add_argument(
        "--public-cert-deployment-context",
        help="Context type for this key, 'ts' or 'issuer', defaults to 'ts'",
        default="ts",
    )
    parser.add_argument(
        "--public-cert-creation-params",
        help="Parameters to generate cert, else defaults from configuration file",
        default={
            "issuer_name": "conmotion_ts_dev",
            "subject_name": "conmotion_ts_dev",
            "days_valid": 365,
        },
    )
    args = parser.parse_args()
    run(
        f"urn:scitt:{args.private_key_deployment_context}:key:{args.private_key_instance_id}",
        args.private_key_creation_params,
        f"urn:scitt:{args.public_cert_deployment_context}:cert:{args.public_cert_instance_id}",
        args.public_cert_creation_params,
    )
