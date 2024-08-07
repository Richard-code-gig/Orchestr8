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

import re
from typing import Tuple, Union, Optional, Dict, List, Any
import ast

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
            # Split the string by commas to handle mixed positional and keyword arguments
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
        return [], {} # Technically without eval we only expect a str or list

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

def parse_command(command: str) -> Tuple[str, Optional[str], Optional[Dict[str, Union[str, int, bool]]]]:
    print(command)
    patterns = {
        'create_task': r"""
            \s*CREATE\s+TASK\s+(?P<task_name>\w+)\s*
            \s*SERVER\s*=\s*(?P<server>\w+)\s*
            \s*(?:(?:SCHEDULE\s*=\s*(?P<schedule>'\d+\s+(?:SECOND|MINUTE|HOUR|DAY|WEEK)')|USING\s+CRON\s+(?P<cron_expr>(?:(?:\d+|\*)\s+){4}(?:\d+|\*))\s+(?P<time_zone>\w+))?)\s*
            \s*(?:ALLOW_OVERLAPPING_EXECUTION\s*=\s*(?P<allow_overlapping_execution>TRUE|FALSE))?\s*
            \s*(?:AFTER\s+(?P<after>.*?)\s*)?\s*(?=AS)\s*
            \s*AS\s+(?P<function>\w+)\s*\((?P<args>(?:[^)(]+|\((?:[^)(]+|\([^)(]*\))*\))*)\)\s*
        """
    }

    for action, pattern in patterns.items():
        match = re.match(pattern, command, re.IGNORECASE | re.VERBOSE)
        if match:
            if action == 'create_task':
                params = {
                    'server': match.group('server'),
                    'schedule': match.group('schedule') if match.group('schedule') else None,
                    'cron_expr': match.group('cron_expr'),
                    'time_zone': match.group('time_zone') if match.group('time_zone') else 'UTC',
                    'allow_overlapping_execution': match.group('allow_overlapping_execution') == 'TRUE' if match.group('allow_overlapping_execution') else None,
                    'after': match.group('after') if match.group('after') else None,
                    'function': match.group('function').split('(')[0].strip(),  # Function name
                    'args': match.group('args') if match.group('args') else []  # Arguments    
                }
                
                params['args'], params['kwargs'] = _separate_args_kwargs(params['args'])
                return action, match.group('task_name'), params
        raise ValueError("Invalid command format")