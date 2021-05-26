# Shakepay Python Bot


## How to get it going

Docker:
```bash
docker-compose build
docker-compose up -d swapbot-tools
docker exec -it swapbot-tools sh
python login.py
```
No Docker:
```bash
pip install --no-cache-dir -r requirements.txt
python login.py
```

Now before you start the bot, you should adjust all your balances in the all_swaps() function of shakepay.py.
You can see what they are with:
Docker+No Docker:
```bash
python all_swaps.py
```

Docker: CTRL+D to detach

Once you are satisfied with the outcome:

Docker:
```bash
docker-compose up -d swapbot
```
No Docker:
```bash
python refund.py
```
The swapbot should be running from there on

If you wish to use the tools, you can attach to the swapbot-tools container with
```bash
docker exec -it swapbot-tools sh
```

## What tools are there?

Swap initiator
```bash
python swap.py domi167 somiadow hydra stmich
```
Transactions with a swapper
```bash
python swapper.py domi167
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
