# Copyright 2024 Sola Richard Olorunfemi
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pytz import timezone
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

from .utils import (
    get_scheduler_type,
    get_scheduler_start_paused,
    get_jobstore_settings,
    get_timezone,
    get_error_log_settings
)

# logging.basicConfig(level=logging.DEBUG, file=get_error_log_settings())

jobstore_settings = get_jobstore_settings()

scheduler_time_zone = timezone(get_timezone().lower())

jobstore_type = jobstore_settings.get('jobstore_type', 'sqlite')
jobstore_url = jobstore_settings.get('jobstore_url', 'sqlite:///jobs.sqlite')

def scheduler():
    
    if jobstore_type.lower() == 'mongodb':
        from apscheduler.jobstores.mongodb import MongoDBJobStore

        jobstores = {
            'mongo': MongoDBJobStore(client=jobstore_url)
        }
    else:
        from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
        jobstores = {
            'default': SQLAlchemyJobStore(url=jobstore_url)
        }
    executors = {
            'default': ThreadPoolExecutor(20),
            'processpool': ProcessPoolExecutor(5)
        }
    job_defaults = {
        'coalesce': True,
        'max_instances': 2
    }

    scheduler_type = get_scheduler_type()

    if scheduler_type.lower == 'BlockingScheduler':
        scheduler = BlockingScheduler(jobstores=jobstores, executors=executors, 
                                    job_defaults=job_defaults, timezone=scheduler_time_zone)
    else:
        scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, 
                                    job_defaults=job_defaults, timezone=scheduler_time_zone)
    scheduler.start(paused=get_scheduler_start_paused())
    return scheduler