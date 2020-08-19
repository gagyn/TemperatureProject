from typing import List
import serial
import datetime

class SerialReader:
    def __init__(self, arduinoPort: str):
        self.ser = serial.Serial(port=arduinoPort, baudrate=19200)
        self.arduinoPort = arduinoPort