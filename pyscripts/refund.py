from shakepay import *
from labrie import checkReturn
import time
import datetime

while True:
    updateTransactions()
    swaps = all_swaps()
    wallet = getCADWallet()
    balance = wallet["balance"]

    print("------------ You owe these people ------------")
    for swapper in swaps:
        if swaps[swapper] >= 1:
            print(swapper, round(swaps[swapper], 2))
    print("")

    for swapper in swaps:
        if swaps[swapper] == 5.00:
            if balance < 5:
                print("Not enough funds")
                break

            creturn = checkReturn(swapper)
            print(creturn)
            
            if creturn["allow_return"] == 0:
                print("It appears "+swapper+" has been added to the do not return list on "+creturn["added_time"]+" with reason: "+creturn["reason"])
            else:
                if creturn["allow_return"] == 1:
                    print("sending $5 to "+ swapper)
                    balance -= 5.0
                    response = sendFunds(swapper, "Thanks for swapping with domi167 swapbot @"+swapper+" 🏓", "5.00", wallet["id"])
                    print(response.text)

        elif swaps[swapper] > 1:
            print("This swap is out of range for this script ($", round(swaps[swapper], 2), swapper,")" )

    print("\nsleeping\n"+str(datetime.datetime.now()))
    time.sleep(2)

