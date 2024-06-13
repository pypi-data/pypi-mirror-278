import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 17
project_path = file_path[0:end]
sys.path.append(project_path)
from loguru import logger
from mns_common.db.MongodbUtil import MongodbUtil
mongodb_util = MongodbUtil('27017')

def create_db_index(str_day):
    query_trade_day = {'_id': str_day}
    is_trade_day = mongodb_util.exist_data_query('trade_date_list', query_trade_day)
    if is_trade_day:
        try:
            mongodb_util.create_index('realtime_quotes_now_' + str_day, [("symbol", 1)])
            mongodb_util.create_index('realtime_quotes_now_' + str_day, [("number", 1)])
            mongodb_util.create_index('realtime_quotes_now_' + str_day, [("symbol", 1), ("number", 1)])
            mongodb_util.create_index('realtime_quotes_now_' + str_day, [("str_now_date", 1)])
            logger.info("创建索引成功:{}", str_day)
        except BaseException:
            logger.warning("创建索引异常:{}", )


if __name__ == '__main__':
    create_db_index("2023-08-11")
