import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 16
project_path = file_path[0:end]
sys.path.append(project_path)

# 每月最大交易天数
MAX_TRADE_DAYS_PER_MONTH = 23
# 每周最大交易天数
MAX_TRADE_DAYS_PER_MONTH = 5


def handle_month_week_line(k_line_info, stock_qfq_daily, deal_days):
    if 1 < deal_days < MAX_TRADE_DAYS_PER_MONTH:
        month_01 = round(sum(stock_qfq_daily['chg']), 2)
        k_line_info['sum_month'] = month_01
        k_line_info['month_num'] = 1
        k_line_info['month01'] = month_01
    elif (deal_days >= MAX_TRADE_DAYS_PER_MONTH) \
            and (deal_days < MAX_TRADE_DAYS_PER_MONTH * 2):
        stock_qfq_daily_month_01 = stock_qfq_daily.iloc[0:MAX_TRADE_DAYS_PER_MONTH]
        month_01 = round(sum(stock_qfq_daily_month_01['chg']), 2)
        stock_qfq_daily_month_02 = stock_qfq_daily.iloc[MAX_TRADE_DAYS_PER_MONTH + 1, deal_days - 1]
        month_02 = round(sum(stock_qfq_daily_month_02['chg']), 2)
        k_line_info['sum_month'] = round(month_01 + month_02, 2)
        k_line_info['month_num'] = 2
        k_line_info['month01'] = month_01
        k_line_info['month_02'] = month_02
    elif deal_days >= MAX_TRADE_DAYS_PER_MONTH * 2:
        stock_qfq_daily_month_01 = stock_qfq_daily.iloc[0:MAX_TRADE_DAYS_PER_MONTH]
        month_01 = round(sum(stock_qfq_daily_month_01['chg']), 2)
        stock_qfq_daily_month_02 = stock_qfq_daily.iloc[MAX_TRADE_DAYS_PER_MONTH + 1, MAX_TRADE_DAYS_PER_MONTH * 2]
        month_02 = round(sum(stock_qfq_daily_month_02['chg']), 2)

        stock_qfq_daily_week_sum = stock_qfq_daily.iloc[MAX_TRADE_DAYS_PER_MONTH * 2 + 1, deal_days - 1]

        week_sum = round(sum(stock_qfq_daily_week_sum['chg']), 2)

        k_line_info['sum_month'] = round(month_01 + month_02, 2)
        k_line_info['month_num'] = 2
        k_line_info['month01'] = month_01
        k_line_info['month_02'] = month_02

        k_line_info['week_num'] = week_sum
    return k_line_info
