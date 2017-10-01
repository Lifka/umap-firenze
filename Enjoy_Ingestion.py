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

stop_enjoy = False

class Enjoy_Gatherer():
    
    def __init__ (self, city):
        
        self.name = "enjoy"
        self.city = city
        
        self.sess_status = False
        self.start_session()
        self.sess_status = True
        self.session_start_time = datetime.datetime.now()       
            
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
                    
    def start_session (self):

        self.url_home = 'https://enjoy.eni.com/it/' + self.city + '/map/'
        
        message = self.log_message("session 4","success")

        try:
            self.session = requests.Session()
        except Exception:
            message = self.log_message("session 1","error")
            print (message)

        try:
            self.session.get(self.url_home)
        except Exception:
            message = self.log_message("session 2","error")
            print (message + " for " + self.url_home)

        try:
            self.session_start_time = datetime.datetime.now()
        except Exception:
            print (message)

        print (message)

            
    def get_feed (self):

        self.url_data = 'https://enjoy.eni.com/ajax/retrieve_vehicles'
        
        try:
            feed = json.loads(self.session.get(self.url_data).text)
            message = self.log_message("feed","success")
        except:
            feed = {}
            message = self.log_message("feed","error")
        print (message)

        self.current_feed = feed
        
    def check_session (self):        

        if not self.sess_status:
            self.start_session()
            self.sess_status = True
            self.session_start_time = datetime.datetime.now()            
        else:
            try:
                if (datetime.datetime.now() - self.session_start_time).total_seconds() < 3000:
                    self.get_feed()
                    self.to_DB()
                    self.last_feed = self.current_feed
                else:
                    try:
                        self.session.close()
                        self.sess_status = False                        
                    except:
                        print ("Fail in closing session")
                    try:
                        self.start_session()
                        self.sess_status = True
                    except:
                        print ("Fail in restarting session")
                        self.sess_status = False                        
                    try:
                        self.get_feed()
                        self.to_DB()
                        self.last_feed = self.current_feed
                    except:
                        print ("Fail in getting feed")
            except:
                print ("FAIL")
        
    def run(crawler):
                
        while True:
            crawler.check_session()
            time.sleep(60)


# City name must to be lowecase
city = "firenze"
crawler =  Enjoy_Gatherer(city)
crawler.run()
