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

import logging
import ast
from typing import Dict, Union
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, JobEvent
from .parse_create_task import parse_command
from .job_scheduler import scheduler
from .module_registry import get_function
from datetime import datetime
import pytz

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

sched = scheduler()
task_conditions = {}

def event_listener(event: JobEvent) -> None:
    if event.exception:
        logger.error(f"Job {event.job_id} failed")
    else:
        logger.info(f"Job {event.job_id} executed successfully")

        for task_name, conditions in task_conditions.items():
            job = sched.get_job(task_name)
            if conditions.get('after') and event.job_id in conditions['after'] and not event.exception:
                conditions['after'].remove(event.job_id)
                if not conditions['after']:
                    job = sched.get_job(task_name)

                    # Resume job only if it is paused
                    if job and job.next_run_time is None:
                        time_zone = conditions.get('time_zone', 'UTC')
                        try:
                            tz = pytz.timezone(time_zone)
                        except pytz.UnknownTimeZoneError:
                            logger.error(f"Unknown timezone: {time_zone}. Defaulting to UTC.")
                            tz = pytz.UTC
                        
                        # Convert current time to user's timezone
                        local_time = datetime.now(tz=tz)
                        sched.modify_job(task_name,next_run_time=local_time)

def add_task(task_name: str, params: Dict[str, Union[str, int, bool]]) -> None:
    
    function_name = params['function']
    args = params['args']
    kwargs = params['kwargs']
    max_instances = int(params['server']) if params['server'] else 1
    schedule_num = params.get('schedule')
    cron_expr = params.get('cron_expr')
    time_zone = params.get('time_zone')
    after_tasks = params.get('after')

    task_function = get_function(function_name)

    if after_tasks and (schedule_num or cron_expr):
        raise ValueError("Only one of 'after' or 'schedule' can be used")
    
    # Check if job already exists
    if sched.get_job(task_name):
        logger.info(f"Job {task_name} already exists, skipping addition.")
        return

    trigger = None
    if schedule_num:
        time = schedule_num.split()[0].strip("'").strip('"')
        unit = schedule_num.split()[1].strip("'").strip('"')
        time = int(time)
        if unit.lower().startswith('second'):
            trigger = IntervalTrigger(seconds=time, timezone=time_zone)
        elif unit.lower().startswith('minute'):
            trigger = IntervalTrigger(minutes=time, timezone=time_zone)
        elif unit.lower().startswith('hour'):
            trigger = IntervalTrigger(hours=time, timezone=time_zone)
        elif unit.lower().startswith('day'):
            trigger = IntervalTrigger(days=time, timezone=time_zone)
        elif unit.lower().startswith('week'):
            trigger = IntervalTrigger(weeks=time, timezone=time_zone)
        else:
            raise ValueError("Interval time not recognised")
    elif cron_expr:
        trigger = CronTrigger.from_crontab(cron_expr, timezone=time_zone)

    if after_tasks:
        after_tasks_list = after_tasks.split(', ')
        for task in after_tasks_list:
            if not sched.get_job(task):
                raise ValueError(f"Required task '{task}' does not exist to create and schedule {task_name}.")
            
        task_conditions[task_name] = {'after': after_tasks_list} 

        # To do:
        # For thread safety, set trigger to an hour after the schedule time of latest after task
        # Then reset next_run_time to now in event_lister() if the after task ran
        # This is because when trigger is None next_run_time is None
        # This causes the job to fail as the task is removed causing JobLookUpError
        # checking get_job has not worked well for this

        sched.add_job(task_function, trigger=None, id=task_name, replace_existing=True, args=args, kwargs=kwargs, max_instances=max_instances)
        logger.info(f"Task_id {task_name} added as function {function_name} with args {args} and kwargs {kwargs}, scheduled after {after_tasks_list}")
        try:
            sched.pause_job(task_name)
        except Exception as e:
            logging.warning(f"WARNING: {e}")
    else:
        sched.add_job(task_function, trigger=trigger, id=task_name, replace_existing=True, args=args, kwargs=kwargs, max_instances=max_instances)
        sched.resume_job(task_name)  # task is resumed if no dependencies
        logger.info(f"Task_id {task_name} added as function {function_name} with args {args} and kwargs {kwargs}, scheduled as {trigger}")

def execute_command(command: str) -> None:
    try:
        action, task_name, params = parse_command(command)

        if action == 'create_task':
            add_task(task_name, params)
        else:
            raise ValueError("Unknown action")
    except ValueError as e:
        logger.error(f"Error: {e}")

# Register event listener
sched.add_listener(event_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

if sched.state == 0:  # scheduler is paused
    sched.resume()
    logging.info("Scheduler resumed")