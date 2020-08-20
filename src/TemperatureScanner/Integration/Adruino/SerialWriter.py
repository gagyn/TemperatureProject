from serial import Serial

class SerialWriter:
    def __init__(self, arduinoPort: str):
        self.arduinoPort = arduinoPort

    def write(self, stringToWrite):
        with Serial(self.arduinoPort, baudrate=19200, timeout=2000) as serial:
            serial.write(str(stringToWrite).encode())
