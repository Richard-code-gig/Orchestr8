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
function workflows defined in a separate script
"""

import logging
import argparse
import signal
from typing import Optional
import sys
import time
from Scheduler.src.create_task import execute_command
from Scheduler.src.module_registry import register_function
from Scheduler.src.job_scheduler import scheduler
from Scheduler.src.utils import get_scheduler_shutdown_wait, get_parameter_file
from Job.test_context_manager import ConfigManager
from Scheduler.src.job_scheduler import scheduler
from Job.automated_test import data_validate
from Databases.SQLite.scripts.example_loader import run_script

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def signal_handler(signum: int, frame: Optional[object]) -> None:
    """Handle shutdown signals."""
    logger.info('Signal received, shutting down scheduler...')
    scheduler().shutdown(get_scheduler_shutdown_wait())
    sys.exit(0)

register_function('data_validate', data_validate)

def main() -> None:
    run_script()

    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Deploy Snowflake Procedure")
    parser.add_argument('--sql_flavour', type=str, default='sqlite', help="Authentication method: env, secrets_manager, encrypted_file, oauth, or saml")
    parser.add_argument('--auth_method', type=str, default='env', help="Authentication method: env, secrets_manager, encrypted_file, oauth, or saml")
    parser.add_argument('--secret_name', type=str, help="Secret name for AWS Secrets Manager (required for secrets_manager auth method)")
    parser.add_argument('--config_file', type=str, help="Path to the encrypted config file (required for encrypted_file auth method)")
    parser.add_argument('--encryption_key', type=str, help="Encryption key for the encrypted config file (required for encrypted_file auth method)")
    parser.add_argument('--oauth_token', type=str, help="OAuth token (required for oauth auth method)")
    parser.add_argument('--saml_response', type=str, help="SAML response (required for saml auth method)")
    args = parser.parse_args()
    
    try:
        # Set up signal handling for graceful shutdown
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        # Path to the YAML configuration file
        CONFIG_FILE = get_parameter_file()
        
        # Create an instance of ConfigManager
        config_manager = ConfigManager(CONFIG_FILE)

        for task in config_manager.get_tasks():
            arg_value = [
                    args.sql_flavour, args.auth_method,
                    args.secret_name, args.config_file,
                    args.encryption_key, args.oauth_token,
                    args.saml_response, config_manager.get_error_reporting(),
                    task['tests']
            ]
            
            task_name = task['task_name']
            command_run_test = f"""
                CREATE TASK {task_name}
                SERVER = 1
                SCHEDULE = '1 MINUTE'
                AS data_validate({arg_value})
            """
            try:
                while True:
                    execute_command(command_run_test)
                    logger.info("You will get a success alert in console in 1 minute ")
                    logger.info("Press ctrl c to exit")
                    time.sleep(5)
            except (KeyboardInterrupt, SystemExit):
                # Graceful shutdown handled by signal_handler
                pass
    finally:
        logger.info("Exiting the main function")

if __name__ == "__main__":
    main()