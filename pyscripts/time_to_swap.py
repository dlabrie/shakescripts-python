from modules.shakepay import *
import re

#checkIfTransactionUpdatesNeeded()
todays = todays_swappers()

speeds = {}
for swapper in todays:
    swaps = swapperTransactions(swapper)
    swaps = {key: val for key, val in sorted(swaps.items(), key = lambda item: int(item[1]["createAtUnix"]), reverse=False)}

    foundADebit=False
    foundACredit=False
    initiated=0
    returned=0
    for swap in swaps:
        if(swaps[swap]["createAtUnix"] < midnightUnix()):
            continue

        if foundACredit == True and foundADebit == False:
            break #didnt initiate

        if swaps[swap]["direction"] == "debit":
            foundADebit = True
            initiated = swaps[swap]["createAtUnix"]

        if swaps[swap]["direction"] == "credit":
            foundACredit = True
            if foundADebit == True:
                returned = swaps[swap]["createAtUnix"]

        #print(swaps[swap]["createdAt"]+" for $"+str(swaps[swap]["amount"])+" | "+swaps[swap]["note"]+" | "+swapper+" | ("+swaps[swap]["direction"]+")")
        
        if foundACredit == True and foundADebit == True:
            speeds[swapper]=(returned-initiated)
            break;

speeds = {k: v for k, v in sorted(speeds.items(), key=lambda item: item[1])}
for swapper in speeds:
    speed = speeds[swapper]
    
    printStr=""
    if round((speed-(speed%3600)) / 3600) > 0: printStr += str(round((speed-(speed%3600)) / 3600))+"h"
    if round((speed%3600-(speed%60)) / 60) / 60 > 0: printStr += str(round((speed%3600-(speed%60)) / 60))+"m"
    if round(speed % 60) > 0: printStr += str(round(speed%60))+"s"

    start = swapper[0]+swapper[1]
    end = swapper[-1]
    swapperCensored = start + (re.sub(r"[a-zA-Z0-9]","🏓", swapper[2:-1])) + end

    print(printStr+" | "+swapperCensored)
