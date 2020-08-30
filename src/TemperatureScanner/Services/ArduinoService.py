from TemperatureScanner.Integration.Adruino.SerialReader import SerialReader
from TemperatureScanner.Integration.Adruino.SerialWriter import SerialWriter
from Common.Configuration.ConfigurationService import ConfigurationService
from typing import List

class ArduinoService:
    def __init__(self, serialReader: SerialReader, serialWriter: SerialWriter, configurationService: ConfigurationService):
        self.serialReader = serialReader
        self.serialWriter = serialWriter
        self.configurationService = configurationService

    def read_now(self, records_count = 0) -> float:
        if records_count == 0:
            records_count = self.configurationService.get_records_count()

        self.serialWriter.write(records_count)
        records: List[str] = self.serialReader.read(records_count)
        if len(records) == 0:
            raise Exception('not connected to arduino')
        
        return self.__calculate_avg_temperature(records)

    def __calculate_avg_temperature(self, records: List[float]) -> float:
        records.sort()
        count = len(records)
        start = count // 10
        stop = count - start
        chosenRecords = records[start:stop]
        return sum(chosenRecords) / len(chosenRecords)