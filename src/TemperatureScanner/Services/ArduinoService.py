from TemperatureScanner.Integration.Adruino.SerialReader import SerialReader
from TemperatureScanner.Integration.Adruino.SerialWriter import SerialWriter
from Common.Configuration.ConfigurationService import ConfigurationService

class ArduinoService:
    def __init__(self, serialReader: SerialReader, serialWriter: SerialWriter, configurationService: ConfigurationService):
        self.serialReader = serialReader
        self.serialWriter = serialWriter
        self.configurationService = configurationService

    def read_now(self, records_count = 0):
        if records_count == 0:
            records_count = self.configurationService.get_records_count()

        self.serialWriter.write(records_count)
        records = self.serialReader.read(records_count)
        return records
