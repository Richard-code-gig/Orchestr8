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

import os
import sys
from pathlib import Path

def get_user_settings_dir() -> Path:
    # Get user-specified directory. Default to ~/Orchestr8/Scheduler/src
    settings_dir = os.getenv('PACKAGE_PROJECT_DIR', os.path.expanduser('~/Orchestr8/Scheduler/src'))
    settings_path = Path(settings_dir)
    return settings_path

def load_user_settings():
    user_settings_file = get_user_settings_dir() / 'SETTINGS.py'
    
    if user_settings_file.exists():
        sys.path.insert(0, str(user_settings_file.parent))
        settings = __import__('SETTINGS')
        sys.path.pop(0)
        return settings
    else:
        raise FileNotFoundError(f"User settings file not found at {user_settings_file}")

# Load the settings once and make them available as module-level variables
settings = load_user_settings()
COMMANDS_SQL = settings.COMMANDS_FILE
PARAMETER_JSON = settings.PARAMETERS_FILE
IMPORT_FILE = settings.IMPORT_FILE
SCHEDULER_TYPE = getattr(settings, 'SCHEDULER_TYPE', 'BackgroundScheduler')
MISFIRE_GRACE_TIME = getattr(settings, 'MISFIRE_GRACE_TIME', 30)
SCHEDULER_START_PAUSED = getattr(settings, 'SCHEDULER_START_PAUSED', False)
SCHEDULER_SHUTDOWN_WAIT = getattr(settings, 'SCHEDULER_SHUTDOWN_WAIT', False)
JOBSTORE = getattr(settings, 'JOBSTORE', None)
JOBSTORE_SQLALCHEMY_URL = getattr(settings, 'JOBSTORE_SQLALCHEMY_URL', None)
TIMEZONE = getattr(settings, 'TIMEZONE', 'UTC')
ERROR_LOG = getattr(settings, 'ERROR_LOG', 'sqlite')
ERROR_LOG_SQLITE_URL = getattr(settings, 'ERROR_LOG_SQLITE_URL', 'sqlite:///error_log.sqlite')
ERROR_LOG_SQLALCHEMY_URL = getattr(settings, 'ERROR_LOG_SQLALCHEMY_URL', '')
DEBUG = getattr(settings, 'DEBUG', False)
WORKSTATION = getattr(settings, 'WORKSTATION', {})