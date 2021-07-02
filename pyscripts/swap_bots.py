from shakepay import *

import time
import datetime

headers =  {
    "accept": "application/json",
    "cache-control": "no-cache",
    "content-type": "application/json",
    "pragma": "no-cache",
    "user-agent": "Shakepay Bot by domi167",
}
request = requests.get("https://swap.labrie.ca/api/online-bots/", headers=headers)
onlineBots = json.loads(request.text)

updateTransactions()

wallet = getCADWallet()
balance = wallet["balance"]

todays = todays_swappers()
for recipient in onlineBots:
    print(recipient["shaketag"])

    
    if recipient["shaketag"] == getShaketag():
        continue
    if recipient["shaketag"] not in todays:
        if wallet["balance"] > 5:
            print("Looks we got $"+str(wallet["balance"])," in the wallet, we're good")
        else:
            print("-- Don't have enough funds")
            exit()

        print("Automagically sending to "+recipient["shaketag"])
        wallet["balance"] =  round(wallet["balance"]-5,2)
        response = sendFunds(recipient["shaketag"], "#ShakingSats 🏓 | Beep Boop we're bots send back to @domi167", "5.00", wallet["id"])
        print(response.text)
        time.sleep(2);
    

