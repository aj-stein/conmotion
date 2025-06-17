#!/usr/bin/env python3

from cbor2 import dumps
from typing import IO, List, Optional
from ..utils.logging import logger


class RegistrationPolicyService:
    def __init__(
        self,
        trust_anchors: Optional[List] = [],
        issuer_ids: Optional[List] = [],
        statement_subjects: Optional[List] = [],
    ):
        self.trust_anchors = trust_anchors
        self.issuer_ids = issuer_ids
        self.statement_subjects = statement_subjects
        logger.debug("policy", extra=self.__dict__)

    def as_cbor(self) -> IO[bytes]:
        """
        Serialize the current Registration Policy maintained by the service as a
        CBOR byte sequence.
        """
        return dumps(["Success!"])
