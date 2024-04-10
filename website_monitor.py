import requests
import time
from bs4 import BeautifulSoup
import re
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

def extract_ips(text):
    # Extract IP addresses using regular expression
    ip_pattern = r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
    return re.findall(ip_pattern, text)

def extract_domains(text):
    # Extract domain names using regular expression
    domain_pattern = r"\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b"
    return re.findall(domain_pattern, text)

def extract_files(text):
    # Extract file names using regular expression
    file_pattern = r"\b\w+\.\w+\b"
    return re.findall(file_pattern, text)

while True:
    try:
        # Send a GET request to the web page
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML content of the web page
        soup = BeautifulSoup(response.text, "html.parser")
        current_page_content = str(soup)

        # Check if the web page has been updated
        if current_page_content != previous_page_content:
            # Extract new IP addresses, domain names, and files
            new_ips = set(extract_ips(current_page_content)) - set(extract_ips(previous_page_content))
            new_domains = set(extract_domains(current_page_content)) - set(extract_domains(previous_page_content))
            new_files = set(extract_files(current_page_content)) - set(extract_files(previous_page_content))

            # Send a message to Slack with the new findings
            if new_ips:
                send_slack_message(webhook_url, f"New IP addresses found: {', '.join(new_ips)}")
            if new_domains:
                send_slack_message(webhook_url, f"New domain names found: {', '.join(new_domains)}")
            # if new_files:
            #     send_slack_message(webhook_url, f"New files found: {', '.join(new_files)}")

            # Update the previous page content
            previous_page_content = current_page_content

        # Wait for a certain amount of time before checking again
        time.sleep(30)  # Adjust the interval as needed

    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
        # Handle the error or exit the program
        break
