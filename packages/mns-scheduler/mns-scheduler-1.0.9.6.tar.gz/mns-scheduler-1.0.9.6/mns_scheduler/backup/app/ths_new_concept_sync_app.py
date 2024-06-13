import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 17
project_path = file_path[0:end]
sys.path.append(project_path)
import mns_common.api.ths.ths_stock_api as ths_stock_api
import datetime
import time
import mns_common.api.msg.push_msg_api as push_msg_api
from loguru import logger
import mns_scheduler.concept.ths.common.ths_concept_sync_common_api as ths_concept_sync_common_api
import pandas as pd
from mns_common.db.MongodbUtil import MongodbUtil

mongodb_util = MongodbUtil('27017')


# app 端获取新增概念信息 接口不稳定

# 获取最大概念代码
def get_max_concept_name():
    query = {"symbol": {'$ne': 'null'}, "success": True}
    return mongodb_util.descend_query(query, 'ths_concept_list', 'symbol', 1)


# 获取app端新概念名称
def get_concept_detail_info_app(concept_code):
    return ths_stock_api.get_new_concept_code_app(concept_code)


# 获取app端新概念详细列表
def get_new_concept_detail_list_app(concept_code):
    new_concept_symbol_list = ths_stock_api.get_new_concept_list_app(concept_code)
    if new_concept_symbol_list is None or new_concept_symbol_list.shape == 0:
        return None
    new_concept_symbol_list = new_concept_symbol_list[ths_concept_sync_common_api.order_fields]
    new_concept_symbol_list['_id'] = str(concept_code) + '-' + new_concept_symbol_list['symbol']
    return new_concept_symbol_list


# 推送新概念信息到微信
def push_msg_to_we_chat_app(concept_code, concept_name):
    url = f'https://m.10jqka.com.cn/hq/industry.html#code={concept_code}&refCountId=R_55ba2964_186'
    msg = "概念代码:" + str(concept_code) + "," + "概念名称:" + concept_name + "," + "url:   " + url
    title = "新增概念:" + str(concept_code) + "-" + concept_name
    push_msg_api.push_msg_to_wechat(title, msg)


# 保存新概念信息到数据库
def save_ths_concept_list_app(concept_code, concept_name, str_day, str_now_time, success):
    concept_code = int(concept_code)
    url = 'https://m.10jqka.com.cn/hq/industry.html#code=' + str(concept_code) + '&refCountId=R_55ba2964_186'
    ths_concept_list = pd.DataFrame([
        [concept_code, concept_code, concept_name, str_day, url, str_now_time, success],
    ], columns=['_id', 'symbol', 'name', 'str_day', 'url', 'str_now_time', 'success'])

    mongodb_util.save_mongo(ths_concept_list, 'ths_concept_list')


# 同步新概念信息 从app爬取
def sync_new_concept_data():
    max_concept_name = get_max_concept_name()
    try:
        now_date = datetime.datetime.now()
        str_day = now_date.strftime('%Y-%m-%d')
        str_now_time = now_date.strftime('%Y-%m-%d %H:%M:%S')
        concept_code = list(max_concept_name['symbol'])[0]
        success = list(max_concept_name['success'])[0]
        if success:
            concept_code = concept_code + 1

        new_concept_df = get_concept_detail_info_app(concept_code)
        if new_concept_df is None or new_concept_df.shape[0] == 0:
            time.sleep(1)
            return None

        concept_name = list(new_concept_df['concept_name'])[0]
        concept_code = list(new_concept_df['concept_code'])[0]
        if success:
            # 推送新概念信息到微信
            push_msg_to_we_chat_app(concept_code, concept_name)
        # 获取新概念详细信息
        new_concept_symbol_list = get_new_concept_detail_list_app(concept_code)

        if new_concept_symbol_list is None or new_concept_symbol_list.shape[0] == 0:
            # 保存新概念信息到数据库
            query = {"symbol": int(concept_code), "success": True}
            exist_success = mongodb_util.exist_data_query('ths_concept_list', query)
            if bool(1 - exist_success):
                save_ths_concept_list_app(concept_code, concept_name, str_day, str_now_time, False)
                time.sleep(1)

        else:
            # 保存新概念信息到数据库
            save_ths_concept_list_app(concept_code, concept_name, str_day, str_now_time, True)
            new_concept_symbol_list.loc[:, 'way'] = 'index_sync'
            # 保存新概念详细信息到数据库
            ths_concept_sync_common_api.save_ths_concept_detail(new_concept_symbol_list, concept_name, str_day,
                                                                str_now_time, concept_code)
            time.sleep(1)

    except BaseException as e:
        logger.error("同步新概念异常:{},concept_code:{}", e, concept_code)


if __name__ == '__main__':
    # myquery1 = {"symbol": {"$ne": 'null'}}
    # newvalues1 = {"$set": {"success": True}}
    #
    # mongodb_util_remote.update_many(myquery1, newvalues1, 'ths_concept_list')
    # concept_df = get_concept_detail_info_app('886033')
    df = get_new_concept_detail_list_app('883418')
    print(df)
    # sync_new_concept_data()
    # code = 886026
    # while True:
    #     symbol_new_concept = get_concept_detail_info_app(code)
    #     logger.info(symbol_new_concept)
    #     new_concept_symbols = ths_stock_api.get_new_concept_list_app(code)
    #     logger.info(new_concept_symbols)
