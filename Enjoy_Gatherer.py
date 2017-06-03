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

stop_enjoy = False

class Enjoy_Gatherer(Thread):
    
    def __init__ (self, city):

        Thread.__init__(self)
        
        self.name = "enjoy"
        self.city = city
        self.sess_status = False
        
    def log_message (self, scope, status):
        
        return '[{}] -> {} {}: {} {}'\
                    .format(datetime.datetime.now(),\
                            self.name,\
                            self.city,\
                            scope,\
                            status)        
        
    def check_session (self):        

        if not self.sess_status:
            self.start_session()
            self.sess_status = True
            self.session_start_time = datetime.datetime.now()
            
        else:
            try:
                if (datetime.datetime.now() - self.session_start_time).total_seconds() < 3000:
                    self.current_feed = self.get_feed()
                else:
                    try:
                        self.session.close()
                        self.sess_status = False                        
                    except:
                        print "Fail in closing session"
                    try:
                        self.start_session()
                        self.sess_status = True
                    except:
                        print "Fail in reopening session"
                        self.sess_status = False                        
                    try:
                        self.current_feed = self.get_feed()
                    except:
                        print "Fail in getting feed"
            except:
                print "FAIL"                        
        
    def start_session (self):

        self.url_home = 'https://enjoy.eni.com/it/' + self.city + '/map/'
                
        try:
            self.session = requests.Session()
            self.session.get(self.url_home)
            self.session_start_time = datetime.datetime.now()
            message = self.log_message("session","success")
        except:
            message = self.log_message("session","error")
        print message
            
    def get_feed (self):

        self.url_data = 'https://enjoy.eni.com/ajax/retrieve_vehicles'
        
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
            self.check_session()
            self.to_DB()
            self.last_feed = self.current_feed
            time.sleep(60)

Enjoy_Gatherer(sys.argv[1]).start()
