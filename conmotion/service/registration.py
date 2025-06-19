#!/usr/bin/env python3

from cbor2 import dumps
from os import PathLike
from typing import IO, List, Optional, Union
from ..utils.certs import PublicCertificate
from ..utils.configuration import config
from ..utils.keys import PrivateKey
from ..utils.logging import logger


class RegistrationPolicyService:
    def __init__(
        self,
        trust_anchors: Optional[List] = [],
        issuer_ids: Optional[List] = [],
        statement_subjects: Optional[List] = [],
        private_key_path: Union[str|PathLike]=config.get("service_key_path"),
        public_cert_path: Union[str|PathLike]=config.get("service_cert_path")
    ):
        self.is_ready = False
        logger.debug(f"key path {private_key_path}")
        with (
           open(private_key_path, "rb") as key_fd,
           open(public_cert_path, "rb") as cert_fd
        ):
           self.private_key = PrivateKey.from_pem(key_fd.read())
           self.public_cert = PublicCertificate.from_pem(cert_fd.read())
        self.trust_anchors = trust_anchors
        self.issuer_ids = issuer_ids
        self.statement_subjects = statement_subjects
        logger.debug("registration_policy", extra=self.__dict__)
        self.is_ready = True

    @property
    def is_ready(self) -> bool:
        return self._is_ready

    @is_ready.setter
    def is_ready(self, value: bool) -> None:
        if value:
          logger.debug("registration service is ready now")
        else:
          logger.debug("registration service is not ready now")
        self._is_ready = value
  
    def as_cbor(self) -> IO[bytes]:
        """
        Serialize the current Registration Policy maintained by the service as a
        CBOR byte sequence.
        """
        return dumps(["Success!"])
