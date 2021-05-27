import sys
from shakepay import *

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

        wallet["balance"] =  round(wallet["balance"]-5,2)
        response = sendFunds(recipient, "You pong 🏓 | #ShakingSats | Why did the gardener get a second job? He wasn't raking in enough. | DM on Discord to be removed", "5.00", wallet["id"])
        print(response.text)
    print("")