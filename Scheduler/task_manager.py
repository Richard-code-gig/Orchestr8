import logging
import signal
from typing import Optional
import sys
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
    
    try:
        # Set up signal handling for graceful shutdown
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        if len(sys.argv) < 2:
            raise IndexError("No command provided")

        input_command = sys.argv[1].strip()
        logger.info(input_command)

        if input_command.lower() == "remove_all_tasks":
            scheduler.remove_all_jobs()
            logger.info("All tasks removed")
        
        elif input_command.lower() == "get_all_tasks":
            scheduler.print_jobs()

        elif input_command.lower() == "get_task":
            task_name = sys.argv[2].strip() if len(sys.argv) > 2 else None
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