import requests

def send_slack_message(webhook_url, message):
    payload = {
        "text":message
    }

    response = requests.post(webhook_url, json=payload)

    if response.status_code == 200:
        print("Message sent to Slack.")
    else:
        print(f"Failed to send message to Slack. Status code: {response.status_code}, Response: {response.text}")

webhook_url = ''  # Add your Slack webhook URL here.

message = "Testing"

send_slack_message(webhook_url, message)