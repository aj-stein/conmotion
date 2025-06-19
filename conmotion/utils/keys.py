#!/usr/bin/env python3

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.bindings._rust import openssl as rust_openssl
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    load_pem_private_key,
    NoEncryption,
    PrivateFormat,
)
from typing import Dict, IO
from .configuration import config
from .logging import logger

ECPrivateKey = rust_openssl.ec.ECPrivateKey

class PrivateKeyFactory:
    def __init__(self, params: Dict[str, str]) -> None:
        self.engine = ec
        if not (params.get("crv")):
          curve = config.get('private_key_curve')
          logger.warning(f"key generation did not override curve, using default", extra={
            "curve": curve
          })
        self.curve = getattr(self.engine, curve)
        self.key = None
        self.params = params

    def __enter__(self) -> IO[bytes]:
        self.create_key()
        return self.export_key()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.key = None
        if exc_type:
            logger.exception(exc_val)

    def create_key(self) -> ECPrivateKey:
        try:
            logger.debug(
                f"create_key_args",
                extra={"engine": self.engine.__name__, **self.params},
            )
            self.key = self.engine.generate_private_key(self.curve())
            return self.key
        except Exception as e:
            logger.exception(e)

    def export_key(self) -> IO[bytes]:
        try:
            logger.debug(
                "export_key_args", extra={"engine": self.engine.__name__, **self.params}
            )
            if not self.key:
                raise RuntimeError("key not generated before export")
            return self.key.private_bytes(
                Encoding.PEM, PrivateFormat.PKCS8, NoEncryption()
            )
        except Exception as e:
            logger.exception(e)

class PrivateKey:
    @staticmethod
    def from_pem(private_key: IO[bytes], password: IO[bytes]=None):
        return load_pem_private_key(private_key, password)