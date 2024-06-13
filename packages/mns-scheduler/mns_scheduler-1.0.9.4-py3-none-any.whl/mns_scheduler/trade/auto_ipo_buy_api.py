import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 17
project_path = file_path[0:end]
sys.path.append(project_path)

import mns_common.component.trade.trade_service_api as trade_service_api


## 自动一键打新
def auto_ipo_buy():
    trade_service_api.auto_ipo_buy()


if __name__ == '__main__':
    auto_ipo_buy()
