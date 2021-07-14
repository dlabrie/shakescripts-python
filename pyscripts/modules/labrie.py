import requests
import json
import time
from shakepay import *

def checkInitiate(shaketag):
    headers =  {
        "accept": "application/json",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "pragma": "no-cache",
        "user-agent": "Shakepay Bot by domi167",
    }
    data =  {"source":getUUID(),"shaketag":shaketag,"step":"initiate"}
    request = requests.post("https://swap.labrie.ca/api/", json=data, headers=headers)
    return json.loads(request.text)["data"]

returnCache = {} 
def checkReturn(shaketag):
    global returnCache

    refreshCache = True
    if shaketag in returnCache:
        if returnCache[shaketag]["time"] > time.time()-1800:
            refreshCache = False

    if refreshCache == True:
        headers =  {
            "accept": "application/json",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "pragma": "no-cache",
            "user-agent": "Shakepay Bot by domi167",
        }
        data =  {"source":getUUID(),"shaketag":shaketag,"step":"return"}
        request = requests.post("https://swap.labrie.ca/api/", json=data, headers=headers)
        returnCache[shaketag] = {
            "time": time.time(),
            "data": json.loads(request.text)["data"],
        }
    
    return returnCache[shaketag]["data"]

def ping():
    headers =  {
        "accept": "application/json",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "pragma": "no-cache",
        "user-agent": "Shakepay Bot by domi167",
    }
    data = {
        "guid": getUUID(),
        "shaketag":getShaketag(),
        "metadata": getWaitlistStats(),
    }
    request = requests.post("https://swap.labrie.ca/api/ping/", json=data, headers=headers)
    return json.loads(request.text)
