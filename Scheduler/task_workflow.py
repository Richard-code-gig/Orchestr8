import os
import logging
import signal
from typing import Optional
import sys
import time
from Scheduler.src.create_task import execute_command
from Scheduler.src.module_registry import register_function
from Scheduler.src.job_scheduler import scheduler
from Scheduler.src.utils import get_scheduler_shutdown_wait, get_import_file
from Scheduler.src.job_scheduler import scheduler

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def signal_handler(signum: int, frame: Optional[object]) -> None:
    """Handle shutdown signals."""
    logger.info('Signal received, shutting down scheduler...')
    # scheduler().shutdown(get_scheduler_shutdown_wait())
    sys.exit(0)

def load_and_register_modules(config_file: str) -> None:
    """Load modules and register functions specified in the configuration file."""
    with open(config_file, 'r') as file:
        lines = [line.strip() for line in file if line.strip() and not line.startswith('#')]
    
    for line in lines:
        try:
            exec(line, globals())
            # Extract function or module.function name for registration
            if line.startswith('from '):
                # from module import function
                parts = line.split()
                if len(parts) == 4 and parts[0] == 'from' and parts[2] == 'import':
                    method_name = parts[3]
                    # Register the function
                    if method_name in globals():
                        register_function(method_name, globals()[method_name])
                        logger.info(f"Successfully registered function: {method_name}")
                    else:
                        logger.error(f"Method {method_name} not found in globals after import.")
                else:
                    logger.error(f"Invalid import statement format: {line}")
            elif line.startswith('import '):
                # import module.function
                parts = line.split()
                if len(parts) == 2 and parts[0] == 'import':
                    module_function = parts[1]
                    module_name, function_name = module_function.rsplit('.', 1)
                    if function_name in globals():
                        register_function(function_name, globals()[function_name])
                        logger.info(f"Successfully registered function: {function_name}")
                    else:
                        exec(f'from {module_name} import {function_name}', globals())
                        if function_name in globals():
                            register_function(function_name, globals()[function_name])
                            logger.info(f"Successfully registered function: {function_name}")
                        else:
                            logger.error(f"Function {function_name} not found after import.")
                else:
                    logger.error(f"Invalid import statement format: {line}")
            else:
                logger.error(f"Unrecognized import statement format: {line}")
        except Exception as e:
            logger.error(f"Error executing import statement {line}: {e}")

def read_input(source: str) -> str:
    """
    Reads input from a string or a file path.

    Args:
        source (str): A string which could be a file path or direct input.

    Returns:
        str: The content read from the source.

    Raises:
        RuntimeError: If there is an error reading the file.
    """
    # Check if the source is a file path
    if os.path.isfile(source):
        try:
            with open(source, 'r') as file:
                return file.read().strip()
        except IOError as e:
            raise RuntimeError(f"Error reading file {source}: {e}")
    else:
        # Assume it's a string
        return source.strip()
    
def main():
    try:
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        load_and_register_modules(get_import_file())

        if len(sys.argv) != 2:
            logging.error("Usage: python parse.py <string_or_file_path>")
            sys.exit(1)

        source = sys.argv[1]

        if not source:
            logging.error("Error: No input provided")
            sys.exit(1)

        try:
            input_content = read_input(source)
            commands = input_content.splitlines() 
            for input_command in commands:
                execute_command(input_command)
            time.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            # Graceful shutdown handled by signal_handler
            pass

    finally:
            logger.info("Exiting the main function")

if __name__ == "__main__":
    main()