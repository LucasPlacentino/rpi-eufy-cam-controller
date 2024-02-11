# MIT License
# by Lucas Placentino
# Eufy Cam Controller - RaspberryPi

import signal, sys, time, logging
import RPi.GPIO as GPIO
from old.main import update_state, dbg

class Camera():
    def __init__(*, self, id, name="Camera", btn_gpio, ip_addr):
        self.id: int = id
        self.name: str = name
        self.btn: Button = Button(btn_gpio, self)
        self.ip_addr: str = ip_addr
        self.device_id: int = device_id
        self.device_sn: str = device_sn
        self.device_name: str = device_name
        self.device_type: int = device_type
        self.device_channel: int = device_channel
        self.station_sn: str = station_sn
        self.status: bool = False

    def get_id(self) -> int:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_ip(self) -> str:
        return self.ip_addr

    def get_status(self) -> bool:
        return self.status


class Controller():
    def __init__(self, cameras):
        self.cameras: list[Camera] = cameras
        self.last_update: str= ""

    def get_cameras(self) -> list[Camera]:
        return self.cameras
    
    def get_camera(self, name) -> Camera:
        for camera in self.cameras:
            if camera.get_name() == name:
                return camera
            
    def get_camera_status(self, name) -> bool:
        return self.get_camera(name).get_status()
    
    def get_camera_ip(self, name) -> str:
        return self.get_camera(name).get_ip()

class Button():
    def __init__(self, gpio: int, camera: Camera):
        self.gpio: int = gpio
        #self.pressed: bool = False
        self.camera: Camera = camera
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.gpio, GPIO.FALLING, callback=self.callback, bouncetime=300)
        signal.signal(signal.SIGINT, self.signal_handler) #? needed?
        #signal.pause() # waits for a btn interrupt

    def callback(self, channel) -> None:
        #self.pressed = True
        logging.info("Button "+self.camera.get_name+" pressed")
        update_state(self.camera)
        dbg("end of btn callback")

    def signal_handler(self, signal, frame) -> None:
        logging.info("CTRL+C, exiting...")
        GPIO.cleanup()
        sys.exit(0)
