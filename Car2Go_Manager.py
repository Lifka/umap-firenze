#!/usr/bin/python
import sys

def print_exception ():
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print (exc_type)
    print (exc_obj)
    print (exc_tb.tb_lineno)  

import datetime
import time

start_cols = [
        
    "start_time",
    "latitude",
    "longitude",

]

from threading import Thread

from DataBaseProxy import dbp
import pandas as pd

def pre_process (df):
    
    df["longitude"] = df.coordinates.apply(lambda x: x[0])
    df["latitude"] = df.coordinates.apply(lambda x: x[1])
    return df.drop("coordinates", axis=1)

class Car2Go_Manager (Thread):

    def __init__ (self, city):

        Thread.__init__(self)
        self.daemon = True
        
        self.name = "car2go " + city
        self.city = city

        doc = dbp.find_last("snapshots", 
                            {"provider":"car2go","city":self.city}).next()
        self.last_time = doc["timestamp"]
        self.last = pd.DataFrame(doc["snapshot"]["placemarks"]).set_index("name")
        self.last = pre_process(self.last)
        self.fleet = self.last.index

        self.active_parkings = pd.DataFrame(columns = start_cols, index=self.last.index)
        self.active_parkings["start_time"] = datetime.datetime.now()
        self.active_parkings["latitude"] = self.last.latitude
        self.active_parkings["longitude"] = self.last.longitude
        
        self.active_bookings = pd.DataFrame(columns = start_cols, index=[])        
        
    def check (self):
        
        try:
            doc = dbp.find_last("snapshots",
                                {"provider":"car2go","city":self.city}).next()
            self.current_time = doc["timestamp"]
            self.current = pd.DataFrame(doc["snapshot"]["placemarks"]).set_index("name")
            self.current = pre_process(self.current)        
        except:
            print ("Exception in " + self.name)
            print_exception()
            
        if not self.current.equals(self.last):

            # Detect new cars
#                print "Fleet"
#                print self.fleet.shape
            self.new_cars = self.current.index.difference(self.fleet)
#                print self.new_cars.shape

            # Indexes creation
#                print "Status"                
            self.still_parked = self.fleet.intersection(self.current.index)
            self.just_booked = self.active_parkings.index.difference(self.current.index).intersection(self.fleet)
            self.just_parked = self.current.index.intersection(self.fleet).difference(self.active_parkings.index)
#                print self.still_parked.shape
#                print self.just_booked.shape
#                print self.just_parked.shape
                            
            # - New parkings
            self.active_parkings = pd.concat([self.active_parkings, pd.DataFrame(index=self.just_parked)])
            self.active_parkings.loc[self.just_parked, "start_time"] = \
                                  self.current_time
            self.active_parkings.loc[self.just_parked,"latitude"] = \
                                  self.current.loc[self.just_parked, "latitude"].values
            self.active_parkings.loc[self.just_parked,"longitude"] = \
                                  self.current.loc[self.just_parked, "longitude"].values
            
            # - New bookings  
            self.active_bookings = pd.concat([self.active_bookings, pd.DataFrame(index=self.just_booked)])                
            self.active_bookings.loc[self.just_booked, "start_time"] = \
                                  self.current_time
            self.active_bookings.loc[self.just_booked,"latitude"] = \
                                  self.active_parkings.loc[self.just_booked, "latitude"].values
            self.active_bookings.loc[self.just_booked,"longitude"] = \
                                  self.active_parkings.loc[self.just_booked, "longitude"].values

            # - Parkings terminated
            def record_parking(parkings):
                parkings["end_time"] = datetime.datetime.now()
                recorded = parkings.T.to_dict()
                if len(recorded.keys()):
                    record = {
                            "provider":"car2go",
                            "city":self.city,
                            "timestamp":datetime.datetime.now(),
                            "parkings":recorded
                            }
                    dbp.insert("parkings", record)
            record_parking(self.active_parkings.loc[self.just_booked])
            self.active_parkings.drop(self.just_booked, inplace=True)
            
            self.last = self.current
            self.last_time = self.current_time

            # - Bookings terminated
            def record_booking(bookings):
                bookings["end_time"] = datetime.datetime.now()
                bookings["end_latitude"] = self.current.loc[bookings.index, "latitude"].values
                bookings["end_longitude"] = self.current.loc[bookings.index, "longitude"].values
                recorded = bookings.T.to_dict()
                if len(recorded.keys()):
                    record = {
                            "provider":"car2go",
                            "city":self.city,
                            "timestamp":datetime.datetime.now(),
                            "bookings":recorded
                            }
                    dbp.insert("bookings", record)
            record_booking(self.active_bookings.loc[self.just_parked.intersection(self.active_bookings.index)])
            self.active_bookings.drop(self.just_parked.intersection(self.active_bookings.index), inplace=True)

            # - Update fleet
            self.fleet = self.fleet.union(self.current.index)
#                print self.fleet.shape
        
manager = Car2Go_Manager("Firenze")
while True:
    manager.check()
    time.sleep(10)
