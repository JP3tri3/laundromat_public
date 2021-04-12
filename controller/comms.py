import sys
sys.path.append("..")
from database.database import Database as db
import datetime


def update_data_persistent(data):
        table_id = data['input_name']

        last_candle_high = data['last_candle_high']
        last_candle_low = data['last_candle_low']
        last_candle_vwap = data['last_candle_vwap']
        wt1 = data['wt1']
        wt2 = data['wt2']

        db().update_strat_values(table_id, wt1, wt2, last_candle_high, last_candle_low, last_candle_vwap)        

def update_data_on_alert(data):
        strat_id = data['name']
        input_column = data['key']
        input_value = data['value']

        update_data(input_name, input_key, input_value)
        conn.updateTableValue('strategy', strat_id, input_column, input_value)

