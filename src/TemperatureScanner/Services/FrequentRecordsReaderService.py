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

    def read_frequently(self):
        while True:
            recordsCount = self.configurationService.get_records_count()
            record = self.arduinoService.read_now(records_count=recordsCount)
            temperatureEntity = {'createdAt': datetime.now(), 'value': record, 'basedOnRecordsCount': recordsCount}
            mongo.db.temperatures.insert_one(temperatureEntity)
            self.__wait_till_next_record()
            
    def __wait_till_next_record(self):
        secondsBetween = self.configurationService.get_records_seconds_between()
        for i in range(secondsBetween):
            time.sleep(1)
            currentConfiguration = self.configurationService.get_records_seconds_between()
            if currentConfiguration == 0:
                return
