import requests
from bs4 import BeautifulSoup
import time
import urllib.parse

# Groups of URLs, keywords, and recipient numbers with their respective API keys
groups = [
    {# fifi 
        "urls": [
            "https://trouverunlogement.lescrous.fr/tools/36/search?bounds=6.1237188_48.6773463_6.1969256_48.6426683",
            # Add more URLs for this group
        ],
        "keywords": ["charmois"],  # Keywords for this group
        "recipients": [
            {"number": "+33651788036", "api_key": "5311228"},
            {"number": "+33651957889", "api_key": "9664529"},
            # Add more recipients with their API keys for this group
        ]
    },
    
    # Add more groups as needed
]

# Function to send WhatsApp message using CallMeBot
def send_whatsapp_message(message, recipient):
    number = recipient['number']
    api_key = recipient['api_key']
    encoded_message = urllib.parse.quote(message)
    url = f'https://api.callmebot.com/whatsapp.php?phone={number}&text={encoded_message}&apikey={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        print(f"Message sent to {number}.")
    else:
        print(f"Failed to send message to {number}. Status code: {response.status_code}")

def check_keywords_in_html(html_content, keywords, recipients, url):
    soup = BeautifulSoup(html_content, 'html.parser')
    found_keywords = [keyword for keyword in keywords if keyword.lower() in soup.text.lower()]
    
    if found_keywords:
        message = f"Keywords found: {', '.join(found_keywords)} in URL: {url}"
        print(message)
        for recipient in recipients:
            send_whatsapp_message(message, recipient)

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
