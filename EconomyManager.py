# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 19:37:31 2016

@author: robin
"""

import json
import machine_learning_test



def getJob(msg):
    with open('memoryDB.json', 'r+') as json_file:
        json_data = json.load(json_file)
        job = json_data[msg][1]
        if((job == "Miner")and(json_data["cityone"][6]!=0)):
            json_data[msg][2] = "working"
            json_data[msg][3] = "Sector A3"
            output = "You are now assigned to Sector A3 for mining " + json_data["cityone"][5] + " minerals. You will receave "+str(json_data["cityone"][6])+" Credits if successfull."
        elif(job == "Builder"):
            json_data[msg][2] = "working"
            json_data[msg][3] = "Sector C8"
            output = "You are now assigned to Sector C8 for building an automatic defence turret. You will receave "+str(json_data["cityone"][6])+" Credits if successfull."
        else:
            output = "There are currently no jobs available for your profession, please standby."
        json_file.seek(0, 0)
        json_file.write(json.dumps(json_data, indent=4))
        json_file.truncate()
    return (output)
    
def reportJob(msg):
    splitStr = msg.split()
    if(len(splitStr) != 2):
        return "Invalid Parameters, please use Format: !repj name statusreport"
    if(splitStr[1] == "success"):
        with open('memoryDB.json', 'r+') as json_file:
            json_data = json.load(json_file)
            json_data[splitStr[0]][2] = "idle"
            json_data[splitStr[0]][3] = "unknownPos"
            json_data[splitStr[0]][4] = json_data[splitStr[0]][4] + json_data["cityone"][6]
            json_data["cityone"][6] = 0
            json_file.seek(0, 0)
            json_file.write(json.dumps(json_data, indent=4))
            json_file.truncate()
        return ("Thanks for your contribution. You now have " + str(json_data[splitStr[0]][4]) + " credits")
    return ("Your report will be analyzed.") #placeholder!

    
def setDemand(msg):
    splitStr = msg.split()
    if(len(splitStr) != 3):
        return "Invalid Parameters, please use Format: !setd location needs price"
    with open('memoryDB.json', 'r+') as json_file:
        json_data = json.load(json_file)
        json_data[splitStr[0]][5] = splitStr[1]
        json_data[splitStr[0]][6] = int(splitStr[2])
        json_file.seek(0, 0)
        json_file.write(json.dumps(json_data, indent=4))
        json_file.truncate()
    return ("A new demand for " + splitStr[1] + " has been created.")
