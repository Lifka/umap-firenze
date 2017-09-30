#!/usr/bin/python

import sys

def print_exception ():
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print (exc_type)
    print (exc_obj)
    print (exc_tb.tb_lineno)   
    
from threading import Thread

import datetime
import time

#import logging
#logging.basicConfig(filename= "./Logs/" + datetime.datetime.now().strftime("%Y-%m-%d") + ".log", 
#                    level=logging.DEBUG)        

import requests
import json

from DataBaseProxy import dbp

class Car2Go_Gatherer():
    
    def __init__ (self, city):
        
        self.name = "car2go"
        self.city = city
        self.session = requests.Session()
        
    def log_message (self, scope, status):
        
        return '[{}] -> {} {}: {} {}'\
                    .format(datetime.datetime.now(),\
                            self.name,\
                            self.city,\
                            scope,\
                            status)
                
    def to_DB (self):
    
        dbp.insert("snapshots", 
                   {
                     "timestamp": datetime.datetime.now(),
                     "provider": self.name,
                     "city": self.city,
                     "snapshot": self.current_feed
                     }
                    )
            
    def get_feed (self):
        
        self.url = 'https://www.car2go.com/api/v2.1/vehicles?oauth_consumer_key=polito&format=json&loc=' + self.city
        
        try:
            feed = json.loads(self.session.get(self.url).text)
            message = self.log_message("feed","success")
        except:
            print_exception()
            feed = {}
            message = self.log_message("feed","error")
        print (message)

        self.current_feed = feed
        
    def run(crawler):
                
        while True:
            crawler.get_feed()
            crawler.to_DB()
            crawler.last_feed = self.current_feed
            time.sleep(60)

#gatherer = Car2Go_Gatherer(sys.argv[1])
#gatherer.run()

city = "Firenze"
crawler =  Car2Go_Gatherer(city)

while True:
	crawler.get_feed()
	crawler.to_DB()
	time.sleep(20)