import os
import shutil
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_user_settings_dir() -> Path:
    settings_dir = os.getenv('PACKAGE_PROJECT_DIR', os.path.expanduser('~/Orchestr8/Scheduler/src'))
    settings_path = Path(settings_dir)

    if not settings_path.exists():
        logger.info(f"Creating settings directory at {settings_path}")
        settings_path.mkdir(parents=True, exist_ok=True)

    return settings_path

def copy_default_settings():
    user_settings_dir = get_user_settings_dir()
    default_settings_file = Path(__file__).resolve().parent / 'SETTINGS.py'
    user_settings_file = user_settings_dir / 'SETTINGS.py'

    if not user_settings_file.exists():
        logger.info(f"Copying default settings to {user_settings_file}")
        shutil.copy(default_settings_file, user_settings_file)

# Copy the settings file during the first run
copy_default_settings()