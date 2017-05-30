# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 15:53:56 2016

@author: robin
"""
import EconomyManager
import MilitaryManager
import MemoryManager

def adminLogin():
    print("not implemented jet") #placeholder

def displayBD():
    print(MemoryManager.getDatabase())
    
if __name__ == "__main__":
    adminLogin()
    while True:
        command = input('Enter command:')
        if (command == "readDB"):
            displayBD();