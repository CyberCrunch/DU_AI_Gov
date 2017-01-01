# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 18:19:15 2016

@author: robin
"""

import requests
import json



def setupEnjin():
    print("not implemented jet") #placeholder
    


def main(): #connection test
    url = "http://www.vulturecorporation.com/api"   #/jsonrpc
    headers = {'content-type': 'application/json'}

    # Example echo method
    payload = {
        "method":"Shop.get",
        "params":{
        	"api_key": "1a2a3a4a5a6a7a8a9a1b2b3b4b5b6b7b8b9b1c2c3c4c5c6c",
        	"preset_id": "12345678"
        },        
        "jsonrpc": "2.0",
        "id": 0
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()

    assert response["result"] # == "echome!"
    assert response["jsonrpc"]
    assert response["id"] == 0

if __name__ == "__main__":
    main()