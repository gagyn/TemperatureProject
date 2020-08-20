from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import json
from TemperatureScanner.Services.ArduinoService import ArduinoService
from TemperatureScanner.Integration.Adruino.SerialReader import SerialReader
from TemperatureScanner.Integration.Adruino.SerialWriter import SerialWriter
from Common.Configuration.ConfigurationService import ConfigurationService
from datetime import datetime

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

@app.route('/readnow', methods=['GET'])
def read_now():
    temperature = arduinoService.read_now()
    temperatureEntity = {'createdAt': datetime.now(), 'value': temperature, 'basedOnRecordsCount': configurationService.get_records_count()}
    mongo.db.temperatures.insert_one(temperatureEntity)
    return jsonify({'text': 'OK - reading was completed', 'value': temperatureEntity})

@app.route('/setport', methods=['POST'])
def set_port():
    port = str(request.json['port'])
    configurationService.set_arduino_port(port)
    return jsonify({'text': 'OK - Arduino port changed'})

@app.route('/setrecordscount', methods=['POST'])
def set_records_count():
    recordsCount = int(request.json['recordsCount'])
    configurationService.set_records_count(recordsCount)
    return jsonify({'text': 'OK - Records count changed'})

app.run()