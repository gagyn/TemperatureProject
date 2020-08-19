from temperatureproject.integration.adruino.serialreader import SerialReader
from integration.adruino.serialwriter import SerialWriter

class ArduinoService:
    def __init__(self, serialReader: SerialReader, serialWriter: SerialWriter):
        self.serialReader = serialReader
        self.serialWriter = serialWriter

    