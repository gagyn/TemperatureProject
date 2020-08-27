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
        self.__toStop = False
        self.__toRestart = False

    def start_frequent_service(self):
        while True:
            if self.stopped:
                time.sleep(1)
                continue

            recordsCount = self.configurationService.get_records_count()
            record = self.arduinoService.read_now(records_count=recordsCount)
            temperatureEntity = {'createdAt': datetime.datetime.now(), 'value': record, 'basedOnRecordsCount': recordsCount}
            self.mongo.db.temperatures.insert_one(temperatureEntity)
            lastSecondBeforeStopped = self.__wait_till_next_record()

            while self.__toRestart:
                self.__toRestart = False
                self.__wait_till_next_record(lastSecondBeforeStopped)
            if self.__toStop:
                self.__toStop = False
                return
            
    def start_reading(self):
        self.stopped = False
        self.__toRestart = False
        self.__toStop = False
        self.configurationService.set_reading_state('running')

    def stop_reading(self):
        self.stopped = True
        self.__toStop = True
        self.configurationService.set_reading_state('paused')

    def restart_reading(self):
        self.__toRestart = True

    def __wait_till_next_record(self, startWith = 0) -> int: # returns the second when was stopped
        secondsBetween = self.configurationService.get_records_seconds_between()
        for i in range(startWith, secondsBetween):
            time.sleep(1)
            if self.__toStop:
                return i
            if self.__toRestart:
                newSecondsBetween = self.configurationService.get_records_seconds_between()
                if i <= newSecondsBetween:
                    self.__toRestart = False
                return i
        return secondsBetween
