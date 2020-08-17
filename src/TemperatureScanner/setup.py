from flask import Flask
from flask_pymongo import PyMongo
import json
from ..Common.Integration.Mongo import MongoHandler

app = Flask(__name__)

with open('config.json') as config_file:
    data = json.load(config_file)
    
app.config['MONGO_DBNAME'] = data['mongoDbName']
app.config['MONGO_URI'] = data['mongoConnectionString']

mongo = PyMongo(app)
mongoHandler = MongoHandler(mongo)
scannerApiController = ScannerApiController(mongoHandler)