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
import unittest
from unittest.mock import patch, MagicMock, call
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from Scheduler.src.module_registry import get_function, register_function
from Scheduler.src.create_task import event_listener, add_task, execute_command, task_conditions
from Scheduler.src.job_scheduler import scheduler

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Define a test function to register in the function registry
def test_function():
    assert True

class TestTaskScheduler(unittest.TestCase):
    
    def setUp(self):
        # Register the test function
        register_function('test_function', test_function)

    @patch('Scheduler.src.create_task.logger') # Mock the loger
    def test_event_listener_success(self, mock_logger):
        event = MagicMock()
        event.exception = False
        event.job_id = 'test_task'

        event_listener(event)

        mock_logger.info.assert_called_with('Job test_task executed successfully')

    @patch('Scheduler.src.create_task.logger')
    def test_event_listener_failure(self, mock_logger):
        event = MagicMock()
        event.exception = True
        event.job_id = 'test_task'

        event_listener(event)

        mock_logger.error.assert_called_with('Job test_task failed')

    @patch('Scheduler.src.create_task.sched') # Mock the scheduler
    @patch('Scheduler.src.module_registry.get_function') # Mock the get_function
    @patch('Scheduler.src.create_task.logger')
    def test_add_task_with_schedule(self, mock_logger, mock_get_function, mock_sched):
        # register_function('test_function', test_function)
        
        # Mock the function to return the test_function
        mock_get_function.return_value = test_function

        # Mock add_job and resume_job
        mock_sched.add_job = MagicMock()
        mock_sched.resume_job = MagicMock()
        mock_sched.get_job = MagicMock(return_value=None)

        params = {
            'function': 'test_function',
            'args': [],
            'kwargs': {},
            'server': 1,
            'schedule': '1 minutes',
            'cron_expr': None,
            'time_zone': 'UTC'
        }

        # Run function to be tested
        add_task('test_task', params)

        self.assertTrue(mock_sched.add_job.called, "add_job was not called")

        # Check if add_job was called with the correct trigger
        add_job_call_args = mock_sched.add_job.call_args
        self.assertIsNotNone(add_job_call_args, "add_job call arguments are None")

        trigger_call = add_job_call_args[1]['trigger']

        # Ensure the trigger is an IntervalTrigger
        self.assertIsInstance(trigger_call, IntervalTrigger)

        # Check interval in seconds
        self.assertEqual(trigger_call.interval.total_seconds(), 60)
        self.assertEqual(trigger_call.timezone.zone, 'UTC')

        # Check if resume_job was called once
        mock_sched.resume_job.assert_called_once_with('test_task')

        # Check if logger.info was called with the correct message
        mock_logger.info.assert_called_with(
            "Task_id test_task added as function test_function with args [] and kwargs {}, scheduled as interval[0:01:00]"
        )


    @patch('Scheduler.src.create_task.sched')
    @patch('Scheduler.src.module_registry.get_function') 
    @patch('Scheduler.src.create_task.logger')
    def test_add_task_with_cron(self, mock_logger, mock_get_function, mock_sched):

        mock_sched.add_job = MagicMock()
        mock_sched.resume_job = MagicMock()
        mock_sched.get_job = MagicMock(return_value=None)
        
        add_task('test_task', {
            'function': 'test_function',
            'args': [],
            'kwargs': {},
            'server': '1',
            'cron_expr': '0 0 * * *',
            'time_zone': 'UTC'
        })
        
        # Assert
        mock_sched.add_job.assert_called()
        self.assertIsInstance(mock_sched.add_job.call_args[1]['trigger'], CronTrigger)

    @patch('Scheduler.src.create_task.logger')  # Mock the logger
    @patch('Scheduler.src.create_task.add_task')  # Mock the add_task
    @patch('Scheduler.src.create_task.parse_command')  # Mock the parse_command
    def test_execute_command_create_task(self, mock_parse_command, mock_add_task, mock_logger):
        # Setup
        mock_parse_command.return_value = ('create_task', 'test_task', {
            'function': 'test_function',
            'args': [],
            'kwargs': {},
            'server': '1'
        })
        
        # Run
        execute_command('create_task test_task {}')
        
        # Assert
        mock_add_task.assert_called_once_with('test_task', {
            'function': 'test_function',
            'args': [],
            'kwargs': {},
            'server': '1'
        })
        mock_logger.error.assert_not_called()

    @patch('Scheduler.src.module_registry.get_function')
    @patch('Scheduler.src.create_task.sched')
    @patch('Scheduler.src.create_task.logger')
    def test_add_task_with_after(self, mock_logger, mock_sched, mock_get_function):
        
        mock_get_function.return_value = test_function

        # Mock the scheduler's `get_job` method to return a mock job if 'existing_task' is queried
        mock_sched.get_job.side_effect = lambda job_id: MagicMock() if job_id == 'my_test_task' else None
        mock_sched.add_job = MagicMock()  

        params = {
            'function': 'test_function',
            'args': [],
            'kwargs': {},
            'server': '1',
            'after': 'my_test_task',
            'time_zone': 'UTC'
        }

        add_task('test_task', params)

        # Assert
        self.assertIn('test_task', task_conditions)
        self.assertEqual(task_conditions['test_task']['after'], ['my_test_task'])

        mock_sched.add_job.assert_called_with(
            mock_get_function.return_value,
            trigger=None,
            id='test_task',
            replace_existing=True,
            args=[],
            kwargs={},
            max_instances=1
        )

        # mock_sched.pause_job.assert_called_with('test_task')
        mock_sched.pause_job.assert_called_with('test_task')

        mock_logger.info.assert_called_with(
            "Task_id test_task added as function test_function with args [] and kwargs {}, scheduled after ['my_test_task']"
        )

        # Assert that the job was added
        mock_sched.add_job.assert_called()
        mock_sched.add_job.assert_called_with(test_function, trigger=None, id='test_task', replace_existing=True, args=[], kwargs={}, max_instances=1)
      
    @patch('Scheduler.src.create_task.logger') 
    def test_execute_command_unknown_action(self, mock_logger):

        execute_command('unknown_action test_task')
        
        # Assert
        mock_logger.error.assert_called_with("Error: Invalid command format")

if __name__ == '__main__':
    unittest.main()