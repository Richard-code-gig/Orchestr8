import yaml

class ConfigManager:
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        self.config = self._load_config()
    
    def _load_config(self):
        """Load the YAML configuration file."""
        try:
            with open(self.config_file_path, 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            raise RuntimeError(f"Failed to load configuration file: {e}")
    
    def get_tasks(self):
        """Return the list of tasks from the configuration."""
        return self.config.get('tasks', [])
    
    def get_error_reporting(self):
        """Return the error reporting configuration."""
        return self.config.get('error_reporting', [])
    
    def get_sql_flavour(self):
        """Return the SQL flavour specified in the configuration."""
        return self.config.get('sql_flavour', '')
    
    def get_schedule(self, task_name):
        """Return the schedule for a specific task."""
        tasks = self.get_tasks()
        for task in tasks:
            if task['task_name'] == task_name:
                return task.get('schedule', '')
        return ''
    
    def get_cron_schedule(self, task_name):
        """Return the cron schedule for a specific task."""
        tasks = self.get_tasks()
        for task in tasks:
            if task['task_name'] == task_name:
                return task.get('cron_schedule', '')
        return ''