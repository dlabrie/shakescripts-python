import sys
from shakepay import *

for swapper in sys.argv:
    if swapper=="swapper.py": 
        continue

    print("Pulling transactions for "+swapper)

    swaps = swapperTransactions(swapper)
    for swap in swaps:
        print(swaps[swap]["createdAt"]+" for $"+str(swaps[swap]["amount"])+" ("+swaps[swap]["direction"]+") | "+swaps[swap]["note"]+"")
        
    print("")

        
