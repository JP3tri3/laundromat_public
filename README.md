Setup:

this is setup to pair with mySQL server, everything needed to setup the SQL tables is commented out in database.sql_connector.py 

if only using bot to initiate strategies based off buy/sell signals from Tradeview and don't need to store data, all mysql references can be removed and update strategy class for creating trades based off webhook variable.

in database.config:
Add Bybit testnet / mainnet API keys
Add SQL Host / user / password / auth / db name

'listener.py' run the webhook listener

Options:

'manual.py' will connect with exchange for manual trading automation through chosen terminal
- Update details under 'manual setters' in view.ui before using

'auto.py' will run bot strat. 
- launch NGROK with open port, or run on server open to domain
- run 'python listener.py'
- Update details under 'manual setters' comment before using
- Change strategy class depending on strategy(in main()), current strategy implemented for example & testing purposes is basic VWAP crossover strategy.  You can add more strategy classes under logic.strategy

Webhook json format:
update 'input name' in webhook alert for database table input name, edit depending on strategy
can update passphrase in json & database.config

{
	"passphrase": "abc123",
	"input_name": "",
	"persistent_data": "True",
	"last_candle_high": {{high}},
	"last_candle_low": {{low}},
	"last_candle_vwap": {{plot("vwap")}},
	"wt1": {{plot("wt1")}},
	"wt2": {{plot("wt2")}}
 }