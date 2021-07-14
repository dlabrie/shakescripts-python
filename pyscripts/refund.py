from modules.shakepay import *
from modules.labrie import checkReturn, ping
import time
import datetime

counter = 0
while True:
    
    print("\n--- "+str(datetime.datetime.now()))
    if counter % 20 == 0:
        print("+++ pinged swap.labrie.ca")
        ping()
        counter = 0
    counter+=1

    updateTransactions()
    swaps = all_swaps()
    wallet = getCADWallet()
    balance = wallet["balance"]

    for swapper in swaps:
        if swaps[swapper] == 5.00:
            if balance < 5:
                print("/!\\ Not enough funds")
                break

            creturn = checkReturn(swapper)
            
            if creturn["allow_return"] == 0:
                print("/!\\ "+swapper+" is on the do not return list on "+creturn["added_time"]+" with reason: "+creturn["reason"])
            else:
                if creturn["allow_return"] == 1:
                    print("-- Sending $5 to "+ swapper)
                    balance -= 5.0
                    response = sendFunds(swapper, "Thanks for swapping with domi167 swapbot @"+swapper+" 🏓", str(swaps[swapper]), wallet["id"])
                    print(response.text)

        elif swaps[swapper] > 0:
            print("/!\\ Won't return $"+str(round(swaps[swapper], 2))+" to "+swapper," - out of range" )

    time.sleep(10)

