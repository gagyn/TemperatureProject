from flask_pymongo import PyMongo
import json
from datetime import datetime

class ConfigurationService:
    def __init__(self, mongoClient: PyMongo):
        self.mongoClient = mongoClient

    def get_records_count(self) -> int:
        recordsCount = self.__get_configuration_by_name('recordsCount')
        if recordsCount == None:
            return 1000
        return recordsCount['value']

    def set_records_count(self, recordsCount: int):
        recordsCountEntity = {'name': 'recordsCount', 'createdAt': datetime.now(), 'value': recordsCount}
        self.__save_new_configuration(recordsCountEntity)

    def get_records_frequency(self):
        pass

    def set_records_frequency(self, frequency):
        pass

    def get_arduino_port(self) -> str:
        port = self.__get_configuration_by_name('port')
        if port is None:
            return self.__get_arduino_port_from_config_file()
        return port['value']

    def set_arduino_port(self, port: str):
        portEntity = {'name': 'port', 'createdAt': datetime.now(), 'value': port}
        self.__save_new_configuration(portEntity)

    def __get_arduino_port_from_config_file(self) -> str:
        with open('config.json') as configFile:
            return json.load(configFile)['port']

    def __get_configuration_by_name(self, configurationName: str) -> dict:
        return self.mongoClient.db.configurations.find_one({'name': configurationName})

    def __save_new_configuration(self, configurationEntity: dict):
        existingConfiguration = self.mongoClient.db.configurations.find_one_and_replace({'name': configurationEntity['name']}, configurationEntity)
        if existingConfiguration is None:
            self.mongoClient.db.configurations.insert_one(configurationEntity)
