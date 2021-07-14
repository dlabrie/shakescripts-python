from modules.shakepay import *

checkIfTransactionUpdatesNeeded()
todays = todays_swappers()

speeds = {}
for swapper in todays:
    swaps = swapperTransactions(swapper)
    swaps = {key: val for key, val in sorted(swaps.items(), key = lambda item: int(item[1]["createAtUnix"]), reverse=False)}

    foundADebit=False
    foundACredit=False
    returned=0
    for swap in swaps:
        if(swaps[swap]["createAtUnix"] < midnightUnix()):
            continue

        if foundACredit == True and foundADebit == False:
            break #didnt initiate

        if swaps[swap]["direction"] == "debit":
            foundADebit = True

        if swaps[swap]["direction"] == "credit":
            foundACredit = True
            if foundADebit == True:
                returned = swaps[swap]["createAtUnix"]

        #print(swaps[swap]["createdAt"]+" for $"+str(swaps[swap]["amount"])+" | "+swaps[swap]["note"]+" | "+swapper+" | ("+swaps[swap]["direction"]+")")
        
        if foundACredit == True and foundADebit == True:
            speeds[swapper]=returned%86400-3600*4
            break;

speeds = {k: v for k, v in sorted(speeds.items(), key=lambda item: item[1])}
for swapper in speeds:
    speed = speeds[swapper]
    
    printStr=""
    if round((speed-(speed%3600)) / 3600) > 0: printStr += str(round((speed-(speed%3600)) / 3600))+":"
    else: printStr+="0"

    if round((speed%3600-(speed%60)) / 60) / 60 > 0: printStr += str(round((speed%3600-(speed%60)) / 60))+":"
    else: printStr+="0"
    
    if round(speed % 60) > 0: printStr += str(round(speed%60)); 
    else: printStr+="0"

    print(printStr+" | "+swapper)
