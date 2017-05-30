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
    url = "http://localhost:4000/jsonrpc"
    #url = "http://www.vulturecorporation.com/api"
    headers = {'content-type': 'application/json'}

    # Example echo method
    payload = {
        "method":"SiteWall.postMessage",
        "params":{
                  "api_key": "1a2a3a4a5a6a7a8a9a1b2b3b4b5b6b7b8b9b1c2c3c4c5c6c",
                  "preset_id": "12345678",
                  "wall_site_id": 123,
                  "post_type": "type?",
                  "message": "this is an AI testmessage"
#                  "access": [string] [optional]
#                  "embed_url": [string] [optional]
#                  "embed_title": [string] [optional]
#                  "embed_description": [string] [optional]
#                  "embed_disable_thumbnail": [string] [optional]
#                  "embed_video_title": [string] [optional]
#                  "embed_video_description": [string] [optional]
        },        
        "jsonrpc": "2.0",
        "id": 0
    }
    payload2 = {
        "method": "echo",
        "params": ["echome!"],
        "jsonrpc": "2.0",
        "id": 0,
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()

    #assert response["result"]  == "echome!"
    assert response["jsonrpc"]
    assert response["id"] == 0
    print("yay")

if __name__ == "__main__":
    main()