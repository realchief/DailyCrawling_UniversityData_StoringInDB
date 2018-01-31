import json


class Config:
    config = {}

    @staticmethod
    def load():
        with open("keywords/config.json", 'r') as f:
            Config.config = json.loads(f.read())
