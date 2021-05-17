# Shakescripts Python


## How to get it going
docker-compose build
docker-compose up -d swapbot-tools
docker exec -it swapbot-tools sh
python login.py
 
Now before you start the bot, you should adjust all your balances in the all_swaps() function of shakepay.py.
You can see what they are with:

python all_swaps.py
 
Once you are satisfied with the outcome:
CTRL + d to detach
 
docker-compose up -d swapbot
 
The swapbot should be running from there on

If you wish to use the tools, you can attach to the swapbot-tools container with
docker exec -it swapbot-tools sh

## What tools are there?

the latest transactions
python swap.py domi167 somiadow

Transactions with a swapper
python swapper.py domi167

All_swaps.js equivalent:
python all_swaps.py

Fastest swappers of the day
python time_to_swap.py

Half assed timestamps of today's swaps
python return_time.py
