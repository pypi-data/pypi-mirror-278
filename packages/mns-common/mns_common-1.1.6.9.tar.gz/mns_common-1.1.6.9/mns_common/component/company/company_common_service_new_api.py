import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 14
project_path = file_path[0:end]
sys.path.append(project_path)
from functools import lru_cache
from mns_common.db.MongodbUtil import MongodbUtil
import mns_common.constant.db_name_constant as db_name_constant

mongodb_util = MongodbUtil('27017')


@lru_cache(maxsize=None)
def get_company_info_by_field(query_key, query_field_key):
    query = eval(query_key)
    query_field = eval(query_field_key)
    return mongodb_util.find_query_data_choose_field('company_info', query, query_field)


# 获取退市股票代码
@lru_cache(maxsize=None)
def get_de_list_company():
    return list(mongodb_util.find_all_data(db_name_constant.DE_LIST_STOCK)['symbol'])
