from shakepay import *

updateTransactions()

swaps = all_swaps()

swapsSummary = {}
for swapper in swaps:
    if swaps[swapper] != 0:
        transactions = swapperTransactions(swapper)
        lastTransaction = list(transactions.keys())[0]
        swapsSummary[lastTransaction] = {"createdAtUnix":transactions[lastTransaction]["createAtUnix"] ,"transaction":transactions[lastTransaction], "swapper":swapper, "balance":swaps[swapper]}


swapsSummary = {key: val for key, val in sorted(swapsSummary.items(), key = lambda item: int(item[1]["createdAtUnix"]), reverse=True)}

print("\n------------ You owe these people ------------")
for transaction in swapsSummary:
    if swapsSummary[transaction]["balance"] > 0.1:
        print(swapsSummary[transaction]["transaction"]["createdAt"]+" for $"+str(swapsSummary[transaction]["transaction"]["amount"])+" | "+ swapsSummary[transaction]["transaction"]["direction"]+" | "+swapsSummary[transaction]["transaction"]["note"]+" |", swapsSummary[transaction]["swapper"], "|", swapsSummary[transaction]["balance"])


print("\n\n------------ These people owe you ------------")
for transaction in swapsSummary:
    if swapsSummary[transaction]["balance"] < -0.1:
        print(swapsSummary[transaction]["transaction"]["createdAt"]+" for $"+str(swapsSummary[transaction]["transaction"]["amount"])+" | "+ swapsSummary[transaction]["transaction"]["direction"]+" | "+swapsSummary[transaction]["transaction"]["note"]+" |", swapsSummary[transaction]["swapper"], "|", swapsSummary[transaction]["balance"])


badgeSwappers = badge_swappers()
print("\n\n------------ Stats ------------")
print("You've swapped with "+str(len(badgeSwappers.keys()))+" different friends since May 3rd 🏓")
print("You've swapped with "+str(len(swaps.keys()))+" different friends since the beginning🏓")

print("\n")

