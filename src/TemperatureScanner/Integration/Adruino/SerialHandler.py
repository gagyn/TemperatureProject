from typing import List
from serial import Serial
from time import sleep

class SerialHandler:
    __serial = None
    def __init__(self, arduinoPort: str):
        if SerialHandler.__serial is None:
            SerialHandler.__serial = Serial(arduinoPort, baudrate=250000, write_timeout=0.5, timeout=0.2)
            sleep(1)

    def write(self, stringToWrite):
        SerialHandler.__serial.write(str(stringToWrite).encode())

    def read(self) -> List[str]:
        lines = SerialHandler.__serial.readlines()
        return [x.decode() for x in lines]