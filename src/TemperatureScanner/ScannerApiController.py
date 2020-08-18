from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import json
from Common.Integration.Mongo.MongoHandler import MongoHandler

app = Flask(__name__)

with open('config.json') as configFile:
    data = json.load(configFile)
    
app.config['MONGO_DBNAME'] = data['mongoDbName']
app.config['MONGO_URI'] = data['mongoConnectionString']

mongo = PyMongo(app)
mongoHandler = MongoHandler(mongo)

@app.route('/readnow', methods=['GET'])
def read_now():
    return jsonify({'text': 'hello index'})

@app.route('/hello_world', methods=['GET'])
def hello_world():
    return 'hello world'

app.run()