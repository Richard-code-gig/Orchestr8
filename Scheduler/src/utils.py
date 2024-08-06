import importlib

# Load settings module dynamically
settings = importlib.import_module('Scheduler.src.config')

def get_setting(name:str, default=None) -> str:
    """Retrieve a setting value from the settings module."""
    return getattr(settings, name, default)

def get_scheduler_type():
    """Get the type of scheduler."""
    return get_setting('SCHEDULER_TYPE', 'BackgroundScheduler')

def get_import_file():
    """Get the type of scheduler."""
    return get_setting('IMPORT_FILE', 'Scheduler/src/import_file.py')

def get_parameter_file():
    """Get parameter file for automated tests."""
    return get_setting('PARAMETER_JSON', 'Job/test_parameter.json')

def get_commands_file():
    """Get commands file for sql template automation."""
    return get_setting('COMMANDS_SQL', 'Scheduler/commands.sql')

def get_misfire_grace_time():
    """Get the grace time for misfires."""
    return get_setting('MISFIRE_GRACE_TIME', 30)

def get_scheduler_start_paused():
    """Check if the scheduler should start in a paused state."""
    return get_setting('SCHEDULER_START_PAUSED', False)

def get_scheduler_shutdown_wait():
    """Check if the scheduler should wait for jobs to complete on shutdown."""
    return get_setting('SCHEDULER_SHUTDOWN_WAIT', False)

def get_jobstore_settings():
    """Get the jobstore configuration."""
    jobstore_config = {}
    jobstore_config['jobstore_type'] = get_setting('JOBSTORE')
    jobstore_config['jobstore_url'] = get_setting('JOBSTORE_SQLALCHEMY_URL')
    return jobstore_config

def get_timezone():
    """Get the timezone setting."""
    return get_setting('TIMEZONE', 'UTC')

def get_error_log_settings():
    """Get the error log configuration."""
    error_log = get_setting('ERROR_LOG', 'sqlite')
    if error_log == 'sqlite':
        return get_setting('ERROR_LOG_SQLITE_URL', 'sqlite:///error_log.sqlite')
    elif error_log == 'sqlalchemy':
        return get_setting('ERROR_LOG_SQLALCHEMY_URL', '')
    return ''

def debug_config():
    """Get external workstation configuration."""
    return get_setting('DEBUG', False)