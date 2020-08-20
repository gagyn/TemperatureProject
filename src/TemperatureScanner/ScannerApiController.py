from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import json
from TemperatureScanner.Services.ArduinoService import ArduinoService
from TemperatureScanner.Integration.Adruino.SerialReader import SerialReader
from TemperatureScanner.Integration.Adruino.SerialWriter import SerialWriter
from Common.Configuration.ConfigurationService import ConfigurationService

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
    arduinoService.read_now()
    return jsonify({'text': 'OK - reading was completed'})

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
    
@app.route('/hello_world', methods=['GET'])
def hello_world():
    return 'hello world'

app.run()