from Databases.Snowflake.scripts.snow_connect import connect_to_snowflake
from Databases.SQLite.scripts.sqlite_connect import connect_to_sqlite

def connect_to_database(sql_flavour='sqlite', auth_method='env', secret_name=None, config_file=None, encryption_key=None, oauth_token=None, saml_response=None):
    if sql_flavour.lower() == 'sqlite':
        return connect_to_sqlite(auth_method, secret_name, config_file, encryption_key, oauth_token, saml_response)
    elif sql_flavour.lower() == 'snowflake':
        return connect_to_snowflake(auth_method, secret_name, config_file, encryption_key, oauth_token, saml_response)
    else:
        raise ValueError(f"Unsupported sql_flavour: {sql_flavour}")
