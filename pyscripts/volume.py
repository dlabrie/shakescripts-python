from shakepay import *

transactionsCache = getTransactionsCache()
transactions = {key: val for key, val in sorted(transactionsCache["data"].items(), key = lambda item: int(item[1]["createAtUnix"]), reverse=True)}

volumeBalanceSent = 0
volumeBalanceReceived = 0

for transaction in transactions:
    if transactions[transaction]["direction"] == "credit":
        volumeBalanceReceived += round(float(transactions[transaction]["amount"]), 2)

    if transactions[transaction]["direction"] == "debit":
        volumeBalanceSent += round(float(transactions[transaction]["amount"]), 2)


print("You've received: $"+str(round(volumeBalanceReceived,2)))
print("You've sent: $"+str(round(volumeBalanceSent,2)))
print("For a total of $"+str(round(volumeBalanceReceived+volumeBalanceSent,2)))