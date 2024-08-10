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

from pathlib import Path

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

IMPORT_FILE = 'Scheduler/src/import_file.py'

COMMANDS_FILE = 'Scheduler/commands.sql'

PARAMETERS_FILE = 'Job/test_parameter.yaml'

# [SCHEDULER_SETTINGS]
SCHEDULER_TYPE = 'BackgroundScheduler'  # Option: BlockingScheduler

MISFIRE_GRACE_TIME = 30  # Grace time in seconds for handling misfires

SCHEDULER_START_PAUSED = False  # Whether to start the scheduler in a paused state

SCHEDULER_SHUTDOWN_WAIT = True  # (should be True). Whether to wait for jobs to complete on shutdown

# [JOBSTORE_SETTINGS]
JOBSTORE = 'sqlite'  # Option: relational databases

JOBSTORE_SQLALCHEMY_URL = 'sqlite:///jobs.sqlite'  # E.g 'mysql://user:password@localhost/dbname'

# [DATETIME_SETTINGS]
TIMEZONE = 'UTC'

# [ERROR_SETTINGS]
DEBUG = False  # Change to True to get debugging error during development

ERROR_LOG = 'sqlite'

ERROR_LOG_SQLITE_URL = 'sqlite:///error_log.sqlite'

ERROR_LOG_SQLALCHEMY_URL = ''

# People who get code error notifications. In the format
# [('Full Name', 'email@example.com'), ('Full Name', 'anotheremail@example.com')]
ADMINS = []

# Local time zone for job runs. When USE_LTZ is True, this is
# interpreted as the default user time zone.
TIME_ZONE = "UTC"
