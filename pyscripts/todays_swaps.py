from modules.shakepay import *

updateTransactions()

swaps = todays_swappers()

print("\n\n------------ All swap summaries ------------")
swapsSummary = {}
for swapper in swaps:
    transactions = swapperTransactions(swapper)
    lastTransaction = list(transactions.keys())[0]
    swapsSummary[lastTransaction] = {"createdAtUnix":transactions[lastTransaction]["createAtUnix"] ,"transaction":transactions[lastTransaction], "swapper":swapper}

swapsSummary = {key: val for key, val in sorted(swapsSummary.items(), key = lambda item: int(item[1]["createdAtUnix"]), reverse=True)}

for transaction in swapsSummary:
    print(swapsSummary[transaction]["transaction"]["createdAt"]+" for $"+str(swapsSummary[transaction]["transaction"]["amount"])+" | "+ swapsSummary[transaction]["transaction"]["direction"]+" | "+swapsSummary[transaction]["transaction"]["note"]+" |", swapsSummary[transaction]["swapper"])
    #print(swapsSummary[transaction]["transaction"]["createdAt"]+" for $"+str(swapsSummary[transaction]["transaction"]["amount"])+" | "+ swapsSummary[transaction]["transaction"]["direction"]+" | "+swapsSummary[transaction]["transaction"]["note"])


badgeSwappers = badge_swappers()
print("\n\n------------ Stats ------------")
print("You've swapped with "+str(len(swaps.keys()))+" different steaks 🥩 🏓")

print("\n")

