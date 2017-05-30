# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 15:52:43 2016

@author: robin
"""

import json


from enum import Enum #testing possible enums for readability...(not implemeted)
class NrH(Enum): #human data formtat for Json
    name = 0
    human = 1
    job = 2
    status = 3
    position = 4
    money = 5
class NrL(Enum): #location data formtat for Json
    name = 0
    location = 1
    planet = 2
    structure = 3
    longitude = 4
    latitude = 5
    resource = 6
    reward = 7
class SpH(Enum): #human string formtat for registration
    name = 0
    job = 1
class SpL(Enum): #location string formtat for registration
    name = 0
    planet = 1
    structure = 2
    longitude = 3
    latitude = 4
    
def regHuman(msg):
    splitStr = msg.split()
    if(len(splitStr) != 2):
        return "Invalid Parameters, please use Format: !reg YourName YourJob"
    with open('memoryDB.json', 'r+') as json_file:
        json_data = json.load(json_file)
        json_data[splitStr[SpH.name.value]] = ['Human', splitStr[SpH.job.value],"idle", "unknownPos", 0]
        json_file.seek(0, 0)
        json_file.write(json.dumps(json_data, indent=4))
        json_file.truncate()
    return ("New human registered: " +msg)

def regLocation(msg):
    splitStr = msg.split()
    if(len(splitStr) != 5):
        return ("Invalid Parameters, please use Format: !geodata name planet type longitude latitude")
    with open('memoryDB.json', 'r+') as json_file:
        json_data = json.load(json_file)
        json_data[splitStr[SpL.name.value]] = ['Location', splitStr[SpL.planet.value], splitStr[SpL.structure.value], splitStr[SpL.longitude.value], splitStr[SpL.latitude.value], "default", 0]
        json_file.seek(0, 0)
        json_file.write(json.dumps(json_data, indent=4))
        json_file.truncate()
    return ("New location registered: " +msg)
    
def getDatabase():
    with open('memoryDB.json', 'r') as json_file:
        json_data = json.load(json_file)
    return(json.dumps(json_data, indent=4, sort_keys=True))