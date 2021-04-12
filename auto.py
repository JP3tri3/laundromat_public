import sys
sys.path.append("..")
from api.bybit_api import Bybit_Api
import controller.comms as comms
import database.config as config
from logic.strategy import Strategy_VWAP_Cross
from database.database import Database as db
import asyncio

#manual Setters:
testnet = True #change to false if running on mainnet
leverage = 3  #set leverage
symbol_pair = 'BTCUSD' #change for your chosen trading symbol pair, only setup for 'BTCUSD' and "ETHUSD" currently
input_quantity = 500 #change for your total number of contracts
strat_id = '1_min'   #database config, this has to match the strat ID used in database table
trade_id = 'bybit_auto_1' #database config, this has to match the trade ID used in database table

vwap_margin_neg = 10 #change if using Strategy_VWAP_Cross
vwap_margin_pos = -10 #change if using Strategy_VWAP_Cross

async def main():

    #input true to clear logs & table:
    db().clear_all_tables_values(True)
    db().delete_trade_records(True)

    if (testnet == True):
        api_key = config.BYBIT_TESTNET_API_KEY 
        api_secret = config.BYBIT_TESTNET_API_SECRET
    else:
        api_key = config.BYBIT_MAINNET_API_KEY 
        api_secret = config.BYBIT_MAINNET_API_SECRET        


    if (symbol_pair == "BTCUSD"):
        symbol = 'BTC'
        key_input = 0
        limit_price_difference = 0.50
        db().update_trade_values(trade_id, strat_id, symbol, symbol_pair,  key_input, limit_price_difference, leverage, input_quantity, 'empty', 0, 0, 0)
    elif (symbol_pair == "ETHUSD"):
        symbol = 'ETH'
        key_input = 1
        limit_price_difference = 0.05
        db().update_trade_values(trade_id, strat_id, symbol, symbol_pair, key_input, limit_price_difference, leverage, input_quantity, 'empty', 0, 0, 0)
    else:
        print("Invalid Symbol Pair")

    #initiate strategy, change 'strat' class depending on chosen strategy:
    strat = Strategy_VWAP_Cross(api_key, api_secret, trade_id, strat_id, symbol, symbol_pair, key_input, input_quantity, leverage, limit_price_difference, vwap_margin_neg, vwap_margin_pos)
    api = Bybit_Api(api_key, api_secret, symbol, symbol_pair, key_input)

    api.set_leverage(leverage)

    #initiate strat, change 'strat' function depending on chosen strategy
    strat.vwap_cross_strategy()
                    



loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
