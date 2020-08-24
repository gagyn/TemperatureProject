from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import json
from TemperatureScanner.Services.ArduinoService import ArduinoService
from TemperatureScanner.Integration.Adruino.SerialReader import SerialReader
from TemperatureScanner.Integration.Adruino.SerialWriter import SerialWriter
from Common.Configuration.ConfigurationService import ConfigurationService
from TemperatureScanner.Services.FrequentRecordsReaderService import FrequentRecordsReaderService
from datetime import datetime
import threading

app = Flask(__name__)

with open('config.json') as configFile:
    data = json.load(configFile)
    
app.config['MONGO_DBNAME'] = data['mongoDbName']
app.config['MONGO_URI'] = data['mongoConnectionString']

mongo = PyMongo(app)

configurationService = ConfigurationService(mongo)
port = configurationService.get_arduino_port()
serialReader = SerialReader(port)
serialWriter = SerialWriter(port)
arduinoService = ArduinoService(serialReader, serialWriter, configurationService)
frequentRecordsReaderService = FrequentRecordsReaderService(configurationService, arduinoService, mongo)
backgroundThread = threading.Thread(target=frequentRecordsReaderService.read_frequently, name='frequentRecordsReader')
backgroundThread.start()

@app.route('/readnow', methods=['POST'])
def read_now():
    shouldSaveToBase = request.json['shouldSave'].lower() == 'true'
    temperature = arduinoService.read_now()
    temperatureEntity = {'createdAt': datetime.now(), 'value': temperature, 'basedOnRecordsCount': configurationService.get_records_count()}
    if shouldSaveToBase:
        mongo.db.temperatures.insert_one(temperatureEntity)
    return jsonify({'response': 'OK - reading was completed', 'value': temperatureEntity})

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
    secondsBetween = int(request['secondsBetween'])
    configurationService.set_records_seconds_between(secondsBetween)
    return jsonify({'response': 'OK - Seconds between records changed'})

app.run()