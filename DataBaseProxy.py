import datetime

from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')

import logging
logging.basicConfig(filename=datetime.datetime.now().strftime("%Y-%m-%d") + ".log", 
                    level=logging.DEBUG)

class DataBaseProxy (object):
    
    def __init__ (self):
        
        self.db = client['UMAP']

    def log_message (self, record, scope, status):
        
        return '[{}] -> {} {}: {} {}'\
                    .format(datetime.datetime.now(),\
                            record["provider"],\
                            record["city"],\
                            scope,\
                            status)

    def insert (self, collection, record):
    
        collection = self.db[collection]
        try:
            collection.insert_one(record)
            logging.debug(self.log_message(record, "insert", "success"))
        except:
            logging.debug(self.log_message(record, "insert", "error"))

dbp = DataBaseProxy()