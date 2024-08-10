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
from typing import List, Dict, Any, Union
import ast
from Scheduler.src.create_task import parse_command


# Redefine the private function _separate_args_kwargs
def _separate_args_kwargs(input_data: Union[str, List[Any]]) -> Union[List[Any], Dict[Any, Any]]:
    if isinstance(input_data, str):
        try:
            input_data = ast.literal_eval(input_data)
            if isinstance(input_data, tuple):
                args = list(input_data)
                kwargs = {}
                return args, kwargs
            elif isinstance(input_data, list):
                args = input_data
                kwargs = {}
            else:
                args = []
                kwargs = input_data

        except (ValueError, SyntaxError):
            items = [item.strip() for item in input_data.split(',')]
            args = []
            kwargs = {}
            for item in items:
                if '=' in item:
                    key, value = item.split('=', 1)
                    try:
                        kwargs[key.strip()] = ast.literal_eval(value.strip())
                    except (ValueError, SyntaxError):
                        kwargs[key.strip()] = value.strip()
                else:
                    try:
                        args.append(ast.literal_eval(item))
                    except (ValueError, SyntaxError):
                        args.append(item)
            return args, kwargs

    if not isinstance(input_data, list):
        return [], {}

    args = []
    kwargs = {}

    for item in input_data:
        if isinstance(item, str) and '=' in item:
            key, value = item.split('=', 1)
            try:
                kwargs[key.strip()] = ast.literal_eval(value.strip())
            except (ValueError, SyntaxError):
                kwargs[key.strip()] = value.strip()
        else:
            args.append(item)

    return args, kwargs


class TestSeparateArgsKwargs(unittest.TestCase):
    def test_string_with_positional_and_keyword_args(self):
        input_data = "1, 2, key1=value1, key2=3"
        args, kwargs = _separate_args_kwargs(input_data)
        self.assertEqual(args, [1, 2])
        self.assertEqual(kwargs, {'key1': 'value1', 'key2': 3})

    def test_string_with_only_positional_args(self):
        input_data = "1, 2, 3"
        args, kwargs = _separate_args_kwargs(input_data)
        self.assertEqual(args, [1, 2, 3])
        self.assertEqual(kwargs, {})

    def test_string_with_only_keyword_args(self):
        input_data = "key1=value1, key2=2"
        args, kwargs = _separate_args_kwargs(input_data)
        self.assertEqual(args, [])
        self.assertEqual(kwargs, {'key1': 'value1', 'key2': 2})

    def test_list_with_positional_and_keyword_args(self):
        input_data = [1, 2, 'key1=value1', 'key2=2']
        args, kwargs = _separate_args_kwargs(input_data)
        self.assertEqual(args, [1, 2])
        self.assertEqual(kwargs, {'key1': 'value1', 'key2': 2})

    def test_list_with_list_and_keyword_args(self):
        input_data = [[1, 2], 'key1=value1', 'key2=2']
        args, kwargs = _separate_args_kwargs(input_data)
        self.assertEqual(args, [[1, 2]])
        self.assertEqual(kwargs, {'key1': 'value1', 'key2': 2})

    def test_list_with_tuple_and_keyword_args(self):
        input_data = [(1, 2), 'key1=value1', 'key2=2']
        args, kwargs = _separate_args_kwargs(input_data)
        self.assertEqual(args, [(1, 2)])
        self.assertEqual(kwargs, {'key1': 'value1', 'key2': 2})

    def test_list_with_only_positional_args(self):
        input_data = [1, 2, 3]
        args, kwargs = _separate_args_kwargs(input_data)
        self.assertEqual(args, [1, 2, 3])
        self.assertEqual(kwargs, {})

    def test_list_with_only_keyword_args(self):
        input_data = ['key1=value1', 'key2=2']
        args, kwargs = _separate_args_kwargs(input_data)
        self.assertEqual(args, [])
        self.assertEqual(kwargs, {'key1': 'value1', 'key2': 2})

    def test_invalid_string_format(self):
        input_data = "key1=value1, key2=2, invalid"
        args, kwargs = _separate_args_kwargs(input_data)
        self.assertEqual(args, ['invalid'])
        self.assertEqual(kwargs, {'key1': 'value1', 'key2': 2})

    def test_invalid_list_format(self):
        input_data = ['key1=value1', 'key2=2', 'invalid']
        args, kwargs = _separate_args_kwargs(input_data)
        self.assertEqual(args, ['invalid'])
        self.assertEqual(kwargs, {'key1': 'value1', 'key2': 2})


class TestParseCommand(unittest.TestCase):
    def test_valid_command_with_all_fields(self):
        command = """
        CREATE TASK my_task SERVER = 1
        SCHEDULE = '10 MINUTE'
        ALLOW_OVERLAPPING_EXECUTION = TRUE
        AFTER some_task
        AS my_function(arg1, arg2=2)
        """
        action, task_name, params = parse_command(command)
        expected_params = {
            'server': '1',
            'schedule': "'10 MINUTE'",
            'cron_expr': None,
            'time_zone': 'UTC',
            'allow_overlapping_execution': True,
            'after': 'some_task',
            'function': 'my_function',
            'args': ['arg1'],
            'kwargs': {'arg2': 2}
        }
        expected_args = ['arg1']
        expected_kwargs = {'arg2': 2}
        self.assertEqual(action, 'create_task')
        self.assertEqual(task_name, 'my_task')
        self.assertEqual(params, expected_params)
        self.assertEqual(params['args'], expected_args)
        self.assertEqual(params['kwargs'], expected_kwargs)

    def test_valid_command_with_cron_expression(self):
        command = """
        CREATE TASK my_task
        SERVER = 1
        USING CRON 0 12 * * * UTC
        AS my_function(arg1='value')
        """
        action, task_name, params = parse_command(command)
        expected_params = {
            'server': '1',
            'schedule': None,
            'cron_expr': '0 12 * * *',
            'time_zone': 'UTC',
            'allow_overlapping_execution': None,
            'after': None,
            'function': 'my_function',
            'args': [],
            'kwargs': {'arg1': 'value'}
        }
        expected_args = []
        expected_kwargs = {'arg1': 'value'}
        self.assertEqual(action, 'create_task')
        self.assertEqual(task_name, 'my_task')
        self.assertEqual(params, expected_params)
        self.assertEqual(params['args'], expected_args)
        self.assertEqual(params['kwargs'], expected_kwargs)

    def test_invalid_command(self):
        command = "INVALID COMMAND"
        with self.assertRaises(ValueError):
            parse_command(command)


if __name__ == '__main__':
    unittest.main()
