#!/usr/bin/env python
# -*- coding: utf-8 -*-

# MIT License
# by Lucas Placentino
# Eufy Cam Controller - RaspberryPi

#import json
import logging
from enum import Enum

from aiohttp import ClientSession
from datetime import datetime
from Crypto.PublicKey import ECC
from apscheduler.schedulers.background import BackgroundScheduler

from .interfaces import HTTPApiEvents, FullDevices, Hubs, Houses, HTTPApiPersistentData
from utils import getTimezoneGMTString

logging.basicConfig(level=logging.DEBUG)

class HTTPApi(HTTPApiEvents):

    _apiDomainBase = "https://mysecurity.eufylife.com"

    _SERVER_PUBLIC_KEY = "04c5c00c4f8d1197cc7c3167c52bf7acb054d722f0ef08dcd7e0883236e0d72a3868d9750cb47fa4619248f3d83f0f662671dadc6e2d31c2f41db0161651c7c076"

    _apiBase = ""
    _username = ""
    _password = ""
    _ecdh: ECDH = ECC.generate(curve='prime256v1')

    token: str|None = None
    tokenExpiration: datetime|None = None
    renewAuthTokenJob: BackgroundScheduler.Job | None # ?

    _log = logging.getLogger(__name__)
    _connected = False
    _requestEufyCloud = ClientSession()

    # pThrottle

    _devices: FullDevices = {}
    _hubs: Hubs = {}
    _houses: Houses = {}

    _persistentData: HTTPApiPersistentData = {
        "user_id": "",
        "email": "",
        "nick_name": "",
        "device_public_keys": {},
        "clientPrivateKey": "",
        "serverPublicKey": _SERVER_PUBLIC_KEY
    }

    _headers: dict[str, str] = {
        "App_version": "v4.6.0_1630",
        "Os_type": "android",
        "Os_version": "31",
        "Phone_model": "ONEPLUS A3003",
        "Country": "DE",
        "Language": "en",
        "Openudid": "5e4621b0152c0d00",
        #"uid": "",
        "Net_type": "wifi",
        "Mnc": "02",
        "Mcc": "262",
        "Sn": "75814221ee75",
        "Model_type": "PHONE",
        "Timezone": "GMT+01:00",
        "Cache-Control": "no-cache",
    }

    def __init__(self, apiBase: str, country: str, username: str, password: str, log: logging.Logger, persistentData: HTTPApiPersistentData|None):
        super()

        self._apiBase = apiBase
        self._username = username
        self._password = password
        self._log = log

        self._log.debug("Loaded API", { "apiBase": apiBase, "country": country, "username": username, "persistentData": persistentData });
        
        self._headers["timezone"] = getTimezoneGMTString()
        self._headers["Country"] = country.capitalize()

        if (persistentData):
            self._persistentData = persistentData
        if (self._persistentData["clientPrivateKey"] == "" or self._persistentData["clientPrivateKey"] == None):
            self._ecdh.generate_key()
            self._persistentData["clientPrivateKey"] = self._ecdh.getPrivateKey().hex()
        else:
            try:
                self._ecdh = #...


