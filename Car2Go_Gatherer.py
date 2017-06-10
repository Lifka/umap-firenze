import sys

def print_exception ():
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print exc_type
    print exc_obj
    print exc_tb.tb_lineno   
    
from threading import Thread

import datetime
import time

#import logging
#logging.basicConfig(filename= "./Logs/" + datetime.datetime.now().strftime("%Y-%m-%d") + ".log", 
#                    level=logging.DEBUG)        

import requests
import json

from DataBaseProxy import dbp

stop_car2go = False

class Car2Go_Gatherer(Thread):

    
    def __init__ (self, city):

        Thread.__init__(self)
        
        self.name = "car2go"
        self.city = city
        
    def log_message (self, scope, status):
        
        return '[{}] -> {} {}: {} {}'\
                    .format(datetime.datetime.now(),\
                            self.name,\
                            self.city,\
                            scope,\
                            status)
            
    def get_feed (self):
        
        self.url = 'https://www.car2go.com/api/v2.1/vehicles?oauth_consumer_key=polito&format=json&loc=' + self.city
        
        try:
            feed = json.loads(requests.get(self.url).text)
            message = self.log_message("feed","success")
        except:
            print_exception()
            feed = {}
            message = self.log_message("feed","error")
        print message

        return feed
                
    def to_DB (self):
    
        dbp.insert("snapshots", 
                   {
                     "timestamp": datetime.datetime.now(),
                     "provider": self.name,
                     "city": self.city,
                     "snapshot": self.current_feed
                     }
                    )
        
    def run(self):
                
        while True:
            self.current_feed = self.get_feed()
            self.to_DB()
            self.last_feed = self.current_feed
            time.sleep(60)

Car2Go_Gatherer(sys.argv[1]).start()
