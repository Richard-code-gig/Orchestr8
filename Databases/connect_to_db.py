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

from Databases.Snowflake.scripts.snow_connect import connect_to_snowflake
from Databases.SQLite.scripts.sqlite_connect import connect_to_sqlite

def connect_to_database(sql_flavour='sqlite', auth_method='env', secret_name=None, config_file=None, encryption_key=None, oauth_token=None, saml_response=None):
    if sql_flavour.lower() == 'sqlite':
        return connect_to_sqlite(auth_method, secret_name, config_file, encryption_key, oauth_token, saml_response)
    elif sql_flavour.lower() == 'snowflake':
        return connect_to_snowflake(auth_method, secret_name, config_file, encryption_key, oauth_token, saml_response)
    else:
        raise ValueError(f"Unsupported sql_flavour: {sql_flavour}")
