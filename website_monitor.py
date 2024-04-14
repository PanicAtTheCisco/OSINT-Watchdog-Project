import requests
import time
from bs4 import BeautifulSoup
import re
import json

# Set the URL of the web page you want to monitor
url = "http://127.0.0.1:5500/test-site/index.html"

# Set the Slack webhook URL
# Load the configuration from the config.json file
with open('config.json') as config_file:
    config = json.load(config_file)

# Get the webhook URL from the configuration
webhook_url = config['webhook']

# Set the interval for checking the web page (in seconds)
interval = 60  # Adjust the interval as needed

def send_slack_message(webhook_url, emails, domains):
    #Get the current date and time
    newDate = time.strftime("%m/%d/%Y, %I:%M:%S %p", time.localtime())

    payload = {
        "text": "New updates to website!",
        "blocks": [
            {
                "type": "section",
                "block_id": "header",
                "text": {
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
                    "text": "`Domain Names:`\n" + domains
                }
            }
        ]
    }

    response = requests.post(webhook_url, json=payload)

    if response.status_code == 200:
        print("Message sent to Slack.")
    else:
        print(f"Failed to send message to Slack. Status code: {response.status_code}, Response: {response.text}")

def extract_emails(text):
    # Extract IP addresses using regular expression
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    return re.findall(email_pattern, text)

def extract_domains(text):
    domain_regex = r"(?:[a-z]+\.[a-z]+(?:\.[a-z]+)*)(?!\.[a-z]+)"
    tlds = ['com', 'org', 'net', 'edu', 'gov', 'mil', 'int', 'arpa', 'aero', 'biz', 'coop', 'info', 'museum', 'name', 'pro', 'xyz']  # Add TLDs as needed
    domain_array = re.findall(domain_regex, text, re.IGNORECASE)
    valid_domain_array = [domain for domain in domain_array if domain.split('.')[-1].lower() in tlds]

    return valid_domain_array

def make_wordlist(webhook_url, url, text):
    # Get the current date and time
    newDate = time.strftime("%m/%d/%Y, %I:%M:%S %p", time.localtime())

    # Extract words using regular expression
    word_pattern = r'\b\w+\b'
    stripTrailingSymbols = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
    words = re.findall(word_pattern, re.sub(r'<.*?>', '', text), re.MULTILINE)
    for word in words:
        word.rstrip(stripTrailingSymbols)

    wordlist = ', '.join(words)

    payload = {
        "text": ">" + newDate + "\n>`Website:` Wordlist for `" + url + "`\n`Wordlist:`\n```" + wordlist + "```"
    }

    response = requests.post(webhook_url, json=payload)

    if response.status_code == 200:
        print("Wordlist sent to Slack.")
    else:
        print(f"Failed to send wordlist to Slack. Status code: {response.status_code}, Response: {response.text}")

def main():
    # Initialize the variable to store the previous version of the web page
    previous_page_content = ""

    made_wordlist = False

    while True:
        try:
            # Send a GET request to the web page
            response = requests.get(url)
            response.raise_for_status()

            # Parse the HTML content of the web page
            soup = BeautifulSoup(response.text, "html.parser")
            current_page_content = str(soup)

            if made_wordlist == False:
                # Initialize the wordlist
                make_wordlist(webhook_url, url, current_page_content)
                made_wordlist = True

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
            time.sleep(interval)  # Adjust the interval as needed

        except requests.exceptions.RequestException as e:
            print("An error occurred:", e)
            # Handle the error or exit the program
            break

main()