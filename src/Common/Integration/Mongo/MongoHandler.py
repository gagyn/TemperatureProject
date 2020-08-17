from flask_pymongo import PyMongo

class MongoHandler:
    def __init__(self, mongoClient: PyMongo):
        self.client = mongoClient
    
    def add(self, entity):
        collection = self.__get_collection(entity)
        collection.insert_one(entity)
    
    def get(self, entity):
        collection = self.__get_collection(entity)

    def __get_collection(self, entity):
        return self.client(type(entity).__name__ + 's')