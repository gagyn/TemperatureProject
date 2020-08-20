from typing import List
from serial import Serial
import datetime

class SerialReader:
    def __init__(self, arduinoPort: str):
        self.arduinoPort = arduinoPort

    def read(self, requestedLinesCount = 0):
        with Serial(self.arduinoPort, baudrate=19200, timeout=500) as serial:
            if requestedLinesCount is 0:
                return serial.readlines()
            return serial.readlines(requestedLinesCount)
