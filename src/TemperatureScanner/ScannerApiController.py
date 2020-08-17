from flask import Flask

class ScannerApiController:
    def __init__(self, mongoHandler):
        self.mongo = mongoHandler

    @app.route("/hello", methods=['GET'])
    def hello_world(self):
        return 'hello world'