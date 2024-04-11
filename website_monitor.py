import requests
import time
from bs4 import BeautifulSoup
import re
import json
import validators

def send_slack_message(webhook_url, emails, domains):
    #Get the current date and time
    newDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    payload = {
        "text": "New updates to website!",
        "blocks": [
            {
                "type": "section",
                "block_id": "header",
                'text': {
                    "type": "mrkdwn",
                    "text": ">" + newDate + "\n>`Website:` New updates to `" + url + "`"
                }
            },
            {
                "type": "section",
                "block_id": "emails",
                "text": {
                    "type": "mrkdwn",
                    "text": "`Email Addresses:`\n" + emails
                }
            },
            {
                "type": "section",
                "block_id": "domains",
                "text": {
                    "type": "mrkdwn",
                    "text": "`Domain Names (will be somewhat inaccurate):`\n" + domains
                }
            }
        ]
    }

    response = requests.post(webhook_url, json=payload)

    if response.status_code == 200:
        print("Message sent to Slack.")
    else:
        print(f"Failed to send message to Slack. Status code: {response.status_code}, Response: {response.text}")

# Set the URL of the web page you want to monitor
url = "http://127.0.0.1:5500/test-site/index.html"

# Set the Slack webhook URL
# Load the configuration from the config.json file
with open('config.json') as config_file:
    config = json.load(config_file)

# Get the webhook URL from the configuration
webhook_url = config['webhook']

# Initialize the variable to store the previous version of the web page
previous_page_content = ""

def extract_emails(text):
    # Extract IP addresses using regular expression
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    return re.findall(email_pattern, text)

def extract_domains(text):
    # Extract domain names using validators domain() function
    domains = []
    lines = text.split('\n')
    for line in lines:
        words = line.split()
        for word in words:
            if validators.domain(word) and not word.endswith(('.html', '.htm', '.php', '.asp', '.aspx', '.jsp', '.cgi', '.pl', '.py', '.rb', '.java', '.cpp', '.c', '.cs', '.dll', '.exe', '.jar', '.war', '.zip', '.tar', '.gz', '.rar', '.7z', '.iso', '.img', '.bin', '.dat', '.csv', '.txt', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.pdf')):
                domains.append(word)
    return domains

while True:
    try:
        # Send a GET request to the web page
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML content of the web page
        soup = BeautifulSoup(response.text, "html.parser")
        current_page_content = str(soup)

        emails = ""
        domains = ""

        # Check if the web page has been updated
        if current_page_content != previous_page_content:
            # Extract new IP addresses, domain names, and files
            new_emails = set(extract_emails(current_page_content)) - set(extract_emails(previous_page_content))
            new_domains = set(extract_domains(current_page_content)) - set(extract_domains(previous_page_content))

            # Send a message to Slack with the new findings
            if new_emails:
                emails = "```" + '\n'.join(new_emails) + "```"
            if new_domains:
                domains = "```" + '\n'.join(new_domains) + "```"

            send_slack_message(webhook_url, emails, domains)

            # Update the previous page content
            previous_page_content = current_page_content

        # Wait for a certain amount of time before checking again
        time.sleep(30)  # Adjust the interval as needed

    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
        # Handle the error or exit the program
        break