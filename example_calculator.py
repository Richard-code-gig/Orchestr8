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

"""Example showing how to use Orchestr8 to orchestrate 
function workflows defined in the same script that runs the commands
"""
import logging
import signal
from typing import Optional
import sys
import time
from Scheduler.src.create_task import execute_command
from Scheduler.src.module_registry import register_function
from Scheduler.src.job_scheduler import scheduler
from Scheduler.src.utils import get_scheduler_shutdown_wait

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def signal_handler(signum: int, frame: Optional[object]) -> None:
    """Handle shutdown signals."""
    logger.info('Signal received, shutting down scheduler...')
    # scheduler().shutdown(get_scheduler_shutdown_wait())
    sys.exit(0)

# Example task functions
def plus_task(a, b):    
    result = a+b
    logging.info(f"Result of plus({a}, {b}): {result}")
    return a + b

def minus_task(a, b, c):
    result = a-b-c
    logging.info(f"Result of minus({a}, {b}, {c}): {result}")
    return a-b-c

def times_task(a, b):
    result = a*b
    logging.info(f"Result of times({a}, {b}): {result}")
    return a * b

def divides_task(a, b):
    result = a/b
    logging.info(f"Result of divides({a}, {b}): {result}")
    return a / b

def plusminus_task(a, b, c):
    result = a+b - c
    logging.info(f"Result of some_task({a}, {b}, {c}): {result}")
    return a + b - c

# Register the functions dynamically
register_function('plus', plus_task)
register_function('minus', minus_task)
register_function('times', times_task)
register_function('divides', divides_task)
register_function('some_task', plusminus_task)

# Example schedule command
minus_command = """
    CREATE TASK minus_task
    SERVER = 1
    SCHEDULE = '1 MINUTE'
    AS minus_task(7, b=3, c=2)
"""

times_command = """
    CREATE TASK times_task
    SERVER = 1
    SCHEDULE = '1 MINUTE'
    AS times_task(a=1, b=2)
"""

# Example command with AFTER clause
divides_command = """
    CREATE TASK divides_task
    SERVER = 3
    AFTER plus, minus
    AS divides_task(12, 6)
"""

sometask_command = """
    CREATE TASK plusminus_task
    SERVER = 4
    AFTER times_task
    AS plusminus_task(4, 6, 7)
"""

def main():
    try:
        # Set up signal handling for graceful shutdown
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        while True:
            execute_command(minus_command)
            execute_command(times_command)
            # execute_command(divides_command)
            execute_command(sometask_command)
            time.sleep(1)
            
    except (KeyboardInterrupt, SystemExit):
        # Graceful exit handled by signal_handler
        pass

    finally:
        logger.info("Exiting the main function")

if __name__ == "__main__":
    main()