from getpass import getpass

import datetime
import calendar
import requests
import uuid
import json
import pytz
import csv
import time
import jwt

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
    #print("Calling Shakepay API Endpoint using POST /authentication")
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
    try:
        return requests.post("https://api.shakepay.com/authentication", json=credentials, headers=headers) 
    except Exception:
        print("Request failed, backing off for 5 seconds.")
        time.sleep(5)
        return shakepayAPIAuth(shakepayUsername, shakepayPassword)

def shakepayAPIPost(endpoint, jsonData):
    #print("Calling Shakepay API Endpoint using POST "+endpoint)
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
    try:
        return requests.post("https://api.shakepay.com"+endpoint, json=jsonData, headers=headers) 
    except Exception:
        print("Request failed, backing off for 5 seconds.")
        time.sleep(5)
        return shakepayAPIPost(endpoint, jsonData)

def shakepayAPIGet(endpoint):
    #print("Calling Shakepay API Endpoint using GET "+endpoint)
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
    try:
        return requests.get("https://api.shakepay.com"+endpoint, headers=headers) 
    except Exception:
        print("Request failed, backing off for 5 seconds.")
        time.sleep(5)
        return shakepayAPIGet(endpoint)

def getWaitlistStats():
    waitlistResponse = json.loads(shakepayAPIGet("/card/waitlist").text)
    transactions = waitlistResponse["history"]

    counter = 0
    for transaction in waitlistResponse["history"]:

        date = datetime.datetime.strptime(transaction["createdAt"].replace("Z","UTC"), "%Y-%m-%dT%H:%M:%S.%f%Z")
        createAtUnix = calendar.timegm(date.utctimetuple())

        if createAtUnix < midnightUnix():
            continue

        counter+=1

    return {
        "position": waitlistResponse["rank"],
        "points": waitlistResponse["score"],
        "swapsToday": counter,
    }

shaketag = ""
def getShaketag():
    global shaketag
    if shaketag == "":
        user_id = jwt.decode(getJWT(), algorithms="HS256", options={"verify_signature": False})["userId"]
        shaketag = json.loads(shakepayAPIGet("/users/"+user_id).text)["username"]
    return shaketag

def saveTransactionsCache(transactions):
    f = open(".transactions", "w")

    date = datetime.datetime.utcnow()
    unixDate = calendar.timegm(date.utctimetuple())
    transactions = { "lastPull":unixDate, "data":transactions }

    global transactionsJson
    transactionsJson = transactions

    f.write(json.dumps(transactions))
    f.close()

transactionsJson = ""
def getTransactionsCache():
    global transactionsJson
    if transactionsJson != "":
        return transactionsJson

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

def pullTransactions(page,size=200):
    if page == 1 and size == 200:
        body = {"filterParams":{"currencies":["CAD"]}}
    else:
        body =  {"pagination":{"descending":True,"rowsPerPage":size,"page":page}, "filterParams":{}}

    print("Will pull transactions page "+str(page), body)

    return shakepayAPIPost("/transactions/history", body)

def updateTransactions(size=200):
    page = 1
    transactionsCache = getTransactionsCache()
    transactions = transactionsCache["data"]

    while True:
        addedTransactions = 0
        foundExistingTransaction = 0
        foundStart = False
        transactionCounter = 0

        newTransactionsResponse = pullTransactions(page, size)
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
    
        #print("checked "+str(transactionCounter)+" from this pull")
        if transactionCounter != size:
            #print("got less than "+str(size)+" transactions, means we reached the end")
            break;

        if foundExistingTransaction > 10:
            #print("found more than 10 transactions, no need to proceed")
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

    try:
        f = open("swapperBalances.csv", "r")
        f.close()
    except:
        f = open("swapperBalances.csv", "w")
        f.write("")
        f.close()

    with open('swapperBalances.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            swapperBalance[row[0]]=float(row[1])

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
    return days_swappers()

def days_swappers(n=1):
    n-=1
    transactionsCache = getTransactionsCache()
    transactions = {key: val for key, val in sorted(transactionsCache["data"].items(), key = lambda item: int(item[1]["createAtUnix"]), reverse=True)}

    swapperBalance = {}

    for transaction in transactions:

        date = datetime.datetime.strptime(transactions[transaction]["createdAt"].replace("Z","UTC"), "%Y-%m-%dT%H:%M:%S.%f%Z")
        createAtUnix = calendar.timegm(date.utctimetuple())

        if createAtUnix < midnightUnix()-(86400*n):
            continue

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

def getWallets():
    walletResponse = shakepayAPIGet("/wallets")
    return json.loads(walletResponse.text)["data"]

def sendFunds(recipient, note, amount, wallet):
    print("Sending",recipient,"$"+str(amount),"with the note:",note)
    body = {"amount": amount,"fromWallet": wallet,"note": note,"to": recipient,"toType": "user"}
    return shakepayAPIPost("/transactions", body)

def shakingSats():
    return shakepayAPIPost("/shaking-sats", {})