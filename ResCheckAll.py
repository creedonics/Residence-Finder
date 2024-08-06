import requests
from bs4 import BeautifulSoup
import time
import urllib.parse
from datetime import datetime, timedelta

# Groups of URLs, keywords, and recipient numbers with their respective API keys
groups = [
    {# groupe 1  
        "urls": [
            "https://trouverunlogement.lescrous.fr/tools/36/search?bounds=6.1237188_48.6773463_6.1969256_48.6426683", # link to the CROUS residence in France, Nancy 54500
            # Add more URLs for this group
        ],
        "keywords": ["CHARMOIS"],  # Keywords for this group, CHARMOIS is a CROUS residence that if available, can be found in the link above
        "recipients": [
            {"whatsapp_number": "", "whatsapp_api_key": "", "signal_id": "", "signal_api_key": ""},
            {"whatsapp_number": "", "whatsapp_api_key": "", "signal_id": "", "signal_api_key": ""},
            # Add more recipients with their API keys for this group
        ]
    },
    # Add more groups as needed
]

# Dictionary to track WhatsApp failure counts and timestamps for suspension
failure_tracking = {}

# Function to send WhatsApp message using CallMeBot with retry logic
def send_whatsapp_message(message, recipient, max_retries=1, delay=5):
    number = recipient['whatsapp_number']
    api_key = recipient['whatsapp_api_key']
    encoded_message = urllib.parse.quote(message)
    url = f'https://api.callmebot.com/whatsapp.php?phone={number}&text={encoded_message}&apikey={api_key}'

    for attempt in range(max_retries):
        response = requests.get(url)
        if response.status_code == 200:
            print(f"WhatsApp message sent to {number}.")
            return True
        elif response.status_code == 503:
            print(f"Failed to send WhatsApp message to {number}. Status code: 503. Attempt {attempt + 1} of {max_retries}")
            if attempt < max_retries - 1:
                time.sleep(delay)
        elif response.status_code == 209:
            print(f"Failed to send WhatsApp message to {number}. Status code: 209. Possible issue with API key or message format. No retry.")
            break
        else:
            print(f"Failed to send WhatsApp message to {number}. Status code: {response.status_code}. No retry.")
            break
    return False

# Function to send Signal message using CallMeBot with retry logic
def send_signal_message(message, recipient, max_retries=1, delay=5):
    signal_id = recipient['signal_id']
    api_key = recipient['signal_api_key']
    encoded_message = urllib.parse.quote(message)
    url = f'https://signal.callmebot.com/signal/send.php?phone={signal_id}&text={encoded_message}&apikey={api_key}'

    for attempt in range(max_retries):
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Signal message sent to {signal_id}.")
            return True
        elif response.status_code == 503:
            print(f"Failed to send Signal message to {signal_id}. Status code: 503. Attempt {attempt + 1} of {max_retries}")
            if attempt < max_retries - 1:
                time.sleep(delay)
        else:
            print(f"Failed to send Signal message to {signal_id}. Status code: {response.status_code}. No retry.")
            break
    return False

def send_message(message, recipient):
    now = datetime.now()
    if 'whatsapp_number' in recipient and 'whatsapp_api_key' in recipient:
        whatsapp_key = recipient['whatsapp_number']
        if whatsapp_key not in failure_tracking:
            failure_tracking[whatsapp_key] = {"failures": 0, "suspend_until": now}
        
        if failure_tracking[whatsapp_key]["suspend_until"] <= now:
            whatsapp_sent = send_whatsapp_message(message, recipient)
            if whatsapp_sent:
                failure_tracking[whatsapp_key]["failures"] = 0
                return True
            else:
                failure_tracking[whatsapp_key]["failures"] += 1
                if failure_tracking[whatsapp_key]["failures"] >= 3:
                    failure_tracking[whatsapp_key]["suspend_until"] = now + timedelta(minutes=30)
                send_signal_message(message, recipient)
                return False

    if 'signal_id' in recipient and 'signal_api_key' in recipient:
        return send_signal_message(message, recipient)

    # If Signal is not configured, attempt WhatsApp even if failures have occurred
    if 'whatsapp_number' in recipient and 'whatsapp_api_key' in recipient:
        return send_whatsapp_message(message, recipient)

    return False

def check_keywords_in_html(html_content, keywords, recipients, url):
    soup = BeautifulSoup(html_content, 'html.parser')
    found_keywords = [keyword for keyword in keywords if keyword.lower() in soup.text.lower()]
    
    if found_keywords:
        message = f"Keywords found: {', '.join(found_keywords)} in URL: {url}"
        print(message)
        for recipient in recipients:
            send_message(message, recipient)

def main(groups, interval):
    while True:
        for group in groups:
            urls = group['urls']
            keywords = group['keywords']
            recipients = group['recipients']
            for url in urls:
                # Send an HTTP request to the URL
                response = requests.get(url)
                if response.status_code != 200:
                    print(f"Failed to retrieve the page at {url}. Status code: {response.status_code}")
                    continue

                html_content = response.text
                check_keywords_in_html(html_content, keywords, recipients, url)

        # Wait for the specified interval before reloading the websites
        time.sleep(interval)

if __name__ == "__main__":
    check_interval = 5  # Check every 5 seconds
    main(groups, check_interval)


