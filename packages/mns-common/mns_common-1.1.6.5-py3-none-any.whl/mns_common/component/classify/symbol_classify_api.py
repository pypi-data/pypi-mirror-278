import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 16
project_path = file_path[0:end]
sys.path.append(project_path)
import mns_common.utils.data_frame_util as data_frame_util
from mns_common.component.classify.symbol_classify_param import stock_type_classify_param


# 深沪普通股票  选择 10cm涨幅的
def choose_sh_symbol(realtime_quotes_now):
    return realtime_quotes_now.loc[
        (realtime_quotes_now['classification'].isin(['S', 'H']))]


# 选择科创 创业板 20厘米的
def choose_kc_symbol(realtime_quotes_now):
    return realtime_quotes_now.loc[
        realtime_quotes_now['classification'].isin(['K', 'C'])]


# 选择北交所的 30厘米的
def choose_bjs_symbol(realtime_quotes_now):
    return realtime_quotes_now.loc[
        realtime_quotes_now['classification'].isin(['X'])]


# 设置新股次新标记 通过交易时间
def set_stock_type(real_time_quotes_now_init):
    if data_frame_util.is_empty(real_time_quotes_now_init):
        return None
    real_time_quotes_now = real_time_quotes_now_init.copy()
    real_time_quotes_now.loc[:, "stock_type"] = stock_type_classify_param['normal_stock']
    # 上市五个交易日的股票
    real_time_quotes_now.loc[real_time_quotes_now['name'].str.startswith('C'), "stock_type"] = \
        stock_type_classify_param[
            'new_stock']
    # 交易上市6-100天的次新股票
    real_time_quotes_now.loc[
        (real_time_quotes_now['stock_type'] != stock_type_classify_param['new_stock'])
        & (real_time_quotes_now['deal_days'] <= stock_type_classify_param['sub_stock_new_max_deal_days']),
        "stock_type"] = stock_type_classify_param['sub_stock_new']

    # 上市次新股 100-365
    real_time_quotes_now.loc[
        (real_time_quotes_now['deal_days'] >= stock_type_classify_param['sub_stock_new_max_deal_days'])
        & (real_time_quotes_now['deal_days'] <= stock_type_classify_param['sub_stock_max_days']),
        "stock_type"] = stock_type_classify_param['sub_stock']

    return real_time_quotes_now


# 设置新股次新标记 通过上市时间
def set_stock_type_by_diff_days(real_time_quotes_now_init):
    if data_frame_util.is_empty(real_time_quotes_now_init):
        return None
    real_time_quotes_now = real_time_quotes_now_init.copy()
    real_time_quotes_now.loc[:, "stock_type"] = stock_type_classify_param['normal_stock']
    # 上市五个交易日的股票
    real_time_quotes_now.loc[real_time_quotes_now['name'].str.startswith('C'), "stock_type"] = \
        stock_type_classify_param[
            'new_stock']
    # 交易上市6?-150天的次新股票
    real_time_quotes_now.loc[
        (real_time_quotes_now['stock_type'] != stock_type_classify_param['new_stock'])
        & (real_time_quotes_now['deal_days'] <= stock_type_classify_param['sub_stock_new_max_diff_days']),
        "stock_type"] = stock_type_classify_param['sub_stock_new']

    # 上市次新股 150-465
    real_time_quotes_now.loc[
        (real_time_quotes_now['deal_days'] >= stock_type_classify_param['sub_stock_new_max_diff_days'])
        & (real_time_quotes_now['deal_days'] <= stock_type_classify_param['sub_stock_max_diff_days']),
        "stock_type"] = stock_type_classify_param['sub_stock']

    return real_time_quotes_now


# 新上市注册股票
def choose_new_stock(real_time_quotes_now):
    real_time_quotes_now = real_time_quotes_now.loc[
        real_time_quotes_now['stock_type'] == stock_type_classify_param['new_stock']]

    return real_time_quotes_now


# 排除新股
def exclude_new_stock(real_time_quotes_now):
    real_time_quotes_now = real_time_quotes_now.loc[
        real_time_quotes_now['stock_type'] != stock_type_classify_param['new_stock']]
    return real_time_quotes_now


# 选择次新new     # 交易上市6-70天的次新股票
def choose_sub_new(real_time_quotes_now):
    real_time_quotes_now = real_time_quotes_now.loc[
        real_time_quotes_now['stock_type'] == stock_type_classify_param['sub_stock_new']]

    return real_time_quotes_now


# 排除次新new      # 交易上市6-70天的次新股票
def exclude_sub_new(real_time_quotes_now):
    real_time_quotes_now = real_time_quotes_now.loc[
        real_time_quotes_now['stock_type'] != stock_type_classify_param['sub_stock_new']]
    return real_time_quotes_now


# 选择次新 71-365
def choose_sub_stock(real_time_quotes_now):
    real_time_quotes_now = real_time_quotes_now.loc[
        real_time_quotes_now['stock_type'] == stock_type_classify_param['sub_stock']]

    return real_time_quotes_now


# 排除次新  71-365
def exclude_sub_stock(real_time_quotes_now):
    real_time_quotes_now = real_time_quotes_now.loc[
        real_time_quotes_now['stock_type'] != stock_type_classify_param['sub_stock']]
    return real_time_quotes_now


# 选择普通
def choose_normal_stock(real_time_quotes_now):
    real_time_quotes_now = real_time_quotes_now.loc[
        real_time_quotes_now['stock_type'] == stock_type_classify_param['normal_stock']]

    return real_time_quotes_now


# 排除普通
def exclude_normal_stock(real_time_quotes_now):
    real_time_quotes_now = real_time_quotes_now.loc[
        real_time_quotes_now['stock_type'] != stock_type_classify_param['normal_stock']]
    return real_time_quotes_now


# 根据类型列表选择
def choose_stock_by_type_list(real_time_quotes_now, type_list):
    return real_time_quotes_now.loc[
        real_time_quotes_now['stock_type'].isin(type_list)]
