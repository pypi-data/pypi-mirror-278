import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 17
project_path = file_path[0:end]
sys.path.append(project_path)

import datetime
import mns_common.utils.date_handle_util as date_util
import mns_common.component.company.company_common_service_api as company_common_service_api
from loguru import logger
import mns_common.api.em.east_money_stock_api as east_money_stock_api
import time
import mns_common.component.common_service_fun_api as common_service_fun_api
import mns_common.component.data.data_init_api as data_init_api
import mns_scheduler.real_time.realtime_quotes_now_create_db_index as realtime_quotes_now_create_db_index_api
import pandas as pd
from mns_common.db.MongodbUtil import MongodbUtil
from mns_common.utils.async_fun import async_fun
import mns_scheduler.trade.auto_sell_service_api as auto_sell_service_api
import mns_common.constant.db_name_constant as db_name_constant
import warnings

warnings.filterwarnings("ignore")

mongodb_util = MongodbUtil('27017')
order = ["_id",
         "symbol",
         "name",
         "industry",
         "chg",
         "quantity_ratio",
         "amount_level",
         "real_exchange",
         "disk_ratio",
         'real_disk_diff_amount_exchange',
         'max_real_main_inflow_multiple',
         'sum_main_inflow_disk',
         "main_inflow_multiple",
         'super_main_inflow_multiple',
         'disk_diff_amount',
         "disk_diff_amount_exchange",
         "exchange",
         "amount",
         "today_main_net_inflow",
         "today_main_net_inflow_ratio",
         "super_large_order_net_inflow",
         "super_large_order_net_inflow_ratio",
         "large_order_net_inflow",
         "large_order_net_inflow_ratio",
         "super_main_inflow_multiple",
         "up_speed",
         "up_speed_05",
         "now_price",
         "high",
         "low",
         "open",
         "yesterday_price",
         "volume",
         "total_mv",
         "flow_mv",
         "list_date",
         "wei_bi",
         "buy_1_num",
         "sell_1_num",
         "outer_disk",
         "inner_disk",
         "average_price",
         "classification",
         "str_now_date",
         "number"]


# 实时表移除数据
@async_fun
def remove_real_time_data(number, realtime_quotes_db_name):
    if number % 50 == 0:
        remove_query = {'number': {"$lte": number - 50}}
        mongodb_util.remove_data(remove_query, realtime_quotes_db_name)


def remove_real_time_all_data():
    remove_query = {}
    mongodb_util.remove_data(remove_query, db_name_constant.REAL_TIME_QUOTES_NOW)


# 保存实时表数据
def save_real_time_quotes(real_time_quotes, now_date, realtime_quotes_db_name, number):
    if 'first_sw_industry' in real_time_quotes.columns:
        real_time_quotes.drop(columns=['first_sw_industry'], inplace=True)
    if 'second_sw_industry' in real_time_quotes.columns:
        real_time_quotes.drop(columns=['second_sw_industry'], inplace=True)
    if 'third_sw_industry' in real_time_quotes.columns:
        real_time_quotes.drop(columns=['third_sw_industry'], inplace=True)
    real_time_quotes.symbol = real_time_quotes.symbol.astype(str)
    str_now_date = now_date.strftime('%Y-%m-%d %H:%M:%S:%f')
    real_time_quotes['_id'] = real_time_quotes['symbol'] + '-' + str_now_date

    try:

        real_time_quotes = real_time_quotes[order]
        real_time_quotes['sum_main_inflow_disk'] = round(real_time_quotes['sum_main_inflow_disk'], 2)
        mongodb_util.insert_mongo(real_time_quotes, realtime_quotes_db_name)
        # 移除现在的数据
        remove_real_time_data(number, realtime_quotes_db_name)
    except BaseException as e:
        logger.error('保存实时数据异常:{}', e)


# 保存历史表数据
def save_real_time_quotes_his(real_time_quotes, now_date, realtime_quotes_db_name, number_his):
    if 'first_sw_industry' in real_time_quotes.columns:
        real_time_quotes.drop(columns=['first_sw_industry'], inplace=True)
    if 'second_sw_industry' in real_time_quotes.columns:
        real_time_quotes.drop(columns=['second_sw_industry'], inplace=True)
    if 'third_sw_industry' in real_time_quotes.columns:
        real_time_quotes.drop(columns=['third_sw_industry'], inplace=True)
    real_time_quotes.symbol = real_time_quotes.symbol.astype(str)
    str_now_date = now_date.strftime('%Y-%m-%d %H:%M:%S:%f')
    real_time_quotes['_id'] = real_time_quotes['symbol'] + '-' + str_now_date

    try:
        real_time_quotes['number'] = number_his

        real_time_quotes = real_time_quotes[order]
        mongodb_util.insert_mongo(real_time_quotes, realtime_quotes_db_name)
    except Exception as e:
        logger.error('保存实时历史数据异常:{}', e)


def handle_init_real_time_quotes_data(real_time_quotes_now, str_now_date, number):
    #  exclude b symbol
    real_time_quotes_now = common_service_fun_api.exclude_b_symbol(real_time_quotes_now.copy())
    #  classification symbol
    real_time_quotes_now = common_service_fun_api.classify_symbol(real_time_quotes_now.copy())
    #  fix industry
    real_time_quotes_now = fix_industry_data(real_time_quotes_now.copy())
    #  calculate parameter
    real_time_quotes_now = data_init_api.calculate_parameter_factor(real_time_quotes_now.copy())

    real_time_quotes_now = real_time_quotes_now.loc[real_time_quotes_now['amount'] != 0]
    real_time_quotes_now['str_now_date'] = str_now_date
    real_time_quotes_now['number'] = number
    return real_time_quotes_now


# fix 错杀数据 有成交量的数据
def fix_industry_data(real_time_quotes_now):
    #  fix industry
    real_time_quotes_now_r = company_common_service_api.amendment_industry(real_time_quotes_now.copy())

    symbol_list = list(real_time_quotes_now_r['symbol'])

    na_real_now = real_time_quotes_now.loc[
        ~(real_time_quotes_now['symbol'].isin(symbol_list))]

    na_real_now = na_real_now.loc[na_real_now['amount'] != 0]

    real_time_quotes_now_result = pd.concat([real_time_quotes_now_r, na_real_now], axis=0)
    return real_time_quotes_now_result


def sync_realtime_quotes():
    # 移除昨日数据
    remove_real_time_all_data()

    now_date_init = datetime.datetime.now()
    str_day_init = now_date_init.strftime('%Y-%m-%d')
    realtime_quotes_db_name = db_name_constant.REAL_TIME_QUOTES_NOW + "_" + str_day_init
    number_his = common_service_fun_api.realtime_quotes_now_max_number(realtime_quotes_db_name, 'number')
    number_his = number_his + 1
    number = common_service_fun_api.realtime_quotes_now_max_number(
        db_name_constant.REAL_TIME_QUOTES_NOW + '_' + str_day_init, 'number')
    number = number + 1
    realtime_quotes_now_create_db_index_api.create_db_index(str_day_init)
    while True:
        now_date = datetime.datetime.now()

        str_now_date = now_date.strftime('%Y-%m-%d %H:%M:%S')
        if bool(date_util.is_trade_time(now_date)):
            try:
                real_time_quotes_now = east_money_stock_api.get_real_time_quotes_all_stocks()
                real_time_quotes_now = handle_init_real_time_quotes_data(real_time_quotes_now.copy(),
                                                                         str_now_date, number)
                save_real_time_quotes(real_time_quotes_now.copy(), now_date, db_name_constant.REAL_TIME_QUOTES_NOW,
                                      number)
                try:
                    auto_sell_service_api.auto_sell_stock(real_time_quotes_now.copy())
                except Exception as e:
                    logger.error("自动卖出执行异常:{}", e)
                # 集合竞价前同步
                if date_util.is_call_auction(str_now_date):
                    if number % 4 == 0:
                        save_real_time_quotes_his(real_time_quotes_now.copy(), now_date, realtime_quotes_db_name,
                                                  number_his)
                        number_his = number_his + 1
                # 开盘前一个小时同步
                elif date_util.is_begin_one_hour(now_date):
                    save_real_time_quotes_his(real_time_quotes_now.copy(), now_date, realtime_quotes_db_name,
                                              number_his)
                    number_his = number_his + 1
                # 下午同步次数
                elif date_util.is_afternoon_time(now_date):
                    if number % 3 == 0:
                        save_real_time_quotes_his(real_time_quotes_now.copy(), now_date, realtime_quotes_db_name,
                                                  number_his)
                        number_his = number_his + 1

                else:
                    # 10:30 到11:30
                    if number % 2 == 0:
                        save_real_time_quotes_his(real_time_quotes_now.copy(), now_date, realtime_quotes_db_name,
                                                  number_his)
                        number_his = number_his + 1

                logger.info("同步实时行情信息:{}", number)
                number = number + 1

            except Exception as e:
                number_his = number_his + 1
                number = number + 1
                logger.error("获取实时行情信息:{}", e)
        elif bool(date_util.is_no_trade_time(now_date)):

            break
        else:
            time.sleep(1)


if __name__ == '__main__':
    sync_realtime_quotes()
