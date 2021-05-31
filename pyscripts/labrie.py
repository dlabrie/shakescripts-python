import requests
import json
from shakepay import getUUID

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

def checkReturn(shaketag):
    headers =  {
        "accept": "application/json",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "pragma": "no-cache",
        "user-agent": "Shakepay Bot by domi167",
    }
    data =  {"source":getUUID(),"shaketag":shaketag,"step":"return"}
    request = requests.post("https://swap.labrie.ca/api/", json=data, headers=headers)
    return json.loads(request.text)["data"]
