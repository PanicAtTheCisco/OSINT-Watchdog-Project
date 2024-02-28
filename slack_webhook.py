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

webhook_url = 'https://hooks.slack.com/services/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'  # Replace with your Slack webhook URL.

message = "Testing"

send_slack_message(webhook_url, message)