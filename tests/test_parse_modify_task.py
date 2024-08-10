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
from Scheduler.src.modify_task import modify_command


class TestModifyCommand(unittest.TestCase):
    def test_alter_task_resume_suspend(self):
        command = "ALTER TASK my_task RESUME"
        expected = {'task_name': 'my_task', 'action': 'RESUME'}
        result = modify_command(command)
        self.assertEqual(result, expected)

        command = "ALTER TASK my_task SUSPEND"
        expected = {'task_name': 'my_task', 'action': 'SUSPEND'}
        result = modify_command(command)
        self.assertEqual(result, expected)

    def test_alter_task_remove(self):
        command = "ALTER TASK my_task REMOVE AFTER task1, task2"
        expected = {'task_name': 'my_task', 'action': 'REMOVE', 'after': 'task1, task2'}
        result = modify_command(command)
        self.assertEqual(result, expected)

        command = "ALTER TASK my_task REMOVE"
        expected = {'task_name': 'my_task', 'action': 'REMOVE', 'after': None}
        result = modify_command(command)
        self.assertEqual(result, expected)

    def test_alter_task_set(self):
        command = """
        ALTER TASK my_task SET SERVER=my_server
        SCHEDULE='5 MINUTE'
        ALLOW_OVERLAPPING_EXECUTION=TRUE
        """
        expected = {
            'task_name': 'my_task',
            'server': 'my_server',
            'schedule': "'5 MINUTE'",
            'cron_expr': None,
            'time_zone': 'UTC',
            'allow_overlapping_execution': True
        }
        result = modify_command(command)
        self.assertEqual(result, expected)

        command = """
        ALTER TASK my_task SET USING CRON 0 0 * * * UTC
        """
        expected = {
            'task_name': 'my_task',
            'server': None,
            'schedule': None,
            'cron_expr': '0 0 * * *',
            'time_zone': 'UTC',
            'allow_overlapping_execution': None
        }
        result = modify_command(command)
        self.assertEqual(result, expected)

        command = """
        ALTER TASK my_task SET SERVER=my_server
        """
        expected = {
            'task_name': 'my_task',
            'server': 'my_server',
            'schedule': None,
            'cron_expr': None,
            'time_zone': 'UTC',
            'allow_overlapping_execution': None
        }
        result = modify_command(command)
        self.assertEqual(result, expected)

    def test_invalid_command(self):
        with self.assertRaises(ValueError) as cm:
            modify_command("ALTER TASK my_task UNKNOWN_ACTION")
        self.assertEqual(str(cm.exception), "Unknown command type")

        with self.assertRaises(ValueError) as cm:
            modify_command("INVALID COMMAND")
        self.assertEqual(str(cm.exception), "Unknown command type")


if __name__ == "__main__":
    unittest.main()
