# MIT License
# by Lucas Placentino
# Eufy Cam Controller - RaspberryPi

import time
import RPi.GPIO as GPIO
from board import SCL, SDA
import busio
from oled_text import OledText, Layout32
from classes import Controller, Camera, Button

cameras = [
    Camera(name="Living room", id=0, ip_addr="192.168.0.146"),
    Camera(name="Entry hall", id=1, ip_addr="192.168.0.147"),
    Camera(name="Kitchen", id=2, ip_addr="192.168.0.148"),
]
BTN_GPIO = 16
I2C_ADDRESS = 0x3C
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 32

i2c = busio.I2C(SCL, SDA)
oled = OledText(i2c, SCREEN_WIDTH, SCREEN_HEIGHT)
oled.layout = Layout32.layout_3small()
#oled.auto_show = False # is set to False, requires oled.show() to update screen

def loop(controller: Controller) -> None:
    print("Starting loop...")
    while True:
        pass
        # wait for button press interrupt
    #    controller.update()
    #    controller.print_status()
    #    controller.check_status()

def api_call_get_all_statuses(cameras :list[cameras]) -> dict[str, bool]:
    #TODO: implement
    pass

def display_cameras(cameras: list[Camera]) -> None:
    i=1
    oled.clear()
    for camera in cameras:
        print(camera.get_name()+" - IP: "+camera.get_ip()+" - Status: "+camera.get_status())
        if i <= 3:
            oled.text("\uf03d "+camera.get_name()+" ON" if camera.get_status() else " OFF", i)
        i+=1


def start() -> None:
    print("Starting...")
    oled.clear()
    oled.text("Starting...", 1)
    controller = Controller(cameras)
    print("Controller created.")
    print("Cameras:")
    oled.clear()
    display_cameras(controller.get_cameras())

    time.sleep(2)

    current_statuses = api_call_get_all_statuses(controller.get_cameras())
    i=1
    for camera in controller.get_cameras():
        camera.status = current_statuses[camera.get_name()] # TODO: set correct status to each camera
    display_cameras(controller.get_cameras())
    btn = Button(BTN_GPIO)

    loop(controller)


def update_state(camera: Camera) -> bool:
    pass


if __name__ == "__main__":
    start()
