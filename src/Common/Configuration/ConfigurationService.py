from flask_pymongo import PyMongo
import json
from datetime import datetime

class ConfigurationService:
    def __init__(self, mongoClient: PyMongo):
        self._mongoClient = mongoClient

    def get_records_count(self) -> int:
        recordsCount = self._get_configuration_value_by_name('recordsCount')
        if recordsCount is None:
            return int(self._get_default_value_from_config_file('recordsCount'))
        return int(recordsCount)

    def set_records_count(self, recordsCount: int):
        recordsCountEntity = self._create_configuration_entity()
        recordsCountEntity = {'name': 'recordsCount', 'createdAt': datetime.now(), 'value': recordsCount}
        self._save_new_configuration(recordsCountEntity)

    def get_records_seconds_between(self) -> int:
        secondsBetween = self._get_configuration_value_by_name('secondsBetween')
        if secondsBetween is None:
            return int(self._get_default_value_from_config_file('secondsBetween'))
        return int(secondsBetween)

    def set_records_seconds_between(self, secondsBetween: int):
        secondsBetweenEntity = self._create_configuration_entity('secondsBetween', secondsBetween)
        self._save_new_configuration(secondsBetweenEntity)

    def get_arduino_port(self) -> str:
        port = self._get_configuration_value_by_name('port')
        if port is None:
            return self._get_default_value_from_config_file('port')
        return port

    def set_arduino_port(self, port: str):
        portEntity = self._create_configuration_entity('port', port)
        self._save_new_configuration(portEntity)

    def get_reading_state(self) -> str:
        state = self._get_configuration_value_by_name('readingState')
        if state is None:
            return 'running'
        return state

    def set_reading_state(self, readingState: str) -> str:
        stateEntity = self._create_configuration_entity('readingState', readingState)
        self._save_new_configuration(stateEntity)

    def _get_default_value_from_config_file(self, configurationName: str) -> str:
        with open('config.json') as configFile:
            return json.load(configFile)[configurationName]

    def _get_configuration_value_by_name(self, configurationName: str) -> object:
        entity = self._mongoClient.db.configurations.find_one({'name': configurationName})
        if entity is None:
            return None
        return entity['value']

    def _create_configuration_entity(self, name: str, value: object) -> dict:
        return {'name': name, 'createdAt': datetime.now(), 'value': value}

    def _save_new_configuration(self, configurationEntity: dict):
        existingConfiguration = self._mongoClient.db.configurations.find_one_and_replace({'name': configurationEntity['name']}, configurationEntity)
        if existingConfiguration is None:
            self._mongoClient.db.configurations.insert_one(configurationEntity)
