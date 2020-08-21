from serial import Serial
from Common.Configuration.ConfigurationService import ConfigurationService
from pymongo import MongoClient
import json

if __name__ == '__main__':
    with open('config.json') as configFile:
        data = json.load(configFile)

    pymongo = MongoClient(data['mongoConnectionString'])
    pymongo.db = pymongo.get_database(data['mongoDbName'])
    configurationService = ConfigurationService(pymongo)
    arduinoPort = configurationService.get_arduino_port()

    with Serial(arduinoPort, baudrate=19200, timeout=100) as serial:
        number = int(serial.read())
        print(number)