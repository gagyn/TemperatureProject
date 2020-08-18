from flask_pymongo import PyMongo
import json
from datetime import datetime

class ConfigurationService:
    def __init__(self, mongoClient: PyMongo):
        self.mongoClient = mongoClient

    def get_records_frequency(self):
        pass

    def set_records_frequency(self, frequency):
        pass

    def get_arduino_port(self):
        port = self.mongoClient.db.configurations.find_one({'name': 'port'})
        if port is None:
            port = self.__get_arduino_port_from_config_file()
        return port

    def set_arduino_port(self, port: str):
        portEntity = {'name': 'port', 'createdAt': datetime.now(), 'value': port}
        result = self.mongoClient.db.configurations.find_one_and_replace({'name': 'port'}, portEntity)
        if result is None:
            self.mongoClient.db.configurations.insert_one(portEntity)

    def __get_arduino_port_from_config_file(self) -> str:
        with open('config.json') as configFile:
            return json.load(configFile)['port']
