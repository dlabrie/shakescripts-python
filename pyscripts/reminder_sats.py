from modules.shakepay import *
import time

updateTransactions()
swaps = all_swaps()
wallet = getBTCWallet()
balance = wallet["balance"]

for swapper in swaps:
    if swaps[swapper] < -1.00:
        transactions = swapperTransactions(swapper)
        lastTransaction = list(transactions.keys())[0]
        if transactions[lastTransaction]["createAtUnix"] > midnightUnix():
            continue

        swaps[swapper] *= -1

        print("-- Reminding "+swapper+" about $"+str(round(swaps[swapper], 2)))
        balance -= 0.00000001
        response = sendFunds(swapper, "Hi "+swapper+", please send back the $"+str(round(swaps[swapper], 2))+" 🏓", "0.00000001", wallet["id"])
        print(response.text)
        time.sleep(2)
    elif swaps[swapper] < 0:
        swaps[swapper] *= -1
        print("/!\\ Won't remind "+swapper+" about $"+str(round(swaps[swapper], 2))+" - out of range" )



