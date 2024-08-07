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

# Example test config file

## Explanation of the test YAML Configuration:

## Tests Configuration:
The tests section includes an array of test configurations for different target tables.
Each test configuration contains a list of target_tables and a corresponding list of tests.
Each test can specify its type and additional parameters required for that specific test.

## Error Reporting Configuration:
The error_reporting section defines different methods for reporting errors.
Each method includes a config section for necessary configurations such as webhook URLs or API keys.

## Schedule and Task Configuration:
The schedule section defines the cron schedule for running the tests. Here, it is set to run every hour.
The task_name and warehouse are specified for the Snowflake task configuration.

## Test Types and Parameters:
row_count: Checks the row count of the table.
default_value_check: Ensures a column has a default value.
primary_key_uniqueness: Checks for uniqueness in the primary key column.
foreign_key: Validates foreign key relationships.
null_check: Ensures a column does not contain NULL values.
custom_query: Runs a custom SQL query provided by the user.
unique_value_check: Ensures a column contains unique values.
data_range_check: Checks if the data in a column falls within a specified range.