#!/usr/bin/env python3

from dotenv import dotenv_values

config = {**dotenv_values(".env")}
