from search_page import search_url
from crawling_data import crawling_data
from make_db import df_to_db

import time
from apscheduler.schedulers.blocking import BlockingScheduler

#스케줄링을 통한 최종 실행
sched = BlockingScheduler()

# 매일 오후 2시 30분마다 실행
@sched.scheduled_job('cron', hour='14', minute='30', id='test_1')
def cp():
    df_to_db(crawling_data(search_url()))

sched.start()