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

import logging
from typing import Optional, List, Dict, Any
from Databases.connect_to_db import connect_to_database
from Job.alerts import send_alerts

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def generate_sql_command(tests: List[Dict[str, Any]]) -> str:
    sql_commands = []
    for test in tests:
        for table in test['target_tables']:
            for test_detail in test['tests']:
                test_type = test_detail['type']
                if test_type == 'row_count':
                    threshold = test_detail.get('threshold', 1)  # Default threshold is 1
                    sql_commands.append(f"""
                        SELECT 'row_count' AS test_type, '{table}' AS table_name, 
                               COUNT(*) < {threshold} AS error 
                        FROM {table}
                    """)
                elif test_type == 'default_value_check':
                    column = test_detail['column']
                    default_value = test_detail['default_value']
                    sql_commands.append(f"""
                        SELECT 'default_value_check' AS test_type, '{table}' AS table_name, 
                               COUNT(*) > 0 AS error 
                        FROM {table} 
                        WHERE {column} != '{default_value}'
                    """)
                elif test_type == 'primary_key_uniqueness':
                    column = test_detail['column']
                    if isinstance(column, dict):
                        column_name = column.get(table, None)
                        if column_name:
                            sql_commands.append(f"""
                                SELECT 'primary_key_uniqueness' AS test_type, '{table}' AS table_name, 
                                       COUNT(*) > 1 AS error 
                                FROM {table} 
                                GROUP BY {column_name} 
                                HAVING COUNT(*) > 1
                            """)
                    else:
                        sql_commands.append(f"""
                            SELECT 'primary_key_uniqueness' AS test_type, '{table}' AS table_name, 
                                   COUNT(*) > 1 AS error 
                            FROM {table} 
                            GROUP BY {column} 
                            HAVING COUNT(*) > 1
                        """)
                elif test_type == 'foreign_key':
                    foreign_key = test_detail['foreign_key']
                    reference_table = test_detail['reference_table']
                    reference_key = test_detail['reference_key']
                    sql_commands.append(f"""
                        SELECT 'foreign_key' AS test_type, '{table}' AS table_name, 
                               COUNT(*) > 0 AS error 
                        FROM {table} 
                        LEFT JOIN {reference_table} ON {table}.{foreign_key} = {reference_table}.{reference_key} 
                        WHERE {reference_table}.{reference_key} IS NULL
                    """)
                elif test_type == 'null_check':
                    column = test_detail['column']
                    sql_commands.append(f"""
                        SELECT 'null_check' AS test_type, '{table}' AS table_name, 
                               COUNT(*) > 0 AS error 
                        FROM {table} 
                        WHERE {column} IS NULL
                    """)
                elif test_type == 'unique_value_check':
                    column = test_detail['column']
                    sql_commands.append(f"""
                        SELECT 'unique_value_check' AS test_type, '{table}' AS table_name, 
                               COUNT(*) > 1 AS error 
                        FROM {table} 
                        GROUP BY {column} 
                        HAVING COUNT(*) > 1
                    """)
                elif test_type == 'data_range_check':
                    column = test_detail['column']
                    start_date = test_detail['start_date']
                    end_date = test_detail['end_date']
                    sql_commands.append(f"""
                        SELECT 'data_range_check' AS test_type, '{table}' AS table_name, 
                               COUNT(*) > 0 AS error 
                        FROM {table} 
                        WHERE {column} < '{start_date}' OR {column} > '{end_date}'
                    """)
                elif test_type == 'custom_query':
                    query = test_detail['query']
                    sql_commands.append(query)
    return ' UNION ALL '.join(sql_commands)


def data_validate(
    sql_flavour: str,
    auth_method: str,
    secret_name: Optional[str],
    config_file: Optional[str],
    encryption_key: Optional[str],
    oauth_token: Optional[str],
    saml_response: Optional[str],
    error_reporting: Optional[List[Dict[str, Any]]],
    tests: List[Dict[str, Any]]
) -> None:

    conn = connect_to_database(
        sql_flavour=sql_flavour,
        auth_method=auth_method,
        secret_name=secret_name,
        config_file=config_file,
        encryption_key=encryption_key,
        oauth_token=oauth_token,
        saml_response=saml_response
    )

    
    cur = conn.cursor()
    try:
        sql_command = generate_sql_command(tests)
        cur.execute(sql_command)
        results = cur.fetchall()

        error_messages = []
        for result in results:
            test_type, table_name, error = result
            if error:
                error_messages.append(f"Test '{test_type}' failed on table '{table_name}'.")

        if error_messages:
            send_alerts(error_reporting, error_messages)
        else:
            logger.info("All tests passed successfully.")

    except Exception as e:
        logger.error(f"Error running tests: {e}")
    finally:
        cur.close()
        conn.close()