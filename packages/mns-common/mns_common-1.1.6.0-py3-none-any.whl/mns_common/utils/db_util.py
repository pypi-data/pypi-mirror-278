import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 14
project_path = file_path[0:end]
sys.path.append(project_path)

from mns_common.db.MongodbUtil import MongodbUtil
from functools import lru_cache

mongodb_util_27017 = MongodbUtil('27017')
mongodb_util_21019 = MongodbUtil('27019')


# 获取数据库链接 27017
@lru_cache(maxsize=None)
def get_db(str_day):
    trade_date_list = mongodb_util_27017.find_query_data('trade_date_list',
                                                         query={"_id": str_day, 'tag': False})
    tag = trade_date_list.shape[0] > 0
    if tag:
        return mongodb_util_27017
    else:
        return mongodb_util_21019


# 获取str_day日期 实时数据 的 field 最小值
@lru_cache(maxsize=None)
def get_realtime_quotes_now_min_number(str_day, field, symbol):
    if field is None:
        field = 'number'
    if symbol is None:
        symbol = '000001'
    realtime_quotes_db_name = 'realtime_quotes_now_' + str_day
    db = get_db(str_day)
    min_str_now_date = str_day + " 09:26:00"
    query = {'symbol': symbol, "str_now_date": {"$gte": min_str_now_date}}
    df = db.ascend_query(query, realtime_quotes_db_name, field, 1)
    if df is None or df.shape[0] == 0:
        return 1
    else:
        return list(df[field])[0]


# 获取str_day日期 实时数据 的 field 最大值
@lru_cache(maxsize=None)
def get_realtime_quotes_now_max_number(str_day, field, symbol):
    if field is None:
        field = 'number'
    if symbol is None:
        symbol = '000001'
    realtime_quotes_db_name = 'realtime_quotes_now_' + str_day
    db = get_db(str_day)
    min_str_now_date = str_day + " 09:26:00"
    query = {'symbol': symbol, "str_now_date": {"$gte": min_str_now_date}}
    df = db.descend_query(query, realtime_quotes_db_name, field, 1)
    if df is None or df.shape[0] == 0:
        return 1
    else:
        return list(df[field])[0]


if __name__ == '__main__':
    print(get_realtime_quotes_now_max_number('2024-06-04', None, None))
    print(get_realtime_quotes_now_min_number('2024-06-04', None, None))