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

    
    def __init__ (self, cities):

        Thread.__init__(self)
        
        self.name = "car2go"
        self.cities = cities
        self.sess_status = {city:False for city in self.cities}
        
    def log_message (self, scope, status):
        
        return '[{}] -> {} {}: {} {}'\
                    .format(datetime.datetime.now(),\
                            self.name,\
                            self.city,\
                            scope,\
                            status)        
        
    def check_session (self):        

        if not self.sess_status[self.city]:
            self.sess_status[self.city] = True
            self.start_session()
            self.session_start_time = datetime.datetime.now()
            
#        if (datetime.datetime.now() - self.session_start_time).total_seconds() > 600:
#            self.session = self.session.close()
#            self.start_session()
#            self.session_start_time = datetime.datetime.now()
        
    def start_session (self):

        self.url_home = 'https://www.car2go.com/api/v2.1/vehicles?oauth_consumer_key=polito&format=json&loc=' + self.city
                
        try:
            self.session = requests.Session()
            self.session.get(self.url_home)
            self.session_start_time = datetime.datetime.now()
            message = self.log_message("session","success")
        except:
            message = self.log_message("session","error")
        print message
            
    def get_feed (self):
        
        self.url_data = self.url_home
        
        try:
            feed = json.loads(self.session.get(self.url_data).text)
            message = self.log_message("feed","success")
        except:
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
            for city in self.cities:
                self.city = city
                self.check_session()
                self.current_feed = self.get_feed()
                self.to_DB()
                self.last_feed = self.current_feed
            time.sleep(60)


car2go_cities = [
                    "wien",
                    "calgary",
                    "montreal",
                    "vancouver",
                    "hamburg",
                    "berlin",
                    "frankfurt",
                    "muenchen",
                    "rheinland",
                    "stuttgart",
                    "firenze",
                    "torino",
                    "milano",
                    "roma",
                    "amsterdam",
                    "madrid",
                    "austin",
                    "columbus",
                    "denver",
                    "newyorkcity",
                    "portland",
                    "seattle",
                    "washingtondc"
                ]

Car2Go_Gatherer(car2go_cities).start()
