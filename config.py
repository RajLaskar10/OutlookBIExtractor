# config.py

import os

# Azure AD App Credentials
CLIENT_ID = ''       # Replace with your Application (client) ID

TENANT_ID = ''       # Replace with your Directory (tenant) ID

# Microsoft Graph API Settings
AUTHORITY_URL = f"https://login.microsoftonline.com/{TENANT_ID}"
GRAPH_API_ENDPOINT = 'https://graph.microsoft.com/v1.0'

# Scopes for Delegated Permissions
SCOPES = ['Mail.Read', 'Mail.ReadWrite', 'User.Read']

# Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ATTACHMENT_DIR = os.path.join(BASE_DIR, 'data', 'attachments')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
LOG_DIR = os.path.join(BASE_DIR, 'logs')

# Output File
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'emails.xlsx')

# Logging Level
LOG_LEVEL = 'ERROR'  # Options: 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'