# main.py

import os
import pandas as pd
from tqdm import tqdm

from config import (
    OUTPUT_FILE, ATTACHMENT_DIR, OUTPUT_DIR, LOG_DIR, LOG_LEVEL
)
from utils.graph_api import GraphAPIClient
from utils.email_processor import process_emails
from utils.logger import setup_logging

def main():
    # Ensure directories exist
    for directory in [ATTACHMENT_DIR, OUTPUT_DIR, LOG_DIR]:
        if not os.path.exists(directory):
            os.makedirs(directory)

    # Set up logging
    setup_logging(LOG_LEVEL)

    # Initialize Graph API Client
    client = GraphAPIClient()

    # Authenticate and get access token
    if not client.authenticate():
        print("Authentication failed. Please check your credentials.")
        return

    # Fetch emails
    emails = client.get_emails()

    if not emails:
        print("No emails retrieved.")
        return

    # Process emails and attachments
    email_data = process_emails(emails, client)

    # Save to Excel
    df = pd.DataFrame(email_data)
    df.to_excel(OUTPUT_FILE, index=False)
    print(f"Data successfully saved to {OUTPUT_FILE}")

if __name__ == '__main__':
    main()