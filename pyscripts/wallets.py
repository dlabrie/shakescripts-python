import sys
from modules.shakepay import *

wallets = getWallets()
print("")
for wallet in wallets:
    if wallet["currency"] == "CAD":
        print("You have $"+str(wallet["balance"])+" Canadian Rupees")
    if wallet["currency"] == "ETH":
        print("You have "+str(wallet["balance"])+" ETH worth $"+str(round(float(wallet["fiatBalance"]),2))+" Canadian Rupees")
    if wallet["currency"] == "BTC":
        print("You have "+str(wallet["balance"])+" BTC worth $"+str(round(float(wallet["fiatBalance"]),2))+" Canadian Rupees")
        
print("")