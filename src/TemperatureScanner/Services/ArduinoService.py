from TemperatureScanner.Integration.Adruino.SerialHandler import SerialHandler
from Common.Configuration.ConfigurationService import ConfigurationService
from typing import List

class ArduinoService:
    def __init__(self, serialHandler: SerialHandler, configurationService: ConfigurationService):
        self.serialHandler = serialHandler
        self.configurationService = configurationService

    def read_now(self, records_count = 0) -> (float, int):
        if records_count == 0:
            records_count = self.configurationService.get_records_count()

        self.serialHandler.write(records_count)
        records: List[str] = list(self.serialHandler.read(records_count))
        if len(records) == 0:
            raise Exception('not connected to arduino')
        
        recordsAsNumbers = [float(x) for x in records]
        return self.__calculate_avg_temperature(recordsAsNumbers), len(recordsAsNumbers)

    def __calculate_avg_temperature(self, records: List[float]) -> float:
        records.sort()
        count = len(records)
        start = count // 10
        stop = count - start
        chosenRecords = records[start:stop]
        return sum(chosenRecords) / len(chosenRecords)