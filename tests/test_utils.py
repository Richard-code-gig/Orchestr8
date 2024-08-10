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

import unittest
from unittest.mock import patch, MagicMock
from Scheduler.src.utils import (
    get_setting,
    get_scheduler_type,
    get_import_file,
    get_parameter_file,
    get_commands_file,
    get_misfire_grace_time,
    get_scheduler_start_paused,
    get_scheduler_shutdown_wait,
    get_jobstore_settings,
    get_timezone,
    get_error_log_settings,
    debug_config
)


class TestSettingsFunctions(unittest.TestCase):
    @patch('Scheduler.src.utils.settings', new_callable=MagicMock)
    def test_get_setting(self, mock_settings):
        # Setup mock
        mock_settings.SOME_SETTING = 'some_value'

        # Test retrieval with default value
        self.assertEqual(get_setting('SOME_SETTING', 'default_value'), 'some_value')

    @patch('Scheduler.src.utils.settings', new_callable=MagicMock)
    def test_get_scheduler_type(self, mock_settings):
        """Test retrieval of scheduler type."""
        mock_settings.SCHEDULER_TYPE = 'DaemonScheduler'
        self.assertEqual(get_scheduler_type(), 'DaemonScheduler')

    @patch('Scheduler.src.utils.settings', new_callable=MagicMock)
    def test_import_file(self, mock_settings):
        """Test retrieval of debug configuration."""
        mock_settings.IMPORT_FILE = 'config.py'
        self.assertEqual(get_import_file(), 'config.py')

    @patch('Scheduler.src.utils.settings', new_callable=MagicMock)
    def test_parameter_file(self, mock_settings):
        """Test retrieval of debug configuration."""
        mock_settings.PARAMETER_JSON = 'config.yaml'
        self.assertEqual(get_parameter_file(), 'config.yaml')

    @patch('Scheduler.src.utils.settings', new_callable=MagicMock)
    def test_commands_file(self, mock_settings):
        """Test retrieval of debug configuration."""
        mock_settings.COMMANDS_SQL = 'config.sql'
        self.assertEqual(get_commands_file(), 'config.sql')

    @patch('Scheduler.src.utils.settings', new_callable=MagicMock)
    def test_get_misfire_grace_time(self, mock_settings):
        """Test retrieval of misfire grace time."""
        mock_settings.MISFIRE_GRACE_TIME = 45
        self.assertEqual(get_misfire_grace_time(), 45)

    @patch('Scheduler.src.utils.settings', new_callable=MagicMock)
    def test_get_scheduler_start_paused(self, mock_settings):
        """Test retrieval of scheduler start paused setting."""
        mock_settings.SCHEDULER_START_PAUSED = True
        self.assertEqual(get_scheduler_start_paused(), True)

    @patch('Scheduler.src.utils.settings', new_callable=MagicMock)
    def test_get_scheduler_shutdown_wait(self, mock_settings):
        """Test retrieval of scheduler shutdown wait setting."""
        mock_settings.SCHEDULER_SHUTDOWN_WAIT = False
        self.assertEqual(get_scheduler_shutdown_wait(), False)

    @patch('Scheduler.src.utils.settings', new_callable=MagicMock)
    def test_get_jobstore_settings(self, mock_settings):
        """Test retrieval of jobstore settings."""
        mock_settings.JOBSTORE = 'mysql'
        mock_settings.JOBSTORE_SQLALCHEMY_URL = 'mysql://user:password@localhost/dbname'
        expected_config = {
            'jobstore_type': 'mysql',
            'jobstore_url': 'mysql://user:password@localhost/dbname'
        }
        self.assertEqual(get_jobstore_settings(), expected_config)

    @patch('Scheduler.src.utils.settings', new_callable=MagicMock)
    def test_get_timezone(self, mock_settings):
        """Test retrieval of timezone setting."""
        mock_settings.TIMEZONE = 'America/New_York'
        self.assertEqual(get_timezone(), 'America/New_York')

    @patch('Scheduler.src.utils.settings', new_callable=MagicMock)
    def test_get_error_log_settings(self, mock_settings):
        """Test retrieval of error log settings."""
        mock_settings.ERROR_LOG = 'sqlalchemy'
        mock_settings.ERROR_LOG_SQLALCHEMY_URL = 'mysql://user:password@localhost/error_log_db'
        self.assertEqual(get_error_log_settings(), 'mysql://user:password@localhost/error_log_db')

    @patch('Scheduler.src.utils.settings', new_callable=MagicMock)
    def test_debug_config(self, mock_settings):
        """Test retrieval of debug configuration."""
        mock_settings.DEBUG = True
        self.assertEqual(debug_config(), True)


if __name__ == "__main__":
    unittest.main()
