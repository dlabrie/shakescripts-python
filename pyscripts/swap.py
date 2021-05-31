import sys
from shakepay import *
from labrie import *

wallet = getCADWallet()

checkIfTransactionUpdatesNeeded()

for i in sys.argv:
    if i=="swap.py": 
        continue
    recipient = i.lower()

    todays = todays_swappers()

    if recipient in todays:
        print("-- You swapped with",recipient,"already");
    else:
        if wallet["balance"] > 5:
            print("Looks we got $"+str(wallet["balance"])," in the wallet, we're good")
        else:
            print("-- Don't have enough funds")
            exit()

        cInitiate = checkInitiate(recipient)
        print(cInitiate)
        
        if cInitiate["allow_initiate"] == 0:
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            print("It appears "+recipient+" has been added to the do not initiate list on "+cInitiate["added_time"]+" with reason: "+cInitiate["reason"])
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        else:
            if cInitiate["allow_initiate"] == 1:
                wallet["balance"] =  round(wallet["balance"]-5,2)
                #response = sendFunds(recipient, "You pong 🏓 | #ShakingSats | JOKE: I took a job as the head of Old McDonald's farm. I'm the CIEIO. | DM on Discord to be removed", "5.00", wallet["id"])
                #print(response.text)
    print("")