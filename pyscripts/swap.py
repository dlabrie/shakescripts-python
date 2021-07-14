import sys
from modules.shakepay import *
from modules.labrie import *
import time

wallet = getCADWallet()
todays = todays_swappers()

checkIfTransactionUpdatesNeeded()

count = 0
for i in sys.argv:
    if i=="swap.py": 
        continue
    recipient = i.lower()

    if count % 10 == 9 :
        todays = todays_swappers()

    count+=1

    if recipient in todays:
        print("-- You swapped with",recipient,"already");
    else:
        if wallet["balance"] > 5:
            print("Looks we got $"+str(wallet["balance"])," in the wallet, we're good")
        else:
            while True:
                wallet = getCADWallet()
                if wallet["balance"] > 40:
                    checkIfTransactionUpdatesNeeded()
                    todays = todays_swappers()
                    break;
                else:
                    print("-- Don't have enough funds ($"+str(round(wallet["balance"],2))+"), will check in 60s")
                    time.sleep(60)
        
        if recipient in todays:
            print("-- You swapped with",recipient,"already");
            continue

        cInitiate = checkInitiate(recipient)
        
        if cInitiate["allow_initiate"] == 0:
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            print("It appears "+recipient+" has been added to the do not initiate list on "+cInitiate["added_time"]+" with reason: "+cInitiate["reason"])
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        else:
            if cInitiate["allow_initiate"] == 1:
                wallet["balance"] =  round(wallet["balance"]-5,2)
                response = sendFunds(recipient, "Good morning @"+recipient+", please return this fiver 🏓 | #ShakingSats | You know what 50 cent did when he got hungry? 58 | DM on discord to be removed.", "5.00", wallet["id"])
                print(response.text)
                time.sleep(2)
    print("")