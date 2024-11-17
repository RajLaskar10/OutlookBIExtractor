# utils/email_processor.py

import os
import base64
import logging
from tqdm import tqdm
from config import ATTACHMENT_DIR

def process_emails(emails, client):
    email_data = []

    for email in tqdm(emails, desc='Processing emails'):
        try:
            data = {
                'Sender': email.get('sender', {}).get('emailAddress', {}).get('address'),
                'To': '; '.join([recipient['emailAddress']['address'] for recipient in email.get('toRecipients', [])]),
                'CC': '; '.join([recipient['emailAddress']['address'] for recipient in email.get('ccRecipients', [])]),
                'Subject': email.get('subject'),
                'Date': email.get('receivedDateTime'),
                'Body': email.get('body', {}).get('content'),
                'Attachments': []
            }

            # Process attachments
            if email.get('hasAttachments'):
                message_id = email.get('id')
                attachments = client.get_attachments(message_id)
                for attachment in attachments:
                    attachment_name = attachment.get('name')
                    data['Attachments'].append(attachment_name)

                    # Save attachment
                    if attachment.get('@odata.type') == '#microsoft.graph.fileAttachment':
                        content_bytes = attachment.get('contentBytes')
                        attachment_data = base64.b64decode(content_bytes)
                        attachment_path = os.path.join(ATTACHMENT_DIR, attachment_name)

                        # Ensure unique filenames
                        base_name, extension = os.path.splitext(attachment_name)
                        counter = 1
                        while os.path.exists(attachment_path):
                            attachment_name = f"{base_name}_{counter}{extension}"
                            attachment_path = os.path.join(ATTACHMENT_DIR, attachment_name)
                            counter += 1

                        with open(attachment_path, 'wb') as f:
                            f.write(attachment_data)
        except Exception as e:
            logging.error(f"Error processing email ID {email.get('id')}: {e}")

        data['Attachments'] = '; '.join(data['Attachments'])
        email_data.append(data)

    return email_data