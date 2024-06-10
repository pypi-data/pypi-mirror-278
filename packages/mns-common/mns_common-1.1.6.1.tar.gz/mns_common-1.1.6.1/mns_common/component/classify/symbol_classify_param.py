import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 16
project_path = file_path[0:end]
sys.path.append(project_path)

# 按照上市时间对股票分类

# 股票类型
stock_type_classify_param = {
    #  上市五个交易日的股票 名字以C开头
    "new_stock": "new",
    # 交易上市6-100天的次新股票
    'sub_stock_new': "sub_new",
    # 上市 100-365天的股票
    "sub_stock": "sub",
    # 365 到无穷天的股票
    "normal_stock": "normal",
    # 一个月最大交易天数 23天 三个月 4*23+1 =93  加1是上市第一天
    'sub_stock_new_max_deal_days': 100,
    # 上市交易 100-365天次新的股票
    'sub_stock_max_days': 365,

}
