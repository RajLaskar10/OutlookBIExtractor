# utils/graph_api.py

import sys
import requests
import logging
from msal import PublicClientApplication
from config import CLIENT_ID, AUTHORITY_URL, SCOPES, GRAPH_API_ENDPOINT

class GraphAPIClient:
    def __init__(self):
        self.access_token = None
        self.headers = None
        self.app = PublicClientApplication(
            CLIENT_ID,
            authority=AUTHORITY_URL
        )

    def authenticate(self):
        try:
            # Try to get token silently
            accounts = self.app.get_accounts()
            if accounts:
                result = self.app.acquire_token_silent(SCOPES, account=accounts[0])
            else:
                # Interactive login via Device Code Flow
                flow = self.app.initiate_device_flow(scopes=SCOPES)
                if 'user_code' not in flow:
                    print(f"Failed to create device flow. Error: {flow}")
                    return False
                print(flow['message'])
                result = self.app.acquire_token_by_device_flow(flow)

            if 'access_token' in result:
                self.access_token = result['access_token']
                self.headers = {
                    'Authorization': f'Bearer {self.access_token}',
                    'Prefer': 'outlook.body-content-type="text"'
                }
                return True
            else:
                error_message = result.get('error_description', 'Unknown error')
                logging.error(f"Error obtaining access token: {error_message}")
                return False
        except Exception as e:
            logging.error(f"Authentication error: {e}")
            return False

    def get_emails(self):
        try:
            emails = []
            endpoint = f'{GRAPH_API_ENDPOINT}/me/messages'
            params = {
                '$top': '50',  # Adjust as needed
                '$select': 'sender,subject,toRecipients,ccRecipients,receivedDateTime,body,hasAttachments',
                '$orderby': 'receivedDateTime DESC',
            }

            while True:
                response = requests.get(endpoint, headers=self.headers, params=params)
                if response.status_code != 200:
                    logging.error(f"Error fetching emails: {response.text}")
                    break

                data = response.json()
                emails.extend(data.get('value', []))

                # Pagination
                if '@odata.nextLink' in data:
                    endpoint = data['@odata.nextLink']
                    params = None  # Params are included in the nextLink
                else:
                    break

            return emails
        except Exception as e:
            logging.error(f"Error retrieving emails: {e}")
            return None

    def get_attachments(self, message_id):
        try:
            endpoint = f'{GRAPH_API_ENDPOINT}/me/messages/{message_id}/attachments'
            response = requests.get(endpoint, headers=self.headers)
            if response.status_code == 200:
                return response.json().get('value', [])
            else:
                logging.error(f"Error fetching attachments for email {message_id}: {response.text}")
                return []
        except Exception as e:
            logging.error(f"Error retrieving attachments for email {message_id}: {e}")
            return []