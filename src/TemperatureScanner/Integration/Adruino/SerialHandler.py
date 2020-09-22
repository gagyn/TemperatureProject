from typing import List
from serial import Serial
from time import sleep

class SerialHandler:
    _serial = None
    def __init__(self, arduinoPort: str):
        if SerialHandler._serial is None:
            SerialHandler._serial = Serial(arduinoPort, baudrate=250000, write_timeout=0.5, timeout=0.5)
            sleep(2)

    def write(self, stringToWrite):
        SerialHandler._serial.write(str(stringToWrite).encode())

    def read(self) -> List[str]:
        lines = SerialHandler._serial.readlines()
        return [x.decode() for x in lines]