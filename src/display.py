#!/usr/bin/env python
# -*- coding: utf-8 -*-

# MIT License
# by Lucas Placentino
# Eufy Cam Controller - RaspberryPi

import os
import sys
import logging
import threading #?
from lib.TP_lib import gt1151, epd2in13_V2 #? or just like this ? use V3 ?
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
from PIL import Image,ImageDraw,ImageFont

logging.basicConfig(level=logging.DEBUG)

font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)

PagePath = ["Home.bmp", "Settings.bmp"]

i = j = k = ReFlag = SelfFlag = Page = Photo_L = Photo_S = 0 #?

class EPaperDisplay():
    def __init__(self, width: int, height: int, landscape: bool = True, touch: bool = True):
        logging.debug(f"EPaperDisplay.__init__()")

        if landscape:
            self.width = height
            self.height = width
        else:
            self.width = width
            self.height = height

        self.epd = epd2in13_V2.EPD() #? or V3?

        if touch:
            self.gt = gt1151.GT1151()
            self.GT_Dev = gt1151.GT_Development() #?
            self.GT_Old = gt1151.GT_Development() #?
            self.gt.GT_Init()

        self.epd.init(self.epd.FULL_UPDATE)
        self.epd.Clear(0xFF)

        self.flag_t = 1
        self.t = threading.Thread(target = self.touch_thread_irq)
        self.t.setDaemon(True)
        self.t.start()

        self.page = PagePath[0]

        #self.image_buffer = Image.new('1', (self.width, self.height), 255)
        self.image_buffer = Image.open(os.path.join(picdir, self.page)) #? or blank
        self.epd.displayPartBaseImage(self.epd.getbuffer(self.image_buffer))
        self.DrawImage = ImageDraw.Draw(self.image_buffer)
        self.epd.init(self.epd.PART_UPDATE)
    
    def touch_thread_irq(self):
        print(f"pthread running") #? logging.debug() ?
        while self.flag_t == 1 :
            if(self.gt.digital_read(self.gt.INT) == 0) :
                self.GT_Dev.Touch = 1
            else :
                self.GT_Dev.Touch = 0
        print(f"thread:exit") #? logging.debug() ?

    def draw(self):
        #TODO:
        pass

    def partial_draw(self):
        #TODO:
        pass

    def draw_image(self, File: str, x: int, y: int):
        "TODO:"
        newimage = Image.open(os.path.join(picdir, File))
        self.image_buffer.paste(newimage, (x, y))

    def refresh(self):
        #TODO:
        pass

    def clear_display(self):
        #TODO:
        pass

    def handle_touch(self) -> dict:
        if (self.page == PagePath[0]): # Home
            if (1==1):
                # touch toggle all cameras
                logging.debug(f"Home: touched toggle all cameras")
                return {"toggle" : "all"}
            #TODO: check coordiantes
            #TODO: ? programmatically get coords based on number of cameras : for i in range(sizeof(cemeras)): if(...): {"toggle": i}
            elif(self.GT_Dev.X[0] > 29 and self.GT_Dev.X[0] < 92 and self.GT_Dev.Y[0] > 56 and self.GT_Dev.Y[0] < 95):
                # touch camera 1
                logging.debug(f"Home: touched camera " + device.name + f" id " + device.id) #TODO:
                return {"toggle": device.id}
            elif (1==1):
                # touch camera 2
                return {}
            elif (1==1):
                # touched settings button
                logging.debug(f"Home: touched settings button")
                return {"go_to_page": 1}
            else:
                return {}
        elif (self.page == PagePath[1]): # Settings
            if (1==1):
                # touch home button
                logging.debug(f"Home: touched home button")
                return {"go_to_page": 0} # Home
            elif (1==1):
                # touch exit button
                return {"exit": True}
            else:
                return {}
        else:
            return {}

