#!/usr/bin/env python
# -*- coding: utf-8 -*-

# MIT License
# by Lucas Placentino
# Eufy Cam Controller - RaspberryPi

import sys
import os
import threading #? or asyncio?
import asyncio #? or threading?
from asyncio import sleep
import time #?
import docker
import json
import logging
import websockets.client as ws_client

from display import EPaperDisplay, PagePath
from models import Device, Camera, Station, Controller
from ws_eufy_api import WSEufyApi, Message

from lib.TP_lib import gt1151, epd2in13_V2 #? or just like this ? use V3 ?

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
"""
from TP_lib import gt1151
from TP_lib import epd2in13_V2 #? V3 ?
"""
# ?-----

from PIL import Image,ImageDraw,ImageFont

logging.basicConfig(level=logging.DEBUG)

#display = EPaperDisplay(250, 122, landscape=True, touch=True)
docker_client = docker.from_env()
WS_EUFY_API = WSEufyApi()

def main() -> None:

    #FIXME:
    number_of_cameras: int = int(os.getenv("NUMBER_OF_CAMERAS", 1))
    STATION_IP_ADRESSES: str = str(os.getenv("CAM_1_SN"))+":"+str(os.getenv("CAM_1_IP"))+";"+str(os.getenv("CAM_2_SN"))+":"+str(os.getenv("CAM_2_IP"))

    # TODO:
    #docker.from_env().containers.get("eufy_cam_controller").start() #?
    try:
        container = docker_client.containers.get("eufy_cam_controller")
        container.start()
    except docker.errors.NotFound:
        logging.debug("Container not found")
        container = docker_client.containers.run(
            environment=[
                "USERNAME={}".format(os.getenv("EUFY_EMAIL", "mail@example.org")),
                "PASSWORD={}".format(os.getenv("EUFY_PASSWORD", "password")),
                "POLLING_INTERVAL={}".format(os.getenv("POLLING_INTERVAL", "10")),
                "COUNTRY={}".format(os.getenv("COUNTRY_CODE", "DE")),
                "LANGUAGE={}".format(os.getenv("LANGUAGE_CODE", "en")),
                "ACCEPT_INVITATIONS={}".format(os.getenv("ACCEPT_INVITATIONS", "false")),
                "STATION_IP_ADRESSES={}".format(STATION_IP_ADRESSES),
                "PORT={}".format(os.getenv("CONTAINER_WS_PORT", "3000"))
                ],
            image="bropat/eufy_security_ws",
            detach=True, name="eufy_cam_controller",
            network="host",
            volumes={"eufy_cam_controller_data": {"bind": "/data", "mode": "rw"}})
    logging.debug(container.logs())

    #epd = epd2in13_V2.EPD()
    #gt = gt1151.GT1151()
    #GT_Dev = gt1151.GT_Development() #?
    #GT_Old = gt1151.GT_Development() #?

    #logging.info("init and Clear")
    #epd.init(epd.FULL_UPDATE)
    #gt.GT_Init()
    #epd.Clear(0xFF)

    asyncio.run(ws_test()) #?


    loop()

def loop() -> None:
    i = j = k = ReFlag = SelfFlag = 0 #?
    while(1):
        #logging.debug("loop()")
        
        #TODO: ?
        if(i > 12 or ReFlag == 1):
            if(display.page == PagePath[1] and SelfFlag == 0):
                display.epd.displayPartial(display.epd.getbuffer(display.image_buffer))
            else:
                display.epd.displayPartial_Wait(display.epd.getbuffer(display.image_buffer))
            i = 0
            k = 0
            j += 1
            ReFlag = 0
            print("*** Draw Refresh ***\r\n")
        elif(k>50000 and i>0 and display.page == PagePath[1]):
            display.epd.displayPartial(display.epd.getbuffer(display.image_buffer))
            i = 0
            k = 0
            j += 1
            print("*** Overtime Refresh ***\r\n")
        elif(j > 50 or SelfFlag):
            SelfFlag = 0
            j = 0
            display.epd.init(display.epd.FULL_UPDATE)
            display.epd.displayPartBaseImage(display.epd.getbuffer(display.image_buffer))
            display.epd.init(display.epd.PART_UPDATE)
            print("--- Self Refresh ---\r\n")
        else:
            k += 1

        display.gt.GT_Scan(display.GT_Dev, display.GT_Old)
        if(display.GT_Old.X[0] == display.GT_Dev.X[0] and display.GT_Old.Y[0] == display.GT_Dev.Y[0] and display.GT_Old.S[0] == display.GT_Dev.S[0]):
            continue
        
        if(display.GT_Dev.TouchpointFlag):
            #logging.debug("display touched")
            #i += 1
            display.GT_Dev.TouchpointFlag = 0
            touch_res = display.handle_touch()
            if "device" in touch_res:
                toggle_device(touch_res["device"])



def toggle_device(device_id: int) -> None:
    logging.debug(f"toggle_device({device_id})")
    #TODO: 


async def ws_test():
    uri: str = "ws://localhost:{}".format(os.getenv("CONTAINER_WS_PORT", "3000"))
    async with ws_client.connect(uri) as websocket:
        """
        should receive this after client connects:
        {
            type: "version";
            driverVersion: string;
            serverVersion: string;
            minSchemaVersion: number;
            maxSchemaVersion: number;
        }
        """
        data = await websocket.recv()
        logging.debug("Initial WS connect response from server: ",data)
        try:
            parsed_data = json.loads(data)
            if "type" in parsed_data and \
               "driverVersion" in parsed_data and \
               "serverVersion" in parsed_data and \
               "minSchemaVersion" in parsed_data and \
               "maxSchemaVersion" in parsed_data:
                message_type = parsed_data["type"]
                WS_EUFY_API.driver_version = parsed_data["driverVersion"]
                WS_EUFY_API.server_version = parsed_data["serverVersion"]
                WS_EUFY_API.min_schema_version = parsed_data["minSchemaVersion"]
                WS_EUFY_API.max_schema_version = parsed_data["maxSchemaVersion"]
            else:
                logging.error("Invalid response from server at initial connection.")
        except json.JSONDecodeError as e:
            logging.error(e)
            #TODO: handle error


        start_listening_command = {
            "messageId": "string",
            "command": "start_listening",
        }
        logging.debug("Sending start_listening command to WS server: ",start_listening_command)
        await websocket.send(json.dumps(start_listening_command))

        message = Message()
        data = await websocket.recv()
        """
        {
            type: "result";
            messageId: string; // maps the `start_listening` command
            success: true,
            result: {
                state: {
                    driver: {
                        version:
                        connected:
                        pushConnected:
                    }
                    stations: string[];
                    devices: string[];
                }
            };
        }
        """
        logging.debug("Initial WS start_listening response from server: ",data)
        try:
            parsed_data = json.loads(data)
            if "type" in parsed_data and \
               "messageId" in parsed_data and \
               "success" in parsed_data and \
               "result" in parsed_data:
                message.type = parsed_data["type"]
                message.id = parsed_data["messageId"]
                WS_EUFY_API.stations = parsed_data["result"]["state"]["stations"]
                WS_EUFY_API.devices = parsed_data["result"]["state"]["devices"]
            else:
                logging.error("Invalid response from server after start_listening message.")
        except json.JSONDecodeError as e:
            logging.error(e)
            #TODO: handle error


        

        await websocket.send("Hello world!")

        await sleep(1) # it is the asyncio.sleep()

        logging.debug(await websocket.recv())



def return_test():
    return json.dumps({"test": "test"})

if __name__ == "__main__":
    exit = 0
    try:
        logging.info(f"Starting...")
        global display
        display = EPaperDisplay(250, 122, landscape=True, touch=True)
        main()
    except KeyboardInterrupt:
        logging.info(f"KeyboardInterrupt")
        exit = 0
    except SystemExit:
        logging.info(f"SystemExit")
        exit = 0
    except Exception as e:
        logging.exception(e)
        exit = 1
    finally:
        display.flag_t = 0
        display.epd.sleep() # ! important?
        time.sleep(2) # or asyncio.sleep(2) ?
        display.epd.Dev_exit()
        
        #TODO: ?
        container = docker_client.containers.get("eufy_cam_controller")
        container.stop()
        cs = container.wait()
        logging.debug(cs)
        ##container.remove()
        
        logging.info(f"Exiting...")
        sys.exit(exit)

# EOF