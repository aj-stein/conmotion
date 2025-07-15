#!/usr/bin/env python3

from flask import Flask, redirect
from werkzeug.wrappers import Response
from ..utils.logging import logger
from .registration import RegistrationPolicyService

app = Flask("conmotion_transparency_service")
app.debug = True

registration_service = RegistrationPolicyService()

@app.route("/")
def index() -> Response:
    """
    When a Relying Party or any HTTP client visits the service without a valid
    endpoint per the specification, redirect to the documentation.
    """
    return redirect("https://conmotion.netlify.app/architecture.html", code=302)


@app.route("/.well-known/transparency-configuration")
def get_registration_policy() -> Response:
    logger.debug("request for registration policy")
    return Response(regstration_service.as_cbor(), mimetype="application/cbor")


if __name__ == "__main__":
    try:
        logger.info("service starting up")
        app.run()
    finally:
        logger.info("service service shutting down")
