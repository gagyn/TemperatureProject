import pymongo


class Session:
    def __init__(self, mongoConnectionString: str):
        self.client = pymongo.MongoClient(mongoConnectionString)
        self.database = self.client["temperatureProject"]
    