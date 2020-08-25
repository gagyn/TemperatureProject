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

    def stop_reading(self):
        self.stopped = True

    def start_reading_frequently(self):
        while self.stopped is False:
            recordsCount = self.configurationService.get_records_count()
            record = self.arduinoService.read_now(records_count=recordsCount)
            temperatureEntity = {'createdAt': datetime.now(), 'value': record, 'basedOnRecordsCount': recordsCount}
            mongo.db.temperatures.insert_one(temperatureEntity)
            self.__wait_till_next_record()
            
    def __wait_till_next_record(self):
        secondsBetween = self.configurationService.get_records_seconds_between()
        for i in range(secondsBetween):
            time.sleep(1)
            currentConfiguration = self.configurationService.get_reading_state()
            if currentConfiguration == 'paused':
                return
