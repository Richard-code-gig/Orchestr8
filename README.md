
# Orchestr8

## Overview
Orchestr8 provides a universal orchestrator based on SQL conditions for managing task workflows, specifically designed for data projects.

## Project Structure
- `Databases/{MongoDb, MySql, Postgres, SQLite, Snowflake}/` - Contains SQL scripts, configuration files, and task setups for various databases.
- `Scheduler/src` - Contains the source files for the scheduler.
- `Scheduler/{commands.sql, task_manager.py, task_workflow.py}` - Scripts for creating and managing workflows.
- `tests` - Contains test files for the Orchestr8 program.
- `example_calculator.py` - A simple calculator demonstrating how workflows can be set up and orchestrated.
- `example_test.py` - A simple SQLite database test showing:
  1. How workflows can be orchestrated in the same deployment script.
  2. How Orchestr8 can assist in data validation.

## Setup
### To Run the Example Files
1. Clone the Repository:
    ```sh
    git clone https://github.com/richard-code-gig/Orchestr8.git
    ```
    Or to specify a different path:
    ```sh
    export PACKAGE_PROJECT_DIR='path/to/your/chosen_directory' && \
    git clone https://github.com/richard-code-gig/Orchestr8.git
    ```

2. Navigate to the Project Directory:
    ```sh
    cd Orchestr8
    ```

3. Create a Virtual Environment:
    ```sh
    python -m venv venv
    ```

4. Activate the Virtual Environment:
    - On Windows:
        ```sh
        venv\Scripts\activate
        ```
    - On macOS and Linux:
        ```sh
        source venv/bin/activate
        ```

5. Install the Required Dependencies:
    ```sh
    pip install -r requirements.txt
    ```

6. Set Up Entry Point Scripts:
    - On macOS/Linux:
        - Make the setup script executable:
          ```sh
          chmod +x setup_env.sh
          ```
        - Execute the script to create symbolic links:
          ```sh
          ./setup_env.sh
          ```
        - Enter your password if prompted.
        - Verify by typing `task_workflow` or `task_manager` in a new terminal window.

    - On Windows:
        - Open Command Prompt with administrator privileges and run:
          ```sh
          setup_env.bat
          ```
        - Verify by typing `task_workflow` or `task_manager` in a new Command Prompt window.

7. Configure Scheduler and Settings:
    - Modify settings in `Scheduler/src/SETTINGS.py` as desired.

8. Test the Program:
    - For a simple automated SQLite data workflow:
      ```sh
      python example_test.py
      ```
    - For a simple calculator task workflow:
      ```sh
      python example_calculator.py
      ```
    - You may need to set the Python path:
      ```sh
      export PYTHONPATH=.
      ```

9. Orchestrate New Workflows:
    - Write your python programs code as needed.
    - Import your entry methods in `Scheduler/src/import_file.py`.
    - Define orchestration SQL in `Scheduler/commands.sql`.
    - Run the workflow with:
      ```sh
      cd Orchestr8
      task_workflow Scheduler/commands.sql
      ```
      If the entry point script is not set in line 7 above, use:
      ```sh
      python Scheduler/task_workflow.py Scheduler/commands.sql
      ```

## License
This project is licensed under the Apache-2.0 License.
