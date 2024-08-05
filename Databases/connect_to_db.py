from Databases.Snowflake.scripts.snow_connect import connect_to_snowflake

def connect_to_database(sql_flavour='snowflake', auth_method='env', secret_name=None, config_file=None, encryption_key=None, oauth_token=None, saml_response=None):
    if sql_flavour.lower() == 'snowflake':
        return connect_to_snowflake(auth_method, secret_name, config_file, encryption_key, oauth_token, saml_response)
    else:
        raise ValueError(f"Unsupported sql_flavour: {sql_flavour}")
