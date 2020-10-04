from Common.Configuration.ConfigurationService import ConfigurationService
from TemperatureScanner.Services.ArduinoService import ArduinoService
from TemperatureScanner.Services.WaitingService import WaitingService
import time
from flask_pymongo import PyMongo
import datetime

class FrequentRecordsReaderService:
    def __init__(self, configurationService: ConfigurationService, arduinoService: ArduinoService, waitingService: WaitingService, mongo: PyMongo):
        self.configurationService = configurationService
        self.arduinoService = arduinoService
        self.mongo = mongo
        self.waitingService = waitingService

    def start_frequent_service(self):
        time.sleep(1)
        shouldStartAsRunning = self.configurationService.get_reading_state() == 'running'
        if shouldStartAsRunning:
            self.waitingService.start(self._read_and_save)
            
    def start_reading(self):
        self.waitingService.start(self._read_and_save)
        self.configurationService.set_reading_state('running')

    def stop_reading(self):
        self.waitingService.cancel()
        self.configurationService.set_reading_state('paused')

    def restart_reading(self):
        self.waitingService.cancel()
        self.waitingService.start(self._read_and_save)

    def make_temperature_entity(self, value: float, recordsCount: int, sensorName: str) -> dict:
        return {'createdAt': datetime.datetime.utcnow(), 'value': value, 'basedOnRecordsCount': recordsCount, 'sensorNameId': sensorName}

    def _read_and_save(self):
        try:       
            (temperature, basedOnRecordsCount) = self.arduinoService.read_now()
            temperatureEntity = self.make_temperature_entity(temperature, basedOnRecordsCount, 'out1')
            self._add_to_base(temperatureEntity)
        except Exception as e:
            print(e)

    def _add_to_base(self, temperatureEntity: dict):
        self.mongo.db.temperatures.insert_one(temperatureEntity)
