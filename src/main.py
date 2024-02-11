#!/usr/bin/env python
# -*- coding: utf-8 -*-

# MIT License
# by Lucas Placentino
# Eufy Cam Controller - RaspberryPi

#import json
import logging
from enum import Enum
import eufy_client

logging.basicConfig(level=logging.DEBUG)


def main():
    pass


if __name__ == "__main__":
    try:
        logging.info("Starting...")
        main()
    except Exception as e:
        logging.error(e)
    finally:
        logging.info("Exiting...")
