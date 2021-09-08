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
        "x-device-total-memory": "6014582784",
        "x-device-serial-number":"",
        "x-device-name": "",
        "x-device-has-notch": "false",
        "user-agent": "Shakepay App v1.7.24 (17024) on domi167 bot",
        "x-device-locale": "en-CA",
        "x-device-manufacturer": "Bot",
        "x-device-is-tablet": "false",
        "x-device-total-disk-capacity": "127881465856",
        "x-device-system-name": "Python",
        "x-device-carrier": "",
        "x-device-model": "Bot",
        "x-device-id": "",
        "x-device-country": "CA",
        "x-device-mac-address": "02:00:00:00:00:00",
        "accept-language": "en-ca",
        "x-device-ip-address": "10.100.100.11",
        "x-device-unique-id": getUUID(),
        "content-type": "application/json",
        "accept": "application/json",
        "x-device-brand": "Bot",
        "accept-encoding": "gzip, deflate, br",
        "x-device-system-version": "",
    }
    credentials =  {"strategy":"local","totpType":"sms","username":shakepayUsername,"password":shakepayPassword}
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
        "user-agent": "Shakepay App v1.7.24 (17024) on domi167 bot",
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
        "user-agent": "Shakepay App v1.7.24 (17024) on domi167 bot",
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
    try:
        waitlistResponse = json.loads(shakepayAPIGet("/card/waitlist").text)
        transactions = waitlistResponse["history"]
    except Exception:
        print("Request failed, backing off for 5 seconds.")
        time.sleep(5)
        return getWaitlistStats();

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
        try:
            shaketag = json.loads(shakepayAPIGet("/users/"+user_id).text)["username"]
        except Exception:
            print("Request failed, backing off for 5 seconds.")
            time.sleep(5)
            return getShaketag();

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

def pullTransactions(isInit: bool, timestamp: str):
    queryString = ""
    if isInit == True:
        queryString = "?limit=2000&currency=CAD&before="+timestamp
    else:
        queryString = "?limit=2000&currency=CAD&since="+timestamp

    print("Will pull transactions page "+str(queryString))

    apiResponse = shakepayAPIGet("/transactions/history"+queryString)
    try:
        return json.loads(apiResponse.text)
    except Exception:
        print("Request failed, backing off for 5 seconds.")
        time.sleep(5)
        return pullTransactions(isInit, timestamp);

globalTimestamp = "2021-04-21T04:00:00.000Z"

def updateTransactions():
    global globalTimestamp

    transactionsCache = getTransactionsCache()
    transactions = transactionsCache["data"]

    isInit = False
    if len(transactions.keys()) == 0:
        isInit = True
        globalTimestamp = datetime.datetime.utcnow().isoformat()+"Z"
    else:
        # Check what is the latest transaction in cache, so we load from there
        date = datetime.datetime.strptime(globalTimestamp.replace("Z","UTC"), "%Y-%m-%dT%H:%M:%S.%f%Z")
        globalTimestampUnix = calendar.timegm(date.utctimetuple())
        for transactionId in transactions:
            transaction = transactions[transactionId]
            if globalTimestampUnix < transaction["createAtUnix"]:
                globalTimestampUnix = transaction["createAtUnix"]
                globalTimestamp = transaction["createdAt"]

    while True:
        addedTransactions = 0
        transactionCounter = 0

        newTransactions = pullTransactions(isInit, globalTimestamp)

        for transaction in newTransactions:
            transactionCounter+=1
            # check if already in ledger
            if transaction["transactionId"] in transactions:
                continue

            if transaction["type"]!="peer": 
                continue

            date = datetime.datetime.strptime(transaction["createdAt"].replace("Z","UTC"), "%Y-%m-%dT%H:%M:%S.%f%Z")
            createAtUnix = calendar.timegm(date.utctimetuple())
            if createAtUnix < 1618963200:
                break

            addedTransactions += 1
            transaction["createAtUnix"] = createAtUnix
            transactions[transaction["transactionId"]] = transaction

            globalTimestamp = transaction["createdAt"];
            
        #print("checked "+str(transactionCounter)+" from this pull")
        if transactionCounter < 1999:
            #print("got less than "+str(size)+" transactions, means we reached the end")
            break
    
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
    wallets = getWallets()
    for wallet in wallets:
        if wallet["currency"] == "CAD":
            return wallet

def getBTCWallet():
    wallets = getWallets()
    for wallet in wallets:
        if wallet["currency"] == "BTC":
            return wallet

def getWallets():
    walletResponse = shakepayAPIGet("/wallets")
    try:
        return json.loads(walletResponse.text)["data"]
    except Exception:
        print("Request failed, backing off for 5 seconds.")
        time.sleep(5)
        return getWallets();

def sendFunds(recipient, note, amount, wallet):
    print("Sending",recipient,"$"+str(amount),"with the note:",note)
    body = {"amount": amount,"fromWallet": wallet,"note": note,"to": recipient,"toType": "user"}
    return shakepayAPIPost("/transactions", body)

def shakingSats():
    return shakepayAPIPost("/shaking-sats", {})