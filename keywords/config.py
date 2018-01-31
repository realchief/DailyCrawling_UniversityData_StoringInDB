import json


class Config:
    config = {}

    @staticmethod
    def load():
        with open("/home/ubuntu/Aleksandar-Scrapy/workfolder/crawler/keywords/config.json", 'r') as f:
            Config.config = json.loads(f.read())
