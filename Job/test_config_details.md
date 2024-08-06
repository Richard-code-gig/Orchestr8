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