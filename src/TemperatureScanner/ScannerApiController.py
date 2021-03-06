from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import json
from TemperatureScanner.Services.ArduinoService import ArduinoService
from TemperatureScanner.Integration.Adruino.SerialHandler import SerialHandler
from Common.Configuration.ConfigurationService import ConfigurationService
from TemperatureScanner.Services.FrequentRecordsReaderService import FrequentRecordsReaderService
from TemperatureScanner.Services.WaitingService import WaitingService
from datetime import datetime
import threading
import os
app = Flask(__name__)

if app.debug:
    configFileName = 'config-dev.json'
else:
    configFileName = 'config.json'

with open(configFileName) as configFile:
    data = json.load(configFile)
    
app.config['MONGO_DBNAME'] = data['mongoDbName']
app.config['MONGO_URI'] = data['mongoConnectionString']

mongo = PyMongo(app)

configurationService = ConfigurationService(mongo)
port = configurationService.get_arduino_port()
serialHandler = SerialHandler(port)
arduinoService = ArduinoService(serialHandler, configurationService)
waitingService = WaitingService(configurationService)
frequentRecordsReaderService = FrequentRecordsReaderService(configurationService, arduinoService, waitingService, mongo)
backgroundThread = threading.Thread(target=frequentRecordsReaderService.start_frequent_service, name='frequentRecordsReader')
backgroundThread.start()

@app.route('/readnow', methods=['POST'])
def read_now():
    (temperature, basedOnRecordsCount) = arduinoService.read_now()
    temperatureEntity = frequentRecordsReaderService.make_temperature_entity(temperature, basedOnRecordsCount, 'out1')
    shouldSaveToBase = request.args.get('shouldSave')
    temperatureToReturn = dict(temperatureEntity)
    if shouldSaveToBase is not None and shouldSaveToBase.lower() == 'true':
        mongo.db.temperatures.insert_one(temperatureEntity)
    return jsonify({'response': 'OK - reading has been completed', 'value': temperatureToReturn})

@app.route('/setport', methods=['POST'])
def set_port():
    port = str(request.json['port'])
    configurationService.set_arduino_port(port)
    return jsonify({'response': 'OK - Arduino port changed'})

@app.route('/setrecordscount', methods=['POST'])
def set_records_count():
    recordsCount = int(request.json['recordsCount'])
    configurationService.set_records_count(recordsCount)
    return jsonify({'response': 'OK - Records count changed'})

@app.route('/setsecondsbetween', methods=['POST'])
def set_seconds_between_records():
    secondsBetween = int(request.json['secondsBetween'])
    configurationService.set_records_seconds_between(secondsBetween)
    frequentRecordsReaderService.restart_reading()
    return jsonify({'response': 'OK - Seconds between records changed'})

@app.route('/pause', methods=['GET'])
def pause_reading():
    state = configurationService.get_reading_state()
    if state == 'paused':
        return 400, 'Reading is already paused'
    frequentRecordsReaderService.stop_reading()
    return jsonify({'response': 'OK - Reading has been stopped'})

@app.route('/start', methods=['GET'])
def start_reading():
    state = configurationService.get_reading_state()
    if state == 'running':
        return 400, 'Reading is already running'
    frequentRecordsReaderService.start_reading()
    return jsonify({'response': 'OK - Reading has been started'})

if __name__ == '__main__':
    app.run()