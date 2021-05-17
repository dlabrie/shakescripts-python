from getpass import getpass

import datetime
import calendar
import requests
import uuid
import json
import pytz

def getUUID():
    fakeUUID = ""
    ## Generate a unique device id if needed
    try:
        f = open(".uuid", "r")
        fakeUUID = f.read()
        f.close()
    except:
        f = open(".uuid", "w")
        fakeUUID = str(uuid.uuid4())
        f.write(fakeUUID.upper())
        f.close()

    if fakeUUID == "":
        f = open(".uuid", "w")
        fakeUUID = str(uuid.uuid4())
        f.write(fakeUUID.upper())
        f.close()
  
    return fakeUUID.upper()

def saveJWT(jwt):
    f = open(".jwtToken", "w")
    f.write(jwt)
    f.close()

def getJWT():
    jwt = ""
    try:
        f = open(".jwtToken", 'r')
        jwt = f.read()
        f.close()
    except IOError:
        print("Please login by using python3 login.py first.")
        f.close()
        exit()

    return jwt

def shakepayAPIAuth(shakepayUsername, shakepayPassword):
    print("Calling Shakepay API Endpoint using POST /authentication")
    headers =  {
        "accept": "application/json",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "pragma": "no-cache",
        "user-agent": "Shakepay App v1.6.96 (16096) on Apple iPhone (iOS 14.5)",
        "x-device-mac-address": "02:00:00:00:00:00",
        "x-device-ip-address": "10.69.4.20",
        "x-device-unique-id": getUUID(),
    }
    credentials =  {"strategy":"local","username":shakepayUsername,"password":shakepayPassword}
    return requests.post("https://api.shakepay.com/authentication", json=credentials, headers=headers) 

def shakepayAPIPost(endpoint, jsonData):
    print("Calling Shakepay API Endpoint using POST "+endpoint)
    headers =  {
        "authorization": getJWT(),
        "accept": "application/json",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "pragma": "no-cache",
        "user-agent": "Shakepay App v1.6.96 (16096) on Apple iPhone (iOS 14.5)",
        "x-device-mac-address": "02:00:00:00:00:00",
        "x-device-ip-address": "10.69.4.20",
        "x-device-unique-id": getUUID(),
    }
    return requests.post("https://api.shakepay.com"+endpoint, json=jsonData, headers=headers) 

def shakepayAPIGet(endpoint):
    print("Calling Shakepay API Endpoint using GET "+endpoint)
    headers =  {
        "authorization": getJWT(),
        "accept": "application/json",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "pragma": "no-cache",
        "user-agent": "Shakepay App v1.6.96 (16096) on Apple iPhone (iOS 14.5)",
        "x-device-mac-address": "02:00:00:00:00:00",
        "x-device-ip-address": "10.69.4.20",
        "x-device-unique-id": getUUID(),
    }
    return requests.get("https://api.shakepay.com"+endpoint, headers=headers) 

def saveTransactionsCache(transactions):
    f = open(".transactions", "w")

    date = datetime.datetime.utcnow()
    unixDate = calendar.timegm(date.utctimetuple())
    transactions = { "lastPull":unixDate, "data":transactions }
    f.write(json.dumps(transactions))
    f.close()

def getTransactionsCache():
    transactions = '{ "lastPull":0, "data":{} }'
    try:
        f = open(".transactions", 'r')
        transactions = f.read()
        if transactions == "":
            transactions = '{ "lastPull":0, "data":{} }'
    except IOError:
        f = open(".transactions", 'w')
        f.write(transactions)
    f.close()

    transactionsJson = json.loads(transactions)
    return transactionsJson

def pullTransactions(page):
    if page == 1:
        body = {"filterParams":{"currencies":["CAD"]}}
    else:
        body =  {"pagination":{"descending":True,"rowsPerPage":200,"page":page}, "filterParams":{}}

    print("Will pull transactions page "+str(page), body)

    return shakepayAPIPost("/transactions/history", body)

def updateTransactions():
    page = 1
    transactionsCache = getTransactionsCache()
    transactions = transactionsCache["data"]

    while True:
        addedTransactions = 0
        foundExistingTransaction = 0
        foundStart = False
        transactionCounter = 0

        newTransactionsResponse = pullTransactions(page)
        newTransactions = json.loads(newTransactionsResponse.text)

        for transaction in newTransactions["data"]:
            transactionCounter+=1
            # check if already in ledger
            if transaction["transactionId"] in transactions:
                foundExistingTransaction += 1
                continue

            if transaction["type"]!="peer": 
                continue
            if transaction["currency"]!="CAD": 
                continue

            date = datetime.datetime.strptime(transaction["createdAt"].replace("Z","UTC"), "%Y-%m-%dT%H:%M:%S.%f%Z")
            createAtUnix = calendar.timegm(date.utctimetuple())
            if createAtUnix < 1618963200:
                foundExistingTransaction += 1
                foundStart = True
                break

            addedTransactions += 1
            transaction["createAtUnix"] = createAtUnix
            transactions[transaction["transactionId"]] = transaction
    
        print("checked "+str(transactionCounter)+" from this pull")

        if transactionCounter != 200:
            print("got less than 200 transactions, reached the end?")
            break;

        if foundExistingTransaction > 10:
            print("found more than 10 transactions, no need to proceed")
            break;

        page += 1

    if addedTransactions > 0:
        saveTransactionsCache(transactions)

def checkIfTransactionUpdatesNeeded():
    transactionsCache = getTransactionsCache()
    lastPull = transactionsCache["lastPull"]

    date = datetime.datetime.utcnow()
    unixDate = calendar.timegm(date.utctimetuple())

    if unixDate-600 > lastPull:
        print("Haven't pulled transactions in over 5 minutes.")
        updateTransactions()
    

def all_swaps():
    transactionsCache = getTransactionsCache()
    transactions = {key: val for key, val in sorted(transactionsCache["data"].items(), key = lambda item: int(item[1]["createAtUnix"]), reverse=True)}

    swapperBalance = {}

    # Adjustements for donations
    swapperBalance["someoneqc"] = -9.01

    swapperBalance["woblz"] = -0.01
    swapperBalance["cannacaged"] = -0.01
    swapperBalance["mstaxidrvr2"] = -0.01
    swapperBalance["cdcrawford"] = 50.00

    # Adjustements for people I gave money to
    swapperBalance["hydra"] = 4.2
    swapperBalance["ddcazes"] = 0.69

    # scummers
    #swapperBalance["kingdesigner187"] = 4.90
    swapperBalance["tammyz"] = 4.90
    swapperBalance["danielcrypto"] = 4.90
    swapperBalance["michaelday"] = 4.90
    swapperBalance["joshduerksen"] = 4.90
    swapperBalance["moneyburner"] = 4.90

    #fuck ups
    swapperBalance["wills"] = 4.90
    swapperBalance["kiks"] = 4.90

    for transaction in transactions:
        if transactions[transaction]["direction"] == "credit":
            swapper = transactions[transaction]["from"]["label"].replace("@","");
            if swapper not in swapperBalance:
                swapperBalance[swapper]=0
            swapperBalance[swapper] += round(float(transactions[transaction]["amount"]), 2)

        if transactions[transaction]["direction"] == "debit":
            swapper = transactions[transaction]["to"]["label"].replace("@","");
            if swapper not in swapperBalance:
                swapperBalance[swapper]=0
            swapperBalance[swapper] -= round(float(transactions[transaction]["amount"]), 2)

    for swapper in swapperBalance:
        swapperBalance[swapper] = round(swapperBalance[swapper], 2)

    return swapperBalance

def todays_swappers():
    transactionsCache = getTransactionsCache()
    transactions = {key: val for key, val in sorted(transactionsCache["data"].items(), key = lambda item: int(item[1]["createAtUnix"]), reverse=True)}

    swapperBalance = {}

    for transaction in transactions:

        date = datetime.datetime.strptime(transactions[transaction]["createdAt"].replace("Z","UTC"), "%Y-%m-%dT%H:%M:%S.%f%Z")
        createAtUnix = calendar.timegm(date.utctimetuple())

        if createAtUnix < midnightUnix():
            continue

        if transactions[transaction]["direction"] == "credit":
            swapper = transactions[transaction]["from"]["label"].replace("@","");
            if swapper not in swapperBalance:
                swapperBalance[swapper]=0

        if transactions[transaction]["direction"] == "debit":
            swapper = transactions[transaction]["to"]["label"].replace("@","");
            if swapper not in swapperBalance:
                swapperBalance[swapper]=0

    return swapperBalance

def todays_swappers():
    transactionsCache = getTransactionsCache()
    transactions = {key: val for key, val in sorted(transactionsCache["data"].items(), key = lambda item: int(item[1]["createAtUnix"]), reverse=True)}

    swapperBalance = {}

    for transaction in transactions:

        date = datetime.datetime.strptime(transactions[transaction]["createdAt"].replace("Z","UTC"), "%Y-%m-%dT%H:%M:%S.%f%Z")
        createAtUnix = calendar.timegm(date.utctimetuple())

        if createAtUnix < midnightUnix():
            continue

        if transactions[transaction]["direction"] == "credit":
            swapper = transactions[transaction]["from"]["label"].replace("@","");
            if swapper not in swapperBalance:
                swapperBalance[swapper]=0

        if transactions[transaction]["direction"] == "debit":
            swapper = transactions[transaction]["to"]["label"].replace("@","");
            if swapper not in swapperBalance:
                swapperBalance[swapper]=0

    return swapperBalance

def badge_swappers():
    transactionsCache = getTransactionsCache()
    transactions = {key: val for key, val in sorted(transactionsCache["data"].items(), key = lambda item: int(item[1]["createAtUnix"]), reverse=True)}

    swapperBalance = {}

    for transaction in transactions:

        date = datetime.datetime.strptime(transactions[transaction]["createdAt"].replace("Z","UTC"), "%Y-%m-%dT%H:%M:%S.%f%Z")
        createAtUnix = calendar.timegm(date.utctimetuple())

        if createAtUnix < 1620014400: # may 3rd
            continue

        if transactions[transaction]["direction"] == "credit":
            swapper = transactions[transaction]["from"]["label"].replace("@","");
            if swapper not in swapperBalance:
                swapperBalance[swapper]=0

        if transactions[transaction]["direction"] == "debit":
            swapper = transactions[transaction]["to"]["label"].replace("@","");
            if swapper not in swapperBalance:
                swapperBalance[swapper]=0

    return swapperBalance

def swapperTransactions(swapperLookup):
    transactionsCache = getTransactionsCache()
    transactions = {key: val for key, val in sorted(transactionsCache["data"].items(), key = lambda item: int(item[1]["createAtUnix"]), reverse=True)}

    swapperTransaction = {}

    for transaction in transactions:

        if transactions[transaction]["direction"] == "credit":
            swapper = transactions[transaction]["from"]["label"].replace("@","");

        if transactions[transaction]["direction"] == "debit":
            swapper = transactions[transaction]["to"]["label"].replace("@","");

        if swapper == swapperLookup:
            swapperTransaction[transaction] = transactions[transaction]

    return swapperTransaction

def midnightUnix():
    return calendar.timegm(datetime.datetime.now(pytz.timezone("America/Montreal")) \
            .replace(hour=0, minute=0, second=0, microsecond=0) \
            .astimezone(pytz.utc) \
            .utctimetuple())

def getCADWallet():
    walletResponse = shakepayAPIGet("/wallets")
    wallets = json.loads(walletResponse.text)["data"]
    for wallet in wallets:
        if wallet["currency"] == "CAD":
            return wallet

def sendFunds(recipient, note, amount, wallet):
    print("Sending",recipient,"$"+str(amount),"with the note:",note)
    body = {"amount": amount,"fromWallet": wallet,"note": note,"to": recipient,"toType": "user"}
    return shakepayAPIPost("/transactions", body)

def shakingSats():
    return shakepayAPIPost("/shaking-sats", {})