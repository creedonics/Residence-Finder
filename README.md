# Residence Finder

This project is designed to monitor specific URLs for certain keywords and send notifications via WhatsApp and Signal. It tracks consecutive failures for WhatsApp and switches to Signal if needed.

## Project Structure

- `ResCheckAll.py`: The main script that performs the keyword monitoring and sends notifications.
- `monitor_script.sh`: A shell script to monitor and restart the `ResCheckAll.py` script if it stops running.
- `logfile.log`: A log file that records the activities and errors of the `ResCheckAll.py` script.

## Prerequisites

Make sure you have the following installed:

- Python 3.x
- Required Python packages: `requests`, `beautifulsoup4`
- Git
- CallMeBot API keys for WhatsApp and Signal

## Setup Instructions

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/yourusername/yourrepository.git
    cd yourrepository
    ```

2. **Install Python Packages**:

    ```bash
    pip install requests beautifulsoup4
    ```

3. **Configure API Keys**:

    - Get your WhatsApp API key from CallMeBot.
    - Get your Signal API key from CallMeBot.
    - Update the `groups` list in `ResCheckAll.py` with your API keys, phone numbers, and Signal IDs.

4. **Make the Shell Script Executable**:

    ```bash
    chmod +x monitor_script.sh
    ```

5. **Run the Monitor Script**:

    The `monitor_script.sh` script will keep `ResCheckAll.py` running and restart it if it stops.

    ```bash
    ./monitor_script.sh
    ```

## Usage

The `ResCheckAll.py` script checks specified URLs for certain keywords every 5 seconds. If a keyword is found, it sends a notification via WhatsApp. If WhatsApp fails, it immediately tries Signal. After three consecutive WhatsApp failures, it switches to using only Signal for 30 minutes.

### Configuration in `ResCheckAll.py`

- **URLs to Monitor**:
    - Add URLs to the `urls` list in the `groups` dictionary.
  
- **Keywords to Search**:
    - Add keywords to the `keywords` list in the `groups` dictionary.
  
- **Recipients**:
    - Add recipient phone numbers and API keys in the `recipients` list in the `groups` dictionary.

### Sample Configuration

```python
groups = [
    {# Group 1
        "urls": [
            "https://example.com/search?query=residence",
            # Add more URLs
        ],
        "keywords": ["Keyword1", "Keyword2"],  # Keywords to search
        "recipients": [
            {
                "whatsapp_number": "+1234567890",
                "whatsapp_api_key": "your_whatsapp_api_key",
                "signal_id": "your_signal_id",
                "signal_api_key": "your_signal_api_key"
            },
            # Add more recipients
        ]
    },
    # Add more groups as needed
]
```
### Log File

The logfile.log file contains logs of script activities, including:
- Successful and failed message sends
- URLs checked and keywords found
- Any errors encountered

### License

This project is licensed under the MIT License. See the LICENSE file for details.

### Contact

For any issues or questions, please open an issue on GitHub or contact yourname.
