# Orchestr8

## Overview
This project provides a universal orchestrator for managing tasks across PostgreSQL and Snowflake based on SQL conditions.

## Project Structure
- `Snowflake/` - Contains SQL scripts, configuration files, and task setup for Snowflake.
- `Postgres/` - Contains SQL scripts, configuration files, and task setup for PostgreSQL.
- `main.py` - The main Python script that manages tasks based on SQL conditions.
- `config.json` - Configuration file for setting up the orchestrator.

## Setup
1. Configure the database connection settings in the respective `Snowflake/snowflake_config.json` or `Postgres/postgres_config.json` file.
2. Implement the `update_column` and `checker` functions in the respective databases using the SQL scripts provided in the `scripts/` directory under each database.
3. Customize the `config.json` to include specific logic for each database.
4. Run `main.py` to manage tasks based on conditions.

## Run Instruction
1. Using Environment Variables (Default)
python loader.py
2. Using AWS Secrets Manager
python loader.py --auth_method secrets_manager --secret_name your_secret_name
3. Using Encripted File
python loader.py --auth_method encripted_file --config_file path/to/config.json.enc --encryption_key your_encryption_key
4. Using oAuth Authentication
python deploy_procedure.py --auth_method oauth --oauth_token "<OAUTH_TOKEN>"
5. Using SAML Authentication
python deploy_procedure.py --auth_method saml --saml_response "<SAML_RESPONSE>"

## Usage
- Define SQL conditions and corresponding task management logic.
- Schedule `main.py` to run periodically using a scheduler like cron.

## License
This project is licensed under the MIT License.
