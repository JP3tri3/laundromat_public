import sys
sys.path.append("..")
import bybit

class Bybit_Api:

    def __init__(self, api_key, api_secret, symbol, symbol_pair, key_input):
        self.client = bybit.bybit(test=True, api_key=api_key, api_secret=api_secret)
        self.symbol = symbol
        self.symbol_pair = symbol_pair
        self.key_input = key_input

    def get_key_input(self):
        return self.key_input

    def my_wallet(self):
        my_wallet = self.client.Wallet.Wallet_getBalance(
            coin=self.symbol).result()
        my_balance = my_wallet[0]['result'][self.symbol]['available_balance']
        print(my_balance)

#symbol:

    def symbol_info_result(self):
        info = self.client.Market.Market_symbolInfo().result()
        return(info[0]['result'])

    def symbol_info_keys(self):
        infoKeys = self.symbol_info_result()
        return infoKeys[self.key_input]

#price:

    def price_info(self):
        keys = self.symbol_info_result()
        key_info = keys[self.key_input]

        last_price = key_info['last_price']
        mark_price = key_info['mark_price']
        ask_price = key_info['ask_price']
        index_price = key_info['index_price']

        print("")
        print("Last Price: " + self.symbol_pair + " " + last_price)
        print("Mark Price: " + self.symbol_pair + " " + mark_price)
        print("Ask Price: " + self.symbol_pair + " " + ask_price)
        print("Index Price: " + self.symbol_pair + " " + index_price)
        print("")

    def last_price(self):
        keys = self.symbol_info_result()
        return float(keys[self.key_input]['last_price'])

#order:
    def get_order(self):
        active_order = self.client.Order.Order_query(symbol=self.symbol_pair).result()
        order = active_order[0]['result']
        return(order)

    def get_order_id(self):
        try:
            order = self.get_order()
            if (order == []):
                return "Waiting on Order ID"
            else:
                order_id = order[0]['order_id']
                return order_id
        except Exception as e:
            print("an exception occured - {}".format(e))
            return False


    def cancel_all_orders(self):
        print("Cancelling All Orders...")
        self.client.Order.Order_cancelAll(symbol=self.symbol).result()


#position:
    def get_position_result(self):
        position_result = self.client.Positions.Positions_myPosition(symbol=self.symbol_pair).result()
        return position_result[0]['result']

    def get_position_side(self):
        try:
            position_result = self.get_position_result()
            return position_result['side']
        except Exception as e:
            print("an exception occured - {}".format(e))   
            return 'null'     

    def get_position_size(self):
        position_result = self.get_position_result()
        return position_result['size']

    def get_position_value(self):
        position_result = self.get_position_result()
        return position_result['position_value']

    def get_active_position_entry_price(self):
        position_result = self.get_position_result()
        return float(position_result['entry_price'])

#orders:
    def place_order(self, price, order_type, side, input_quantity, stop_loss, reduce_only):

        try:
            if(order_type == 'Market'):
                print(f"sending order {price} - {side} {self.symbol_pair} {order_type} {stop_loss}")
                order = self.client.Order.Order_new(side=side, symbol=self.symbol_pair, order_type="Market",
                                            qty=input_quantity, time_in_force="PostOnly", stop_loss=str(stop_loss), reduce_only=reduce_only).result()
            elif(order_type == "Limit"):
                print(f"sending order {price} - {side} {self.symbol_pair} {order_type} {stop_loss}")
                order = self.client.Order.Order_new(side=side, symbol=self.symbol_pair, order_type="Limit",
                                            qty=input_quantity, price=price, time_in_force="PostOnly", stop_loss=str(stop_loss), reduce_only=reduce_only).result()
            else:
                print("Invalid Order")
        except Exception as e:
            print("an exception occured - {}".format(e))
            return False
        return order

    def change_order_price(self, price):
        order = self.client.Order.Order_replace(symbol=self.symbol_pair, order_id=str(self.get_order_id()), p_r_price=str(price)).result()
        return order

#Leverage
 
    def get_position_leverage(self):
        position = self.get_position_result()
        return position['leverage']

    def set_leverage(self, leverage):
        set_leverage = self.client.Positions.Positions_saveLeverage(symbol=self.symbol_pair, leverage=str(leverage)).result()
        print("Leverage set to: " + str(leverage))
        return set_leverage    
#stop_loss

    def change_stop_loss(self, sl_amount):
        self.client.Positions.Positions_tradingStop(
            symbol=self.symbol_pair, stop_loss=str(sl_amount)).result()
        print("")
        print("Changed stop Loss to: " + str(sl_amount))

#Profit & Loss
    def closed_profit_loss(self):
        records = self.client.Positions.Positions_closePnlRecords(symbol=self.symbol_pair).result()
        return records[0]['result']['data']

    def closed_profit_lossQuantity(self, index):
        record_result = self.closed_profit_loss()
        return record_result[index]['closed_size']

    def lastProfitLoss(self, index):
        record_result = self.closed_profit_loss()
        return record_result[index]['closed_pnl']

    def last_exit_price(self, index):
        record_result = self.closed_profit_loss()
        return record_result[index]['avg_exit_price']

    def last_entry_price(self, index):
        record_result = self.closed_profit_loss()
        return record_result[index]['avg_entry_price']

    #Calc Entry_Exit

    def calc_last_gain(self, index, input_quantity):
        total = self.lastProfitLoss(index)
        exit_price = float(self.get_exit_price(input_quantity))
        return round(float('%.10f' % total) * exit_price, 3)

    def calc_total_gain(self, input_quantity):
        total = 0
        index = 0
        total_quantity = 0
        flag = False

        while(flag == False):
            total_quantity += self.closed_profit_lossQuantity(index)
            total += self.calc_last_gain(index, input_quantity)

            if total_quantity < input_quantity:
                index += 1
            else:
                flag = True

        return total

    def calc_total_coin(self, input_quantity):
        index = 0
        total_quantity = 0
        total = 0.0
        flag = False

        while(flag == False):
            amount = float(self.lastProfitLoss(index))
            total += amount
            total_quantity += self.closed_profit_lossQuantity(index)

            if total_quantity < input_quantity:
                index += 1
            else:
                flag = True

        return ('%.10f' % total)

    def get_entry_price(self, input_quantity):
        index = 0
        divisible = 1
        last_entry_price = self.last_entry_price(index)
        entry_price = 0
        total_quantity = 0

        flag = False

        while(flag == False):
            total_quantity += self.closed_profit_lossQuantity(index)
            entry_price += last_entry_price

            if total_quantity < input_quantity:
                index += 1
                divisible += 1
                print("Index = " + str(index))
            else:
                flag = True

        if (index == 0):
            return entry_price
        else:
            return (entry_price / divisible)


    def get_exit_price(self, input_quantity):
        index = 0
        divisible = 1
        last_exit_price = self.last_exit_price(index)
        exit_price = 0
        total_quantity = 0
        flag = False

        while(flag == False):
            total_quantity += self.closed_profit_lossQuantity(index)
            exit_price += last_exit_price

            if total_quantity < input_quantity:
                index += 1
                divisible += 1
                print("Index = " + str(index))
            else:
                flag = True
        
        if (index == 0):
            return exit_price
        else:
            return (exit_price / divisible)