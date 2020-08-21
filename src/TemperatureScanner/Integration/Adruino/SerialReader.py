from typing import List
from serial import Serial

class SerialReader:
    def __init__(self, arduinoPort: str):
        self.arduinoPort = arduinoPort

    def read(self, requestedLinesCount = 0) -> List[str]:
        with Serial(self.arduinoPort, baudrate=19200, timeout=1) as serial:
            if requestedLinesCount == 0:
                return serial.readlines().decode()
            return [x.decode() for x in serial.readlines(requestedLinesCount)]
