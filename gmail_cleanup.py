import os.path
import base64
import json
import time
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

# Mapping of Gmail internal labels to human-readable categories
CATEGORY_MAP = {
    'CATEGORY_PROMOTIONS': 'Promotions',
    'CATEGORY_SOCIAL': 'Social',
    'CATEGORY_UPDATES': 'Updates',
    'CATEGORY_FORUMS': 'Forums',
    'CATEGORY_PERSONAL': 'Personal'
}

# ABSOLUTE SAFETY RULES (To avoid deleting important emails)
PROTECTED_LABELS = ['Keep', 'Tax', 'Receipts', 'Legal', 'School', 'Work', 'Banking']
SEARCH_QUERY = 'is:unread older_than:1y -is:starred -is:important -in:drafts -in:spam -in:trash'

for label in PROTECTED_LABELS:
    SEARCH_QUERY += f' -label:{label}'

def authenticate():
    """Handle OAuth2 authentication and token management."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                print("Error: credentials.json not found. Please provide OAuth 2.0 credentials from Google Cloud Console.")
                return None
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def get_emails(service, query):
    """Retrieve a list of message IDs that match the search query."""
    results = service.users().messages().list(userId='me', q=query, maxResults=500).execute()
    messages = results.get('messages', [])
    return messages


def format_size(size_bytes):
    """Format bytes into a human-readable string."""
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB")
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"

def get_full_analysis_batch(service, messages):
    """Fetch sizes and labels for all candidates efficiently."""
    analysis = {'total_size': 0, 'samples': []}
    
    def callback(request_id, response, exception):
        if exception is None:
            size = response.get('sizeEstimate', 0)
            analysis['total_size'] += size
            
            # Still keep track of samples for the top 20
            headers = response.get('payload', {}).get('headers', [])
            labels = response.get('labelIds', [])
            
            # Identify the category
            category = "General"
            for label_id in labels:
                if label_id in CATEGORY_MAP:
                    category = CATEGORY_MAP[label_id]
                    break

            msg_details = {
                'id': request_id, 
                'size': size,
                'category': category
            }
            for header in headers:
                if header['name'] == 'From': msg_details['from'] = header['value']
                elif header['name'] == 'Subject': msg_details['subject'] = header['value']
                elif header['name'] == 'Date': msg_details['date'] = header['value']
                elif header['name'] == 'List-Unsubscribe': msg_details['unsubscribe'] = header['value']
            analysis['samples'].append(msg_details)

    # Batch process in chunks to be safe
    for i in range(0, len(messages), 100):
        batch = service.new_batch_http_request(callback=callback)
        for msg in messages[i:i+100]:
            batch.add(service.users().messages().get(
                userId='me', id=msg['id'], format='metadata', 
                metadataHeaders=['From', 'Subject', 'Date', 'List-Unsubscribe']
            ))
        batch.execute()
    
    return analysis

def main():
    """Main execution flow: Search -> Analyze -> Confirmation -> Trash."""
    creds = authenticate()
    if not creds:
        return

    try:
        service = build('gmail', 'v1', credentials=creds)
        
        print(f"Searching for emails with query: {SEARCH_QUERY}")
        messages = get_emails(service, SEARCH_QUERY)
        
        if not messages:
            print("No matching emails found.")
            return

        print(f"Found {len(messages)} candidates.")
        print("\nAnalyzing candidates and fetching sample details...")
        
        # New optimized analysis fetch (includes storage)
        analysis = get_full_analysis_batch(service, messages)
        total_size_str = format_size(analysis['total_size'])
        
        print(f"\nPotential Space Reclaimed: {total_size_str}")
        
        print("\nTop 20 Samples:")
        # Sort samples by date to keep display consistent
        sorted_samples = sorted(analysis['samples'], key=lambda x: x.get('date', ''), reverse=True)
        for details in sorted_samples[:20]:
            sender = details.get('from', 'Unknown')
            subject = details.get('subject', 'No Subject')
            print(f"- {details.get('date')}: {sender} | Subject: {subject}")
            
            # Show unsubscribe link if available
            unsub = details.get('unsubscribe')
            if unsub:
                # Often contains <mailto:...> or <http://...>, let's clean it up slightly
                import re
                links = re.findall(r'<(https?://[^>]+)>', unsub)
                if links:
                    print(f"  [Unsubscribe: {links[0]}]")
        
        print("\nAnalyzing sender and category distribution...")
        senders = {}
        categories = {}
        for details in analysis['samples']:
            sender = details.get('from', 'Unknown')
            senders[sender] = senders.get(sender, 0) + 1
            
            cat = details.get('category', 'General')
            categories[cat] = categories.get(cat, 0) + 1
        
        print("\nCategory Breakdown (from candidates):")
        sorted_cats = sorted(categories.items(), key=lambda x: x[1], reverse=True)
        for cat, count in sorted_cats:
            percentage = (count / len(analysis['samples'])) * 100
            print(f"- {cat}: {count} emails ({percentage:.1f}%)")

        print("\nTop Senders (from samples):")
        sorted_senders = sorted(senders.items(), key=lambda x: x[1], reverse=True)
        for sender, count in sorted_senders[:10]:
            print(f"- {sender}: {count} emails")

        confirm = input("\nType PROCEED to move these emails to Trash, or anything else to cancel: ")
        
        if confirm.strip().upper() == 'PROCEED':
            total_messages = len(messages)
            print(f"\nMoving emails to Trash... (0/{total_messages})")
            
            for i, msg in enumerate(messages, 1):
                try:
                    service.users().messages().trash(userId='me', id=msg['id']).execute()
                    print(f"Progress: {i}/{total_messages} emails processed", end='\r')
                except HttpError as e:
                    print(f"\nError trashing email {msg['id']}: {e}")
            
            print()  # New line after progress indicator
            print(f"Successfully moved {total_messages} emails to Trash.")
        else:
            print("Action cancelled.")


    except HttpError as error:
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    main()
