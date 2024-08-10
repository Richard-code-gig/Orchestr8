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
from copy import deepcopy
from typing import Optional, Dict
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from .parse_modify_task import modify_command
from .job_scheduler import scheduler

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

scheduler = scheduler()

task_conditions = {}


def _alter_task(params: Dict) -> None:
    task_name = params['task_name']
    job = scheduler.get_job(task_name)

    if not job:
        logger.info(f'Specified job with id {task_name} cannot be found')
        return

    action = params.get('action')
    try:
        action = action.upper()
    except Exception:
        pass

    if action:
        if action == 'RESUME':
            scheduler.resume_job(task_name)
            return
        elif action == 'SUSPEND':
            scheduler.pause_job(task_name)
            return
        elif action == 'REMOVE':
            logger.info("Running action REMOVE")

            if 'after' in params:
                logger.info(f"After in {params}")

                """Remove specified predecessors."""
                predecessors_to_remove = [pred.strip() for pred in params['after'].split(',')]
                predecessors_to_remove_copy = deepcopy(predecessors_to_remove)
                if task_name not in task_conditions:
                    task_conditions[task_name] = {'after': predecessors_to_remove_copy}

                _update_task_graph(task_name)

                predecessors_left = task_conditions[task_name].get('after', [])

                if not predecessors_left:
                    del task_conditions[task_name]['after']
                    logger.info(f"Removed predecessors {predecessors_to_remove} from {task_name}")
                return
            else:
                scheduler.remove_job(task_name)
                return

    if 'schedule' in params or 'cron_expr' in params:
        trigger = None
        if 'schedule' in params and params['schedule']:
            schedule_num = params['schedule']
            time, unit = schedule_num.split()[0].strip("'").strip('"'), schedule_num.split()[1].strip("'").strip('"')
            time = int(time)
            if unit.lower().startswith('second'):
                trigger = IntervalTrigger(seconds=time, timezone=params['time_zone'])
            elif unit.lower().startswith('minute'):
                trigger = IntervalTrigger(minutes=time, timezone=params['time_zone'])
            elif unit.lower().startswith('hour'):
                trigger = IntervalTrigger(hours=time, timezone=params['time_zone'])
            elif unit.lower().startswith('day'):
                trigger = IntervalTrigger(days=time, timezone=params['time_zone'])
            elif unit.lower().startswith('week'):
                trigger = IntervalTrigger(weeks=time, timezone=params['time_zone'])
            else:
                raise ValueError("Interval time not recognized")
        elif 'cron_expr' in params and params['cron_expr']:
            trigger = CronTrigger.from_crontab(params['cron_expr'], timezone=params['time_zone'])

        if trigger:
            try:
                scheduler.modify_job(task_name, trigger=trigger)
            except Exception as e:
                logger.warning(f"Error modifying job schedule: {e}")

    if 'allow_overlapping_execution' in params:
        try:
            max_instances = int(params['allow_overlapping_execution'])
            scheduler.modify_job(task_name, max_instances=max_instances)
        except Exception as e:
            logger.warning(f"Error modifying job max instances: {e}")


def _update_task_graph(task_name: str) -> None:
    """
    Update task graph and handle transitions of tasks becoming standalone or root tasks.
    """
    logger.debug(f"Task Conditions: {task_conditions}")  # Log task_conditions
    if not task_conditions:
        return

    while task_conditions.get(task_name).get('after'):
        task_conditions[task_name]['after'].pop()
    scheduler.pause_job(task_name)
    logger.info(f"Task {task_name} is now a root task and automatically suspended")
    return


def execute_command(command: str) -> None:
    try:
        params = modify_command(command)
        _alter_task(params)

    except ValueError as e:
        logger.error(f"Error: {e}")


if scheduler.state == 0:
    scheduler.resume()
    logging.info("Scheduler resumed")
