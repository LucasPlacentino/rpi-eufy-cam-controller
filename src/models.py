#!/usr/bin/env python
# -*- coding: utf-8 -*-

# MIT License
# by Lucas Placentino
# Eufy Cam Controller - RaspberryPi

#import json
import logging
from enum import Enum

logging.basicConfig(level=logging.DEBUG)

class DeviceState(Enum):
    ON = 1
    OFF = 0

class Device():
    def __init__(self, id: int, name: str, ip_addr: str, sn: str):
        self.id: int = id
        self.name: str = name
        self.ip_addr: str = ip_addr
        self.sn: str = sn

class Camera(Device):
    def __init__(self):
        self.state = DeviceState.OFF

class Station(Device):
    def __init__(self):
        self.state = DeviceState.OFF

class Controller():
    def __init__(self, devices: list[Device]):
        self.devices = devices
