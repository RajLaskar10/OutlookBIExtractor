# Outlook Email Extractor

## Overview

This project allows you to access your Outlook mailbox online, read emails and attachments, and save the extracted data into an Excel file using Python on macOS.

## Features

- Authenticate with Microsoft Graph API using OAuth 2.0
- Fetch emails from your Outlook mailbox
- Process emails to extract sender, recipients, subject, date, body, and attachments
- Save email data into an Excel file
- Save attachments to a local directory

## Prerequisites

- Python 3.x installed on macOS
- Microsoft 365 account with access to Outlook
- Azure Active Directory application registered for API access
- Internet connectivity

## Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/outlook_email_extractor.git
   cd outlook_email_extractor