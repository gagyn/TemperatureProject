from typing import List
from serial import Serial

class SerialReader:
    def __init__(self, arduinoPort: str):
        self.arduinoPort = arduinoPort

    def read(self, requestedLinesCount = 0) -> List[str]:
        with Serial(self.arduinoPort, baudrate=19200, timeout=500) as serial:
            if requestedLinesCount is 0:
                return serial.readlines().decode()
            return serial.readlines(requestedLinesCount).decode()
