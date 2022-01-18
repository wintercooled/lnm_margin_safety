import json

# https://github.com/ln-markets/api-python
from lnmarkets import rest

#
# Adds margin to long positions until they are within safety limit specified
#

# SETTINGS
SAFETY_MARGIN = 5000 # The amount in USD you want your positions to sit under the price.
                     # Example: price (bid) 40000 and position margin calls at 39000 and
                     #          you want to add margin until margin call drops to 38000
                     #          then set this to 2000

MARGIN_ADD_AMOUNT = 1000 # The amount of margin (sats) to add to a position each call.

# API CREDENTIALS
# API KEY NAME: your api key name
KEY = 'your api key'
SECRET = 'your api secret'
PASSPHRASE = 'your api passphrase'


def get_risky_positions(lnm, current_price, safety_margin):
    running_positions = json.loads(lnm.futures_get_positions({ 'type': 'running' }))
    risky_positions = []

    for rp in running_positions:
        liquidation = rp['liquidation']
        difference = current_price - liquidation
        if difference < safety_margin:
            pid = rp['pid']
            print(f'AT RISK: {pid}')
            risky_positions.append(rp)
    return risky_positions


def add_margin(lnm, margin_add_amount, pid):
    print(f'ADDING MARGIN: {pid}')
    lnm.futures_add_margin_position(
        {
            'amount': margin_add_amount,
            'pid': pid
        }
    )


options = {
    'key': KEY,
    'secret': SECRET,
    'passphrase': PASSPHRASE
}

lnm = rest.LNMarketsRest(**options)

current_price = json.loads(lnm.futures_get_ticker())['bid']
print(f'CURRENT PRICE (USD): {current_price}')

balance = json.loads(lnm.get_user())['balance']
print(f'BALANCE (sats): {balance}')

print(f'SAFETY MARGIN (sats): {SAFETY_MARGIN}')

risky_positions = get_risky_positions(lnm, current_price, SAFETY_MARGIN)

print(f'NUMBER OF RISKY POSITIONS: {len(risky_positions)}')

while len(risky_positions) > 0:
    for rp in risky_positions:
        pid = rp['pid']
        add_margin(lnm, MARGIN_ADD_AMOUNT, pid)
    risky_positions = get_risky_positions(lnm, current_price, SAFETY_MARGIN)
