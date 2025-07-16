from googleapiclient.discovery import build

def fetch_unread_emails(creds):
    service = build("gmail", "v1", credentials=creds)
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
    messages = results.get('messages', [])
    summaries = []

    for msg in messages[:5]:
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
        snippet = msg_data.get("snippet")
        summaries.append(snippet)

    return summaries
