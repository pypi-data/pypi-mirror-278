import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 17
project_path = file_path[0:end]
sys.path.append(project_path)
from datetime import datetime
import mns_common.api.ths.ths_stock_api as ths_stock_api
import mns_common.utils.date_handle_util as date_handle_util
import mns_common.utils.data_frame_util as data_frame_util


def sync_wei_concept_data():
    now_date = datetime.now()
    str_day = now_date.strftime('%Y-%m-%d')
    number = 1
    result = None
    while True:
        wen_cai_concept_df = ths_stock_api.ths_concept_wen_cai(date_handle_util.no_slash_date(str_day),
                                                               str(number))
        result = data_frame_util.merge_choose_data_no_drop(result, wen_cai_concept_df)
        if wen_cai_concept_df.shape[0] < 50:
            break
        number = number + 1
    result = result.rename(columns={"股票代码": "symbol",
                                    "股票简称": "name",
                                    "最新价": "price",
                                    "最新涨跌幅": "chg",
                                    "所属概念": "concepts",
                                    "所属概念数量": "concept_num"
                                    })
    result = result[[
        'symbol',
        'name',
        'price',
        'chg',
        'concepts',
        'concept_num',
        'market_code',
        'code',
    ]]
    result['chg'].fillna(0, inplace=True)
    result['price'].fillna(0, inplace=True)
    result['concepts'].fillna(0, inplace=True)
    return result


if __name__ == '__main__':
    df = sync_wei_concept_data()
    print(df)
