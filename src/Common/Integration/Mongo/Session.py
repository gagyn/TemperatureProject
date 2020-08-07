import pymongo

class Session:
    def __init__(self, mongoConnectionString: str):
        self.client = pymongo.MongoClient(mongoConnectionString)
        self.database = self.client["temperatureProject"]
    
    def add(self, entity):
        collection = self.__get_collection(entity)
        collection.insert_one(entity)
    
    def get(self, entity):
        collection = self.__get_collection(entity)

    def __get_collection(self, entity):
        return self.database(type(entity).__name__ + 's')