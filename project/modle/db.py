import pymongo
import config
import asyncio
# from ..config import database  

def singo(cls):
    instance=dict()
    def _singo(*args,**kw):
        if cls not in instance:
            instance[cls]=cls(*args,**kw)
        return instance[cls]
    return _singo

@singo            
class mongodb:
    def __init__(self):
        client = pymongo.MongoClient(host=config.database["host"], port=config.database["port"],)
        self.db = client.lee
