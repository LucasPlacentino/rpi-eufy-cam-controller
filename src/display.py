#!/usr/bin/env python
# -*- coding: utf-8 -*-

# MIT License
# by Lucas Placentino
# Eufy Cam Controller - RaspberryPi

import logging
from lib.TP_lib import gt1151, epd2in13_V2 #? or just like this ? use V3 ?

logging.basicConfig(level=logging.DEBUG)

class EPaperDisplay():
    def __init__(self, width, height, landscape: bool = True, touch: bool = True):
        logging.debug("EPaperDisplay.__init__()")
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

    def display(self, image):
        pass

    def clear_display(self):
        pass


