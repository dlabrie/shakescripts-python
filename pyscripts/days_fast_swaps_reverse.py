from modules.shakepay import *
import re
import sys
import datetime

n = int(sys.argv[1])
days_swaps = days_swappers(n)
speeds = {}

swapperDaySwaps = {}

for swapper in days_swaps:
    swapperDaySwaps[swapper] = {}
    
    swaps = swapperTransactions(swapper)
    swaps = {key: val for key, val in sorted(swaps.items(), key = lambda item: int(item[1]["createAtUnix"]), reverse=False)}

    for swap in swaps:
        if(swaps[swap]["createAtUnix"] < midnightUnix()-(86400*n)):
            continue

        date = datetime.datetime.strptime(swaps[swap]["createdAt"].replace("Z","UTC"), "%Y-%m-%dT%H:%M:%S.%f%Z")
        dateStr = str(date.year)+"-"+str(date.month)+"-"+str(date.day)
        
        if dateStr not in swapperDaySwaps[swapper]:
            swapperDaySwaps[swapper][dateStr] = {}

        swapperDaySwaps[swapper][dateStr][swap]=swaps[swap]

for swapper in swapperDaySwaps:
    speeds[swapper] = {}
    for transactionInADay in swapperDaySwaps[swapper]:
        foundADebit=False
        foundACredit=False
        received=0
        returned=0

        swapperDaySwaps[swapper][transactionInADay] = {key: val for key, val in sorted(swapperDaySwaps[swapper][transactionInADay].items(), key = lambda item: int(item[1]["createAtUnix"]), reverse=False)}

        for transaction in swapperDaySwaps[swapper][transactionInADay]:
            swap = swapperDaySwaps[swapper][transactionInADay][transaction]
            
            if foundACredit == False and foundADebit == True:
                break #didnt return

            if swap["direction"] == "credit":
                foundACredit = True
                received = swap["createAtUnix"]

            if swap["direction"] == "debit" and foundACredit == True:
                foundADebit = True
                returned = swap["createAtUnix"]
            
            print(swap["direction"]+" "+str(foundACredit)+" "+str(foundADebit)+" "+str(swap["createAtUnix"]))
            
            if foundACredit == True and foundADebit == True:
                speeds[swapper][transactionInADay]=(returned-received)
                break;

for swapper in speeds:
    if len(speeds[swapper].items()) > 0:
        avg = round(sum(speeds[swapper].values())/len(speeds[swapper].items()))
        speeds[swapper]["avg"] = avg
    if len(speeds[swapper].items()) == 0:
        speeds[swapper]["avg"] = 99999999999999999

speeds = {k: v for k, v in sorted(speeds.items(), key=lambda item: item[1]["avg"])}
for swapper in speeds:
    speed = speeds[swapper]["avg"]
    
    if speed == 99999999999999999:
        continue

    printStr=""
    if round((speed-(speed%3600)) / 3600) > 0: printStr += str(round((speed-(speed%3600)) / 3600))+"h"
    if round((speed%3600-(speed%60)) / 60) / 60 > 0: printStr += str(round((speed%3600-(speed%60)) / 60))+"m"
    if round(speed % 60) > 0: printStr += str(round(speed%60))+"s"

    start = swapper[0]+swapper[1]
    end = swapper[-1]
    swapperCensored = start + (re.sub(r"[a-zA-Z0-9]","🏓", swapper[2:-1])) + end

    print(swapper + " | avg is " + printStr + " | "+str(speeds[swapper]))