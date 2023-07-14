# MIT License
# by Lucas Placentino
# Eufy Cam Controller - RaspberryPi

import sys
import time
import logging
import RPi.GPIO as GPIO
from board import SCL, SDA
import busio
from oled_text import OledText, Layout32  # pip install oled-text
#import luma # maybe?
from classes import Controller, Camera, Button

DEBUG: bool = True
BTN1_GPIO: int = 16
BTN2_GPIO: int = 17
BTN3_GPIO: int = 18
I2C_ADDRESS: int = 0x3C  # or 0x3D (hex address)
SCREEN_WIDTH: int = 128
SCREEN_HEIGHT: int = 32  # or 64
cameras: list[Camera] = [
    Camera(
        name="Living room",
        id=0,
        btn_gpio=BTN1_GPIO,
        ip_addr="192.168.0.146"
    ),
    Camera(
        name="Entry hall",
        id=1,
        btn_gpio=BTN2_GPIO,
        ip_addr="192.168.0.147"
    ),
    Camera(
        name="Kitchen",
        id=2,
        btn_gpio=BTN3_GPIO,
        ip_addr="192.168.0.148"
    ),
]

# ----------------------------------------

i2c = busio.I2C(SCL, SDA)
oled = OledText(i2c, SCREEN_WIDTH, SCREEN_HEIGHT)
oled.layout = Layout32.layout_3small()
# oled.auto_show = False # is set to False, requires oled.show() to update screen

controller: Controller = Controller(cameras)


def loop() -> None:
    logging.debug("Starting loop...")
    while True:
        pass
        # wait for button press interrupt
    #    controller.update()
    #    controller.print_status()
    #    controller.check_status()


def api_call_get_all_statuses(cameras: list[cameras]) -> dict[str, bool]:
    # TODO: implement
    pass


def display_cameras(cameras: list[Camera]) -> None:
    i = 1
    oled.clear()
    for camera in cameras:
        logging.info(camera.get_name()+" - IP: "+camera.get_ip() +
                     " - Status: "+str(camera.get_status()))
        if i <= 3:
            # oled.text("\uf03d "+camera.get_name()+" ON" if camera.get_status() else " OFF", i)
            oled.text(camera.get_name() +
                      " ON" if camera.get_status() else " OFF", i)
        i += 1


def api_call_change_camera_status(camera: Camera) -> bool:
    res = False
    logging.info("API call: Changing status of "+camera.get_name() +
                 " (id: "+str(camera.get_id())+") to " + str(not camera.get_status()))
    # TODO: implement
    return res


def start() -> None:
    logging.info("Starting...")
    oled.clear()
    oled.text("Starting...", 1)
    logging.info("Cameras:")
    oled.clear()
    display_cameras(controller.get_cameras())

    time.sleep(2)

    current_statuses = api_call_get_all_statuses(controller.get_cameras())
    i = 1
    for camera in controller.get_cameras():
        # TODO: set correct status to each camera
        camera.status = current_statuses[camera.get_name()]
    display_cameras(controller.get_cameras())

    logging.debug("End of start()")
    loop()


def update_state(camera: Camera) -> bool:
    if api_call_change_camera_status(camera):
        camera.status = not camera.status
        display_cameras(controller.get_cameras())
        return True
    else:
        logging.error("Error: could not update status of "+camera.get_name())
        return False


if __name__ == "__main__":
    logging.basicConfig(
        stream=sys.stderr,
        level=logging.DEBUG if DEBUG else logging.INFO,
        format='%(asctime)s-%(name)s: %(levelname)s - %(message)s',
        datefmt='% Y-%m-%d@%H: % M: % S'
    )
    try:
        start()
    except Exception as e:
        if e == KeyboardInterrupt:
            logging.error("KeyboardInterrupt: Exiting...", exc_info=False)
            oled.clear()
            oled.text("Exiting...", 1)
            time.sleep(2)
            sys.exit(0)
        elif e == SystemExit:
            logging.error("SystemExit: Exiting...", exc_info=False)
            oled.clear()
            oled.text("Exiting...", 1)
            time.sleep(2)
            sys.exit(0)
        else:
            logging.exception("Exception occurred")
            oled.clear()
            oled.text("Error: "+str(e), 1)
            time.sleep(2)
            sys.exit(1)
