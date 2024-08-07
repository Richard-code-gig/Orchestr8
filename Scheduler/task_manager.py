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
import signal
from typing import Optional
import sys
from argparse import ArgumentParser
from src.modify_task import execute_command
from src.job_scheduler import scheduler
from src.utils import get_scheduler_shutdown_wait
from src.job_scheduler import scheduler

scheduler = scheduler()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def signal_handler(signum: int, frame: Optional[object]) -> None:
    """Handle shutdown signals."""
    logger.info('Signal received, shutting down scheduler...')
    scheduler().shutdown(get_scheduler_shutdown_wait())
    sys.exit(0)

def main() -> None:
    """
    Main function to handle command-line arguments and execute commands.
    
    Commands:
    - remove_all_tasks: Removes all scheduled tasks.
    - get_all_tasks: Prints all scheduled tasks.
    - get_task <task_name>: Retrieves details of a specific task.
    """
    parser = ArgumentParser(description='Command-line tool for task management.')
    parser.add_argument('command', type=str, help='The command to execute')
    parser.add_argument('task_name', nargs='?', type=str, help='The name of the task (optional)')
    
    args = parser.parse_args()

    try:
        # Set up signal handling for graceful shutdown
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        input_command = args.command.strip().lower()
        logger.info(f"Command received: {input_command}")

        if input_command.lower() == "remove_all_tasks":
            scheduler.remove_all_jobs()
            logger.info("All tasks removed")
        
        elif input_command.lower() == "get_all_tasks":
            scheduler.print_jobs()

        elif input_command.lower() == "get_task":
            task_name = args.task_name.strip()
            if task_name:
                job = scheduler.get_job(task_name)
                if job:
                    logger.info(f"{task_name} detail is:\n{job}")
                else:
                    logger.info(f"No task found with name {task_name}")
            else:
                logger.error("No task name provided for 'get_task' command")
        else:
            try:
                execute_command(input_command)
            except Exception as e:
                logger.error(f"Failed to execute command: {e}")

    finally:
        logger.info("Exiting the main function")

if __name__ == "__main__":
    main()