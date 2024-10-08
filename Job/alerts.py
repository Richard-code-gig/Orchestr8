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
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def _mock_send_alert(method, message):
    logger.info(f"Alert sent via {method}: {message}")


def _send_slack_alert(webhook_url, message):
    payload = {
        "text": message
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(webhook_url, headers=headers, json=payload)

    if response.status_code == 200:
        logger.info(f"Alert sent to Slack successfully: {message}")
    else:
        logger.error(f"Failed to send alert to Slack: {response.text}")


def _send_datadog_alert(api_key, endpoint, message):
    payload = {"message": message}
    headers = {"DD-API-KEY": api_key}
    response = requests.post(endpoint, json=payload, headers=headers)
    if response.status_code == 200:
        logger.info(f"Alert sent to Datadog successfully: {message}")
    else:
        logger.error(f"Failed to send alert to Datadog: {response.text}")


def _send_grafana_alert(api_key, endpoint, message):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    payload = {
        'annotations': {
            'summary': message
        }
    }
    response = requests.post(endpoint, json=payload, headers=headers)
    if response.status_code == 200:
        logger.info(f"Alert sent to Grafana successfully: {message}")
    else:
        logger.error(f"Failed to send alert to Grafana: {response.text}")


def send_alerts(error_reporting, messages):
    combined_message = "\n".join(messages)
    for method in error_reporting:
        try:
            if method['method'] == 'slack':
                _send_slack_alert(method['config']['webhook_url'], combined_message)
            elif method['method'] == 'datadog':
                _send_datadog_alert(method['config']['api_key'], method['config']['endpoint'], combined_message)
            elif method['method'] == 'grafana':
                api_key = method['config']['api_key']
                endpoint = method['config']['endpoint']
                _send_grafana_alert(api_key, endpoint, combined_message)
            else:
                _mock_send_alert('mock', combined_message)
        except Exception as e:
            logger.info(f"Error occured: {e}\nDefaulting to Mock alert")
            _mock_send_alert('mock', combined_message)
