import sqlite3

def connect_to_sqlite(auth_method='env', secret_name=None, config_file=None, encryption_key=None, oauth_token=None, saml_response=None):
    conn = sqlite3.connect('example.db')
    return conn
