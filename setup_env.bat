@REM # Copyright 2024 Sola Richard Olorunfemi
@REM # Licensed under the Apache License, Version 2.0 (the "License");
@REM # you may not use this file except in compliance with the License.
@REM # You may obtain a copy of the License at
@REM # 
@REM #     http://www.apache.org/licenses/LICENSE-2.0
@REM # 
@REM # Unless required by applicable law or agreed to in writing, software
@REM # distributed under the License is distributed on an "AS IS" BASIS,
@REM # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
@REM # See the License for the specific language governing permissions and
@REM # limitations under the License.

@echo off

set SCRIPT_PATH_WORKFLOW=%USERPROFILE%\Orchestr8\Scheduler\task_workflow.py
set LINK_PATH_WORKFLOW=C:\Windows\System32\task_workflow.py
set SCRIPT_PATH_MANAGER=%USERPROFILE%\Orchestr8\Scheduler\task_manager.py
set LINK_PATH_MANAGER=C:\Windows\System32\task_manager.py

:: Check if script exists
if not exist "%SCRIPT_PATH_WORKFLOW%" (
    echo Error: %SCRIPT_PATH_WORKFLOW% does not exist.
    exit /b 1
)
if not exist "%SCRIPT_PATH_MANAGER%" (
    echo Error: %SCRIPT_PATH_MANAGER% does not exist.
    exit /b 1
)

:: Create symbolic link
if exist "%LINK_PATH_WORKFLOW%" (
    echo Symbolic link %LINK_PATH_WORKFLOW% already exists.
) else (
    mklink "%LINK_PATH_WORKFLOW%" "%SCRIPT_PATH_WORKFLOW%"
    echo Symbolic link created at %LINK_PATH_WORKFLOW%
)

if exist "%LINK_PATH_MANAGER%" (
    echo Symbolic link %LINK_PATH_MANAGER% already exists.
) else (
    mklink "%LINK_PATH_MANAGER%" "%SCRIPT_PATH_MANAGER%"
    echo Symbolic link created at %LINK_PATH_MANAGER%
)