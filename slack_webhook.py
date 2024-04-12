# Note: this is for testing that your slack webhook is working properly

import requests
import json

def send_slack_message(webhook_url, message):
    payload = {
        "text":message
    }

    response = requests.post(webhook_url, json=payload)

    if response.status_code == 200:
        print("Message sent to Slack.")
    else:
        print(f"Failed to send message to Slack. Status code: {response.status_code}, Response: {response.text}")

# Set the Slack webhook URL
# Load the configuration from the config.json file
with open('config.json') as config_file:
    config = json.load(config_file)

# Get the webhook URL from the configuration
webhook_url = config['webhook']

message = "Testing"

send_slack_message(webhook_url, message)