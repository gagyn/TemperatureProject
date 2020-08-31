from flask_pymongo import PyMongo
import json
from datetime import datetime

class ConfigurationService:
    def __init__(self, mongoClient: PyMongo):
        self.mongoClient = mongoClient

    def get_records_count(self) -> int:
        recordsCount = self.__get_configuration_by_name('recordsCount')
        if recordsCount is None:
            return int(self.__get_default_value_from_config_file('recordsCount'))
        return recordsCount['value']

    def set_records_count(self, recordsCount: int):
        recordsCountEntity = {'name': 'recordsCount', 'createdAt': datetime.now(), 'value': recordsCount}
        self.__save_new_configuration(recordsCountEntity)

    def get_records_seconds_between(self) -> int:
        secondsBetween = self.__get_configuration_by_name('secondsBetween')
        if secondsBetween is None:
            return int(self.__get_default_value_from_config_file('secondsBetween'))
        return secondsBetween['value']

    def set_records_seconds_between(self, secondsBetween: int):
        secondsBetweenEntity = {'name': 'secondsBetween', 'createdAt': datetime.now(), 'value': secondsBetween}
        self.__save_new_configuration(secondsBetweenEntity)

    def get_arduino_port(self) -> str:
        port = self.__get_configuration_by_name('port')
        if port is None:
            return self.__get_default_value_from_config_file('port')
        return port['value']

    def set_arduino_port(self, port: str):
        portEntity = {'name': 'port', 'createdAt': datetime.now(), 'value': port}
        self.__save_new_configuration(portEntity)

    def get_reading_state(self) -> str:
        state = self.__get_configuration_by_name('readingState')
        if state is None:
            return 'stopped'
        return state['value']

    def set_reading_state(self, readingState: str) -> str:
        stateEntity = {'name': 'readingState', 'createdAt': datetime.now(), 'value': readingState}
        self.__save_new_configuration(stateEntity)
        
    def __get_default_value_from_config_file(self, configurationName: str) -> str:
        with open('config.json') as configFile:
            return json.load(configFile)[configurationName]

    def __get_configuration_by_name(self, configurationName: str) -> dict:
        return self.mongoClient.db.configurations.find_one({'name': configurationName})

    def __save_new_configuration(self, configurationEntity: dict):
        existingConfiguration = self.mongoClient.db.configurations.find_one_and_replace({'name': configurationEntity['name']}, configurationEntity)
        if existingConfiguration is None:
            self.mongoClient.db.configurations.insert_one(configurationEntity)
