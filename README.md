# ShakePay Python Swapbot

These scripts and bot are provided "as is" and do not have any guarantees on their outcome. By using these scripts you acknowledge this disclamer and assume full responsibility of using them.

If you wish to donate, send any amount other than 5$ to domi167. BTC and ETH Accepted :)

# What tools are there?

Swap initiator
```bash
python swap.py domi167 somiadow hydra stmich
```
Transactions with a swapper
```bash
python transactions.py domi167
```
All_swaps.js equivalent:
```bash
python all_swaps.py
```
Fastest swappers of the day
```bash
python time_to_swap.py
```

Half assed timestamps of today's swaps
```bash
python return_time.py
```

# How to get it going

## ------------ Docker ------------
```bash
docker-compose build
docker-compose up -d swapbot-tools
docker exec -it swapbot-tools sh
python login.py
```
Now before you start the bot, you should adjust all your balances (if needed) by using the swapperBalances.csv.
If someone gave you money, you should put a negative balance:
```txt
domi167,-5.0
```
If you donated any amount to someone you should put a positive balance:
```txt
domi167,420.69
```
If you were scammed and don't want to be reminded, you should put a positive balance, but not the full amount [the bot would be sending the $5 back]:
```txt
moneyburner,4.95
```

You can see the balances of more than 5¢ by running
```bash
python all_swaps.py
```

If you wish to use the tools, you can attach to the swapbot-tools container with
```bash
docker exec -it swapbot-tools sh
```
CTRL+D to detach

Once you are satisfied with the outcome:
Run the bot:
```bash
docker-compose up -d swapbot
```

## ------------ No Docker ------------

```bash
pip install --no-cache-dir -r requirements.txt
pip install requests
python login.py
```

Now before you start the bot, you should adjust all your balances (if needed) by using the swapperBalances.csv.
If someone gave you money, you should put a negative balance:
```txt
domi167,-5.0
```
If you donated any amount to someone you should put a positive balance:
```txt
domi167,420.69
```
If you were scammed and don't want to be reminded, you should put a positive balance, but not the full amount [the bot would be sending the $5 back]:
```txt
moneyburner,4.95
```

You can see what they are with:
```bash
python all_swaps.py
```

Once you are satisfied with the outcome, you can run the bot:
```bash
python refund.py
```
The swapbot should be running from there on
