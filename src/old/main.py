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

def main() -> None:

    # TODO:
    #docker.from_env().containers.get("eufy_cam_controller").start() #?
    container = docker_client.containers.run(image="bropat/eufy_security_ws", detach=True, name="eufy_cam_controller", network="host", volumes={"eufy_cam_controller_data": {"bind": "/data", "mode": "rw"}})
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

async def ws_test():
    uri: str = "ws://localhost:3000"
    async with ws_client.connect(uri) as websocket:
        await websocket.send("Hello world!")

        await sleep(1) # it is the asyncio.sleep()

        logging.debug(await websocket.recv())

def return_test():
    return json.dumps({"test": "test"})

if __name__ == "__main__":
    exit = 0
    try:
        logging.info(f"Starting...")
        main()
        global display
        display = EPaperDisplay(250, 122, landscape=True, touch=True)
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
        docker.from_env().containers.get("eufy_cam_controller").stop()
        docker.from_env().containers.get("eufy_cam_controller").remove()
        
        logging.info(f"Exiting...")
        sys.exit(exit)

# EOF