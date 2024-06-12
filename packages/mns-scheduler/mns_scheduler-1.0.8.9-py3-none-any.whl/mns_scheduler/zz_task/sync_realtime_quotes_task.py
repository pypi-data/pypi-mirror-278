import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 17
project_path = file_path[0:end]
sys.path.append(project_path)
import mns_scheduler.real_time.realtime_quotes_now_sync as realtime_quotes_now_sync
import mns_scheduler.company_info.company_info_sync_api as company_info_sync_api
from loguru import logger
from apscheduler.schedulers.blocking import BlockingScheduler


def sync_realtime_quotes():
    logger.error("同步实时数据开始")
    # 更新新股公司信息
    company_info_sync_api.new_company_info_update()
    realtime_quotes_now_sync.sync_realtime_quotes()
    logger.error("同步实时数据完成")


blockingScheduler = BlockingScheduler()

# 同步实时数据
blockingScheduler.add_job(sync_realtime_quotes, 'cron', hour='09', minute='20', max_instances=4)

print('同步实时行情定时任务启动成功')
blockingScheduler.start()
