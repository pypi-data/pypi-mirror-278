import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 14
project_path = file_path[0:end]
sys.path.append(project_path)
from loguru import logger
import easytrader
from easytrader import grid_strategies
import mns_common.api.akshare.stock_bid_ask_api as stock_bid_ask_api

user = easytrader.use('ths')
user.connect(r'D:\Program Files\ths\xiadan.exe')
user.grid_strategy = grid_strategies.Xls
user.grid_strategy_instance.tmp_folder = 'C:\\custom_folder'


# 下单
def order_buy(symbol, buy_price, buy_volume):
    logger.warning("买入代码:{},买入价格:{},买入数量:{}", symbol, buy_price, buy_volume)
    user.enable_type_keys_for_editor()
    buy_result = user.buy(symbol, buy_price, buy_volume)

    return buy_result


# 自动一键打新
def auto_ipo_buy():
    user.auto_ipo()


# 获取持仓
def get_position():
    return user.position


# 卖出
def order_sell(symbol, sell_price, sell_volume):
    user.enable_type_keys_for_editor()
    sell_result = user.sell(symbol, sell_price, sell_volume)
    return sell_result


# 取消
def order_cancel(entrust_no):
    user.enable_type_keys_for_editor()
    cancel_result = user.cancel_entrust(entrust_no)
    return cancel_result


# 获取最新卖出价格
def get_last_sell_price(symbol):
    stock_bid_ask_df = stock_bid_ask_api.stock_bid_ask_em(symbol)
    buy_5 = list(stock_bid_ask_df['buy_5'])[0]
    if buy_5 != 0:
        return buy_5
    buy_4 = list(stock_bid_ask_df['buy_4'])[0]
    if buy_4 != 0:
        return buy_4

    buy_3 = list(stock_bid_ask_df['buy_3'])[0]
    if buy_3 != 0:
        return buy_3

    buy_2 = list(stock_bid_ask_df['buy_2'])[0]
    if buy_2 != 0:
        return buy_2

    buy_1 = list(stock_bid_ask_df['buy_1'])[0]
    if buy_1 != 0:
        return buy_1
    # 跌停价格
    sell_1 = list(stock_bid_ask_df['sell_1'])[0]
    if sell_1 != 0:
        return sell_1


# 获取最新价格
def get_last_buy_price(symbol):
    stock_bid_ask_df = stock_bid_ask_api.stock_bid_ask_em(symbol)
    # 用二档买入 五档成本过高
    sell_2 = list(stock_bid_ask_df['sell_2'])[0]
    if sell_2 != 0:
        return sell_2
    sell_5 = list(stock_bid_ask_df['sell_5'])[0]
    if sell_5 != 0:
        return sell_5
    sell_4 = list(stock_bid_ask_df['sell_4'])[0]
    if sell_4 != 0:
        return sell_4
    sell_3 = list(stock_bid_ask_df['sell_3'])[0]
    if sell_3 != 0:
        return sell_3
    sell_1 = list(stock_bid_ask_df['sell_1'])[0]
    if sell_1 != 0:
        return sell_1
    # 打板价格
    buy_1 = list(stock_bid_ask_df['buy_1'])[0]
    if buy_1 != 0:
        return buy_1


if __name__ == '__main__':
    # while True:
    position_df = get_position()
    print(position_df)
    # buy_result_df = order_buy('300085', '10.28', 1000)
    # print(buy_result_df)
    # auto_ipo_buy()
    # cancel_result_df = order_cancel('0111735004')
    # print(cancel_result_df)
    # sell_result_df = order_sell('300917', '24.88', 200)
    # print(sell_result_df)
