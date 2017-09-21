import sys

def print_exception ():
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print exc_type
    print exc_obj
    print exc_tb.tb_lineno   
    
from threading import Thread

import datetime
import time

import googlemaps

#import logging
#logging.basicConfig(filename= "./Logs/" + datetime.datetime.now().strftime("%Y-%m-%d") + ".log", 
#                    level=logging.DEBUG)        

import requests
import json

from DataBaseProxy import dbp

import pandas as pd

class Google_Manager(Thread):
    
    def __init__ (self, city):
        
        Thread.__init__(self)
        self.daemon = True
        
        self.name = "google"
        self.city = city
        
        self.keys = pd.Series([
                        'AIzaSyD3PdBLQxWMDsaJ1tdHOs02QNBuIEqLSiQ', 
                        'AIzaSyBnUsB3u6Blg23D5uqIQPnM_1Pawkp5VLY',
                        'AIzaSyBaaQQyMnT7MUI421WdO67g66igzXL2O4A',
                        'AIzaSyDbPG5qS-g0pROiPRcOT2G-keWi54ie2-M',
                        'AIzaSyCjy-sVWBCyN9FOjBeNg2_OeULs-uXSmMI',
                        'AIzaSyAUrnCmaEs7e7izfCiKYm-k7Ap0EwZzYes',
                        'AIzaSyCeT4Z_Cfabvpnh2FBbf3TCrhBNtwlfVwU',
                        'AIzaSyAcPVep5aXJLbuBDV7Qn_JaWSpD4o6s30w', 
                        'AIzaSyBHz8SA5BKIJDOu9mtLJb5JilGvcLnGIiM',
                        'AIzaSyBqMJcxNQUmciUN8qsI-4JVO9Hh_EJqNfE',
                        'AIzaSyB9XupnKFaH-zuVg_lBlz7NO8q6QpWFKZk',
                        'AIzaSyAVpeQaUjVPZznjp1b1sbtUl2iBzHSuGek',
                        'AIzaSyCoFpO5q5MatCal_1lLaxVCr6LcXePo91M',
                        'AIzaSyCGfLn4VqFrbV1PFc6duXi7ojPktJb-ta4',
                        'AIzaSyA6zgFdORCnKRnpp74Ew925aCwbSmzsM9U',
                        'AIzaSyBSjjou5aXnl-9L3SIaJR05Vc3Zb8j0WpY',
                        'AIzaSyAKaQDrgawidGlRNkjqTIMngFZs7pOV8Zc',
                        'AIzaSyCnksllWfpV0D3iDBomyKRFUkqEvEoNtKg',
                        'AIzaSyB0ggpBGN6wRpsA1cdfAgO2iVtSt6Nj41I',
                        'AIzaSyDVU9CsZY89DZv7JC7N5u8HTWrppGJNOko',  
                        'AIzaSyCDdrDzYVj0zwvV3Xhx9IJ6gv-L9PVXYaM',
                        'AIzaSyC846uXMy_r_Oh0jDBZdt5IzZnm4FuQi4g',
                        'AIzaSyCgI76-0WngwQVoTjQHwMuV0RoOetOqdaY',
                        'AIzaSyCDHutrFFMeC_Eabvx3xlPWXBKRbAq3uiY',
                        'AIzaSyB0s6yNxx5zP8Z6_-fG-8dRTiTBbQnpyRM',
                        'AIzaSyD1KTSXE5ZI1ZhlLkcHL0Se4of7E-ySF0s',
                        'AIzaSyCrB9XXWrMQxh2u7MhAe85T3wxGgSub5Wo',
                        'AIzaSyDVmI2S_fSIiMd2sXxCoUFJAltlSkHue4A',
                        'AIzaSyAhHK0alplPwl8F1EbBQdg3geZSFsagaEY',
                        'AIzaSyCO3Lg7nkuXAxPamTxuFrQmxkAYn-DRt2M', 
                        'AIzaSyAGH6f-iU3mniyU74tPDoYlTv7KfD9GGts',
                        'AIzaSyDnjsWBJLiu2KeQuB06SI3MX5oNcSxYGpk',
                        'AIzaSyA02bc_0MCLk9bJ5VQl61friKy_jez-fDg',
                        'AIzaSyDE1gmIDOwgNqZwtPG4n0cXuAWJC-o6zqs',  
                        'AIzaSyBHDeDRrHZUWZGLpCYX-lsOCJtpE_iOmxY',  
                        'AIzaSyDXITzscAk9WiYdSufNbCXMb8S0N6vMKo4',
                        'AIzaSyD4-UC0o3G5ZGsu-10iAaJk8UbPuoo_8Zs',
                        'AIzaSyBfJR-CbDlJTP5muitqaPPZpRyG0pwnV8c', 
                        'AIzaSyDRMVFkibqRU2ZyupJK21K08YdeU4huADI',
                        'AIzaSyCjgNFAJJgLr_uAETkXR0oBJOfm3waUCEI',
                        'AIzaSyC0KdkkbI1KkO8SOTg3LAWDvrH31yek14s', 
                        'AIzaSyBzWqwdMfkFYlMEOHEukfJEQ5UhV-3jRaU',
                        'AIzaSyDmOL7veIgsgNGBI7mSp6Ae7WKg5xC-M9A', 
                        'AIzaSyCZ_HyYgD0e5PE_IbcUAm86tgRdqTKIVa4', 
                        'AIzaSyDINMpddT6_02MXVVh_eZX_loznPYkk9RQ', 
                        'AIzaSyArjlKz9vAzX6CSCNYXkfjbejybaeCG1tI',
                        'AIzaSyBTmkpRo_chM1F6EKWL49XpuZThmNLDI1Q',
                        'AIzaSyBTuu3MBUtqKNh9U0TdLK1cR6RmYFmTSNI',
                        'AIzaSyAdNcdinGUCkoIuxYrYYmASNMc--yClRGU',
                        'AIzaSyAjHuNQcgdppxyLzxTZLnebLgQrqHYU9rs',
                        'AIzaSyAMEAKU2tvWlAD9dTW6caHQz7MOpY5sEts',
                        'AIzaSyDQtEe-SCGTzBdvzICGB0xDQhW1Fwes1IM',
                        'AIzaSyAsD334lOk1j3kcxJsukjxCU7gYiyhCwEw',
                        'AIzaSyAgZ0CVty4csyFOahjJ6qLt45SkvGkLNws',
                        'AIzaSyBV0Pt5zrM3FfQZthXNVcnk-LGlEX-VJM8',
                        'AIzaSyD27GZgUF9EvBm9FnnxtYvITr2T1DoXbgs',
                        'AIzaSyBuB0z38UKKpRr2Q-yE2cYb_G0fzK35l58',
                        'AIzaSyBiOBLKT6Lhqe1S6Snr6kXjm8k1omlk84E',
                        'AIzaSyCiO7Mq1126rVOhB7GviIn9RHmi-WPMdMI',
                        'AIzaSyAqkZFyTXCZ0uw9kLlQqk0SoCGJTROwFOU',
                        'AIzaSyCj185lSh8Jmy_yuFY5WUGzDXLSVGaFfl8',
                        'AIzaSyDW2f8E8jbPAPOc5HkrV6FxpAlN2CC6SnY',
                        'AIzaSyCCykwZbKA6HP37jMaqBMeNF-vd_I5IClU',
                        'AIzaSyCzyusNzfAXGt_I6llVedB3XgHnrnRSguc',
                        'AIzaSyCNAPVUGE009Jwt-HFcJzkICgip-Vthrqo',
                        'AIzaSyBNjWRFmiMG6nrLgM3yl4OjDzqk5WUaK3g',
                        'AIzaSyCxueXvh-KigSV57C_xU2s4IqsfncuODNQ',
                        'AIzaSyCLhyRuqK4ToyKpXRq9Bj3EwGGVu5DqP3Y',
                        'AIzaSyDY-vxkPbJ-fbpKvKrrAB87PU_MgsdPvys'
                        'AIzaSyBWpLux2H4qWJ83hYboLZzj_MW20FKgu38',
                        'AIzaSyA9cuVnYlm1_lAv2pZdpic4lPdWQeTnSTQ',
                        'AIzaSyAe8X4tnMrNC8VgAzvyNCxyzMla5zTDfLs',
                        'AIzaSyAKZRcJtQCY-3zRLKPO0fbLuRmZ-VNCS20',
                        'AIzaSyBWLEjpvkaMVE3_VMWJdfDhlhqVVXRYALI',
                        'AIzaSyAj0HTPsaEybv8UmeHcXcTAFiB1ACQ1beY'
                        
                    ])
 
        self.current_key = 0
        self.start_session()

        doc = dbp.find_last("bookings",
                            {"city":self.city}).next()
        self.last_time = doc["timestamp"]
        self.last = pd.DataFrame(doc["bookings"])
       
    def log_message(self, scope, status):
        return '[{}] -> {} {}: {} {}'\
                    .format(datetime.datetime.now(),\
                            self.name,\
                            self.city,\
                            scope,\
                            status)  
   
    def start_session (self):
        print self.keys.iloc[self.current_key]
        try:
            self.gmaps = googlemaps.Client(key=self.keys.iloc[self.current_key])
            self.session_start_time = datetime.datetime.now()
            message = self.log_message("session","success")
        except:
            message = self.log_message("session","error")
        print message
 
            
    def get_directions (self, booking):

        try:
            directions_result = self.gmaps.directions\
                ([booking['start_latitude'], booking['start_longitude']],
                  [booking['end_latitude'], booking['end_longitude']],
                  mode="transit",
                  departure_time = datetime.datetime.now())
            message = self.log_message("direction_transit","success")
        except:
            message = self.log_message("direction_transit","error")
        print message
                
    def to_DB (self):
    
        dbp.insert("snapshots", 
                   {
                     "timestamp": datetime.datetime.now(),
                     "provider": self.name,
                     "city": self.city,
                     "snapshot": self.current_feed
                     }
                    )

    def run (self):
        
        while True:

            doc = dbp.find_last("bookings",
                                {"city":self.city}).next()
            self.current_time = doc["timestamp"]
            self.current = pd.DataFrame(doc["bookings"])

            if not self.current.equals(self.last):
                print self.current

            self.last = self.current
            time.sleep(10)

#Google_Manager("torino").start()