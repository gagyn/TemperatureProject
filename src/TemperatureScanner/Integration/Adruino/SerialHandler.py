from typing import List
from serial import Serial

class SerialHandler:
    __serial = None
    def __init__(self, arduinoPort: str):
        if SerialHandler.__serial is None:
            SerialHandler.__serial = Serial(arduinoPort, baudrate=19200, write_timeout=2, timeout=3)

    def write(self, stringToWrite):
        SerialHandler.__serial.write(str(stringToWrite).encode())

    def read(self, requestedLinesCount = 0) -> List[str]:
        if requestedLinesCount == 0:
            return [x.decode() for x in SerialHandler.__serial.readlines()]
        lines = SerialHandler.__serial.readlines()
        return [x.decode() for x in lines]