#!/bin/sh

# Copyright 2024 Sola Richard Olorunfemi
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

SCRIPT_PATH_WORKFLOW="$HOME/Orchestr8/Scheduler/task_workflow.py"
LINK_PATH_WORKFLOW="/usr/local/bin/task_workflow"
SCRIPT_PATH_MANAGER="$HOME/Orchestr8/Scheduler/task_manager.py"
LINK_PATH_MANAGER="/usr/local/bin/task_manager"

# Check if scripts exists
if [ ! -f "$SCRIPT_PATH_WORKFLOW" ]; then
    echo "Error: $SCRIPT_PATH_WORKFLOW does not exist."
    exit 1
fi

if [ ! -f "$SCRIPT_PATH_MANAGER" ]; then
    echo "Error: $SCRIPT_PATH_MANAGER does not exist."
    exit 1
fi

# Create symbolic link
if [ -L "$LINK_PATH_WORKFLOW" ]; then
    echo "Symbolic link $LINK_PATH_WORKFLOW already exists."
else
    sudo ln -s "$SCRIPT_PATH_WORKFLOW" "$LINK_PATH_WORKFLOW"
    echo "Symbolic link created at $LINK_PATH_WORKFLOW"
fi

if [ -L "$LINK_PATH_MANAGER" ]; then
    echo "Symbolic link $LINK_PATH_MANAGER already exists."
else
    sudo ln -s "$SCRIPT_PATH_MANAGER" "$LINK_PATH_MANAGER"
    echo "Symbolic link created at $LINK_PATH_MANAGER"
fi