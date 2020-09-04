import time
from Common.Configuration.ConfigurationService import ConfigurationService
from TemperatureScanner.Services.ArduinoService import ArduinoService
from flask_pymongo import PyMongo
import datetime

class FrequentRecordsReaderService:
    def __init__(self, configurationService: ConfigurationService, arduinoService: ArduinoService, mongo: PyMongo):
        self.configurationService = configurationService
        self.arduinoService = arduinoService
        self.mongo = mongo
        self.stopped = configurationService.get_reading_state() == 'paused'
        self._toRestart = False

    def start_frequent_service(self):
        time.sleep(1)
        while True:
            if self.stopped:
                time.sleep(1)
                continue

            (temperature, basedOnRecordsCount) = self.arduinoService.read_now()
            temperatureEntity = {'createdAt': datetime.datetime.utcnow(), 'value': temperature, 'basedOnRecordsCount': basedOnRecordsCount, 'sensorNameId': 'out1'}
            self.mongo.db.temperatures.insert_one(temperatureEntity)
            lastSecondBeforeStopped = self._wait_till_next_record()

            while self._toRestart:
                self._toRestart = False
                self._wait_till_next_record(lastSecondBeforeStopped)
            
    def start_reading(self):
        self.stopped = False
        self._toRestart = False
        self.configurationService.set_reading_state('running')

    def stop_reading(self):
        self.stopped = True
        self.configurationService.set_reading_state('paused')

    def restart_reading(self):
        self._toRestart = True

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
