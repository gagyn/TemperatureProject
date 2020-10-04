from typing import List
from serial import Serial
from time import sleep
from os import path

class SerialHandler:
    _serial: Serial = None

    def __init__(self, arduinoPort: str):
        self.arduinoPort = arduinoPort
        if SerialHandler._serial is None:
            self._init_serial()

    def write(self, stringToWrite):
        try:
            SerialHandler._serial.write(str(stringToWrite).encode())
        except:
            print('Arduino not available')
            sleep(2)
            self._init_serial()

    def read(self) -> List[str]:
        try:
            lines = SerialHandler._serial.readlines()
            return [x.decode() for x in lines]
        except:
            print('Arduino not available')
            sleep(2)
            self._init_serial()
    
    def _init_serial(self):
        if path.exists(self.arduinoPort):
            SerialHandler._serial = Serial(self.arduinoPort, baudrate=250000, write_timeout=0.5, timeout=0.8)
            sleep(3)
        