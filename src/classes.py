#!/usr/bin/env python
# -*- coding: utf-8 -*-

# MIT License
# by Lucas Placentino
# Eufy Cam Controller - RaspberryPi

import json
import logging

class Device():
    def __init__(self, id: int, name: str, ip_addr: str, sn: str):
        self.id: int = id
        self.name: str = name
        self.ip_addr: str = ip_addr
        self.sn: str = sn

class Camera(Device):
    def __init__(self):
        pass

class Station(Device):
    def __init__(self):
        pass

class Controller():
    def __init__(self, devices: list[Device]):
        self.devices = devices
