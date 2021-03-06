from TemperatureScanner.Integration.Adruino.SerialHandler import SerialHandler
from Common.Configuration.ConfigurationService import ConfigurationService
from typing import List
from time import sleep

class ArduinoService:
    def __init__(self, serialHandler: SerialHandler, configurationService: ConfigurationService):
        self.serialHandler = serialHandler
        self.configurationService = configurationService

    def read_now(self, records_count = 0) -> (float, int):
        if records_count == 0:
            records_count = self.configurationService.get_records_count()

        self.serialHandler.write(records_count)
        sleep(0.2)
        records = self.serialHandler.read()
        if len(records) == 0:
            raise Exception('not connected to arduino')
        
        recordsAsNumbers = [float(x) for x in records]
        return self._calculate_avg_temperature(recordsAsNumbers), len(recordsAsNumbers)

    def _calculate_avg_temperature(self, records: List[float]) -> float:
        records.sort()
        count = len(records)
        start = count // 10
        stop = count - start
        chosenRecords = records[start:stop]
        return sum(chosenRecords) / len(chosenRecords)