# Orchestr8

## Overview
This project provides a universal orchestrator for managing tasks workflows specifically for data projects based on SQL conditions.

## Project Structure
- `Databases/{MongoDb, MySql, Postgres, Snowflake}/` - Contains SQL scripts, configuration files, and task setup for some databases.
- `Scheduler/src` Contains the scheduler source files.
- `Scheduler/{commands.sql, task_manager.py, task_workflow.py}` Scripts to create and manage workflows.
- `tests` - Contains test files for the Orchestrate program.
- `example_same_script.py` - Example file showing how workflows can be setup and orchestrated on same deployment script.

## Setup
### To run the example files given
1. Write python programs (the supplied `Job` directory is recommended) as you would do without orchestration.
2. Import your program entry point methods in `Scheduler/src/import_file.py` file.
3. Write orchestration code in SQL template in `Scheduler/commands.sql` file.
4. Install python modules [for MacOs]:
```sh
cd Orchestr8
python3 -m venv venv
source venv/bin/activate
pip -r requiremnets.txt
```
5. Run workflow [using the example file given]:
   On same script
```sh
cd Orchestr8
export PYTHONPATH=.
python3 example_same_script.py`
```
   On different script
```sh
cd Orchestr8
export PYTHONPATH=.
python3 Scheduler/task_workflow.py `Scheduler/commands.sql`
```
6. Run integrated tests:
```sh
cd Orchestr8
export PYTHONPATH=.
pytest tests`
```
## License
This project is licensed under the MIT License.
