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
        self.stopped = configurationService.get_reading_state() == 'paused'
        if self.stopped:
            self.stop_reading()
        else:
            self.start_reading()
        self._toRestart = False

    def start_frequent_service(self):
        time.sleep(1)
        self.waitingService.start(self._read_and_save)
            
    def start_reading(self):
        self.stopped = False
        self._toRestart = False
        self.configurationService.set_reading_state('running')

    def stop_reading(self):
        self.stopped = True
        self.configurationService.set_reading_state('paused')

    def restart_reading(self):
        self._toRestart = True

    def make_temperature_entity(self, value: float, recordsCount: int, sensorName: str) -> dict:
        return {'createdAt': datetime.datetime.utcnow(), 'value': value, 'basedOnRecordsCount': recordsCount, 'sensorNameId': sensorName}

    def _read_and_save(self):
        try:       
            temperatureEntity = self._read_temperature()
            self._add_to_base(temperatureEntity)
        except Exception as e:
            print(e)

    def _wait_if_stopped(self):
        while self.stopped:
            time.sleep(1)

    def _read_temperature(self) -> dict:
        (temperature, basedOnRecordsCount) = self.arduinoService.read_now()
        return self.make_temperature_entity(temperature, basedOnRecordsCount, 'out1')

    def _add_to_base(self, temperatureEntity: dict):
        self.mongo.db.temperatures.insert_one(temperatureEntity)
        
    def _wait_and_handle_restarts(self):
        lastSecondBeforeStopped = self._wait_till_next_record()
        while self._toRestart:
            self._toRestart = False
            self._wait_till_next_record(lastSecondBeforeStopped)

    def _wait_till_next_record(self, startWith = 0) -> int: # returns the second when was stopped
        secondsBetween = self.configurationService.get_records_seconds_between()
        for i in range(startWith, secondsBetween):
            time.sleep(1)
            if self.stopped:
                return i
            if self._toRestart:
                newSecondsBetween = self.configurationService.get_records_seconds_between()
                if i <= newSecondsBetween:
                    self._toRestart = False
                return i
        return secondsBetween
