import unittest
from unittest.mock import patch, MagicMock, call
from Scheduler.src.modify_task import _alter_task, execute_command, _update_task_graph, task_conditions
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

class TestSchedulerFunctions(unittest.TestCase):

    def setUp(self):
        # Set up mock scheduler
        self.mock_scheduler = MagicMock()
        self.mock_scheduler.get_job = MagicMock()
        self.mock_scheduler.resume_job = MagicMock()
        self.mock_scheduler.pause_job = MagicMock()
        self.mock_scheduler.remove_job = MagicMock()
        self.mock_scheduler.modify_job = MagicMock()

        # Patch the scheduler with mock
        patch('Scheduler.src.modify_task.scheduler', self.mock_scheduler).start()

        # Set up task_conditions
        self.mock_task_conditions = {}

        patch('Scheduler.src.modify_task.task_conditions', self.mock_task_conditions).start()

    def tearDown(self):
        patch.stopall()

    def test_alter_task_resume(self):
        self.mock_scheduler.get_job.return_value = MagicMock()  # Simulate a found job
        params = {'task_name': 'task1', 'action': 'RESUME'}
        _alter_task(params)
        self.mock_scheduler.resume_job.assert_called_with('task1')

    def test_alter_task_suspend(self):
        self.mock_scheduler.get_job.return_value = MagicMock()  # Simulate a found job
        params = {'task_name': 'task2', 'action': 'SUSPEND'}
        _alter_task(params)
        self.mock_scheduler.pause_job.assert_called_with('task2')
    
    def test_alter_task_remove(self):
        self.mock_scheduler.get_job.return_value = MagicMock()  # Simulate a found job
        params = {'task_name': 'task3', 'action': 'REMOVE'}
        _alter_task(params)
        self.mock_scheduler.remove_job.assert_called_with('task3')

    def test_alter_task_remove_after(self):
        self.mock_task_conditions['task3'] = {'after': ['task4', 'task5']}
        params = {'task_name': 'task3', 'action': 'REMOVE', 'after': 'task4, task5'}
        _alter_task(params)

        # Check if task's 'after' key is removed when empty
        self.assertNotIn('after', self.mock_task_conditions['task3'])
        self.assertEqual({'task3': {}}, self.mock_task_conditions)
        
        # Check if the _update_task_graph is called properly
        self.mock_scheduler.pause_job.assert_called_with('task3')

    def test_alter_task_interval_schedule(self):
        self.mock_scheduler.get_job.return_value = MagicMock()
        params = {'task_name': 'task4', 'schedule': "'2 MINUTE'", 'time_zone': 'UTC'}
        _alter_task(params)

        alter_job_call_args = self.mock_scheduler.modify_job.call_args
        trigger_call = alter_job_call_args[1]['trigger']

        self.assertIsInstance(trigger_call, IntervalTrigger)
        self.assertTrue(self.mock_scheduler.modify_job.called, "modify_job was not called")
        self.assertEqual(trigger_call.interval.total_seconds(), 120)
        self.assertEqual(trigger_call.timezone.zone, 'UTC')

    def test_alter_task_cron_schedule(self):
        self.mock_scheduler.get_job.return_value = MagicMock() 
        params = {'task_name': 'task5', 'cron_expr': '0 0 * * *', 'time_zone': 'UTC'}
        _alter_task(params)
        
        # Extract the actual arguments passed to modify_job
        actual_call_args = self.mock_scheduler.modify_job.call_args
        actual_task_name = actual_call_args[0][0]
        actual_trigger = actual_call_args[1]['trigger']
        
        # Create expected trigger
        expected_trigger = CronTrigger.from_crontab('0 0 * * *', timezone='UTC')
        
        self.assertTrue(self.mock_scheduler.modify_job.called, "modify_job was not called")
       
        # Assert 'task5' was passed as the first argument
        self.assertEqual(actual_task_name, 'task5', 
                     f"Expected task name 'task5', but got '{actual_task_name}'")

        self.assertEqual(str(actual_trigger), str(expected_trigger))

    def test_alter_task_allow_overlapping_execution(self):
        self.mock_scheduler.get_job.return_value = MagicMock()  # Simulate a found job
        params = {'task_name': 'task6', 'allow_overlapping_execution': '3'}
        _alter_task(params)
        self.mock_scheduler.modify_job.assert_called_with('task6', max_instances=3)

    def test_update_task_graph(self):
        self.mock_task_conditions['task3'] = {'after': ['task7','task8']}
        _update_task_graph('task3')

        self.assertNotIn('task7', self.mock_task_conditions)
        self.assertNotIn('task8', self.mock_task_conditions)
        self.mock_scheduler.pause_job.assert_called_with('task3')

    def test_execute_command(self):
        command = "ALTER TASK task1 SET SCHEDULE = '5 MINUTE' USING CRON 0 0 * * *"
        with patch('Scheduler.src.modify_task.modify_command', return_value={
            'task_name': 'task1',
            'schedule': "'5 MINUTE'",
            'cron_expr': '0 0 * * *',
            'time_zone': 'UTC'
        }):
            _alter_task = MagicMock()
            with patch('Scheduler.src.modify_task._alter_task', _alter_task):
                execute_command(command)
                _alter_task.assert_called_once_with({
                    'task_name': 'task1',
                    'schedule': "'5 MINUTE'",
                    'cron_expr': '0 0 * * *',
                    'time_zone': 'UTC'
                })

if __name__ == '__main__':
    unittest.main()
