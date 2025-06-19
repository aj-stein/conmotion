#!/usr/bin/env python3

from cryptography.hazmat.primitives.asymmetric import ec, utils
from cryptography.hazmat.bindings._rust import openssl as rust_openssl
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography import x509
from cryptography.hazmat.primitives import hashes
import datetime
from typing import Dict, IO
from .configuration import config
from .keys import PrivateKey
from .logging import logger

ECPrivateKey = rust_openssl.ec.ECPrivateKey

class CertificateFactory:
  def __init__(self, private_key: IO[bytes], params: Dict[str, str]):
    self.engine = x509
    self.private_key = PrivateKey.from_pem(private_key)
    self.params = params
    self.cert = None

  def __enter__(self) -> IO[bytes]:
      self.create_cert()
      return self.export_cert()

  def __exit__(self, exc_type, exc_val, exc_tb) -> None:
      self.key = None
      if exc_type:
          logger.exception(exc_val)
  
  def create_cert(self) -> x509.CertificateBuilder:
      subject_name = x509.Name(
        [x509.NameAttribute(x509.NameOID.COMMON_NAME, self.params.get('subject_name'))]
      )
      issuer_name = x509.Name(
        [x509.NameAttribute(x509.NameOID.COMMON_NAME, self.params.get('issuer_name'))]
      )
      if not(self.params.get('days_valid')): self.params['days_valid'] = config.get('public_cert_days_valid')
      if not(self.params.get('serial_number')): self.params['serial_number'] = x509.random_serial_number()
      days_valid, serial_number = self.params.get('days_valid'), self.params.get('serial_number')
      try:
        logger.debug("create_cert", extra={"engine": self.engine.__name__, **self.params})
        self.cert = (self.engine.CertificateBuilder()
          .subject_name(subject_name)
          .issuer_name(issuer_name)
          .public_key(self.private_key.public_key())
          .serial_number(serial_number)
          .not_valid_before(datetime.datetime.now(datetime.UTC))
          .not_valid_after(datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=days_valid))
          .sign(self.private_key, hashes.SHA256())
        )
        return self.cert
      except Exception as e:
         logger.exception(e)

  def export_cert(self) -> IO[bytes]:
    try:
      logger.debug("export_cert", extra={"engine": self.engine.__name__, **self.params})
      if not self.cert:
          raise RuntimeError("cert not generated before export")
      return self.cert.public_bytes(Encoding.PEM)
    except Exception as e:
      logger.exception(e)
  