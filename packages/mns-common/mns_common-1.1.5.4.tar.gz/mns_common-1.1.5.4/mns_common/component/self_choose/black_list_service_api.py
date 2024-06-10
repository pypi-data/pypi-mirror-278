import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 16
project_path = file_path[0:end]
sys.path.append(project_path)
import pandas as pd
from mns_common.db.MongodbUtil import MongodbUtil
import mns_common.utils.data_frame_util as data_frame_util

mongodb_util = MongodbUtil('27017')
import mns_common.constant.db_name_constant as db_name_constant
from functools import lru_cache

# 1 重大违法类
MAJOR_VIOLATIONS = 'major_violations'
## 立案调查
REGISTER_INVESTIGATE = 'register_investigate '

# 2 财务类
FINANCIAL = 'financial'

## 财务年报审计有问题(非标准无保留)
FINANCIAL_PROBLEM_ANNUAL_REPORT = 'financial_problem_annual_report'
## 财务利润表有问题
FINANCIAL_PROBLEM_PROFIT = 'financial_problem_profit'
## 负债比有问题
FINANCIAL_PROBLEM_DEBT = 'financial_problem_debt'
## 未出财报
FINANCIAL_PROBLEM_NOT_REPORT = 'financial_problem_not_reported'

# 3 规范类
COMPLIANCE = 'compliance'
#

# 4 交易类
TRANSACTIONS = 'transactions'

# 5自主拉黑
SELF_SHIELD = 'self_shield'


# 黑名单操作

def save_black_stock(
        id_key,
        symbol,
        name,
        str_day,
        str_now_date,
        choose_reason,
        choose_reason_detail,
        announce_url,
        black_type,
        black_type_detail):
    query_exist = {'_id': id_key}
    if mongodb_util.exist_data_query(db_name_constant.SELF_BLACK_STOCK, query_exist):
        return
    black_choose_dict = {
        "_id": id_key,
        "symbol": symbol,
        "name": name,
        "str_day": str_day,
        "str_now_date": str_now_date,
        "choose_reason": choose_reason,
        "choose_reason_detail": choose_reason_detail,
        'announce_url': announce_url,
        'black_type': black_type,
        "black_type_detail": black_type_detail,
        'valid': True
    }
    black_choose_df = pd.DataFrame(black_choose_dict, index=[1])
    mongodb_util.save_mongo(black_choose_df, db_name_constant.SELF_BLACK_STOCK)


# 获取黑名单 列表
@lru_cache(maxsize=None)
def get_black_stock_list(begin_day):
    if begin_day is None:
        query = {"valid": True}
    else:
        query = {"$gte": begin_day, "valid": True}
    self_black_stock_df = mongodb_util.find_query_data(db_name_constant.SELF_BLACK_STOCK, query)
    if data_frame_util.is_not_empty(self_black_stock_df):
        return list(self_black_stock_df['symbol'])
    else:
        return ['000001']
