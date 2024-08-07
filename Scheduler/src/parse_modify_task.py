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
from typing import Union, Optional, Dict

def _determine_command_type(command: str) -> str:
    """
    Determine the type of the ALTER TASK command.
    """
    
    command = command.upper()

    if 'RESUME' in command or 'SUSPEND' in command:
        return 'alter_task_resume_suspend'
    elif 'REMOVE' in command:
        return 'alter_task_remove'
    elif 'SET' in command:
        return 'alter_task_set'
    else:
        return 'unknown'

def modify_command(command: str) -> Optional[Dict[str, Union[str, int, bool]]]:

    # Define patterns for `ALTER TASK` commands
    patterns = {
        'alter_task_resume_suspend': r"""
            \s*ALTER\s+TASK\s+(?P<task_name>\w+)\s+(?P<action>RESUME|SUSPEND)\s*
        """,
        
        'alter_task_remove': r"""
            \s*ALTER\s+TASK\s+(?P<task_name>\w+)\s+(?P<action>REMOVE)(?:\s+AFTER\s+(?P<after>[^,]+(?:\s*,\s*[^,]+)*))?\s*
        """,
        
        'alter_task_set': r"""
            \s*ALTER\s+TASK\s+(?P<task_name>\w+)\s+SET\s*
            (?:\s*SERVER\s*=\s*(?P<server>\w+)\s*)?
            \s*(?:(?:SCHEDULE\s*=\s*(?P<schedule>'\d+\s+(?:SECOND|MINUTE|HOUR|DAY|WEEK)')|USING\s+CRON\s+(?P<cron_expr>(?:(?:\d+|\*)\s+){4}(?:\d+|\*))\s+(?P<time_zone>\w+))?)\s*
            (?:\s*ALLOW_OVERLAPPING_EXECUTION\s*=\s*(?P<allow_overlapping_execution>TRUE|FALSE)\s*)?
        """
    }

    command_type = _determine_command_type(command)
    
    # If the command type is unknown, raise an error
    if command_type == 'unknown':
        raise ValueError("Unknown command type")

    pattern = patterns.get(command_type)

    # Match the command against the selected pattern
    match = re.match(pattern, command, re.IGNORECASE | re.VERBOSE)
    
    if match:
        params = {'task_name': match.group('task_name')}
        
        if command_type == 'alter_task_resume_suspend':
            params['action'] = match.group('action')
            return params
            
        elif command_type == 'alter_task_remove':
            params['action'] = 'REMOVE'
            params['after'] = match.group('after') if match.group('after') else None
            return params
            
        elif command_type == 'alter_task_set':
            params['server'] = match.group('server') if match.group('server') else None
            params['schedule'] = match.group('schedule') if match.group('schedule') else None
            params['cron_expr'] = match.group('cron_expr') if match.group('cron_expr') else None
            params['time_zone'] = match.group('time_zone') if match.group('time_zone') else 'UTC'
            params['allow_overlapping_execution'] = match.group('allow_overlapping_execution') == 'TRUE' if match.group('allow_overlapping_execution') else None
            return params
    
    raise ValueError("Invalid command format")