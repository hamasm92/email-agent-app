import os
import urllib.parse
from google.oauth2.credentials import Credentials
import requests

# This version only builds the URL and accepts the code later
def generate_auth_url():
    client_id = os.environ["GOOGLE_CLIENT_ID"]
    redirect_uri = "urn:ietf:wg:oauth:2.0:oob"
    scopes = [
        "https://www.googleapis.com/auth/calendar.readonly",
        "https://www.googleapis.com/auth/gmail.readonly"
    ]
    scope_str = " ".join(scopes)
    encoded_scope = urllib.parse.quote(scope_str)

    auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        f"&response_type=code"
        f"&scope={encoded_scope}"
        f"&access_type=offline"
        f"&prompt=consent"
    )
    return auth_url

def exchange_code_for_credentials(code):
    client_id = os.environ["GOOGLE_CLIENT_ID"]
    client_secret = os.environ["GOOGLE_CLIENT_SECRET"]
    redirect_uri = "urn:ietf:wg:oauth:2.0:oob"
    token_url = "https://oauth2.googleapis.com/token"
    scopes = [
        "https://www.googleapis.com/auth/calendar.readonly",
        "https://www.googleapis.com/auth/gmail.readonly"
    ]

    data = {
        "code": code.strip(),
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code"
    }

    response = requests.post(token_url, data=data)
    if response.status_code != 200:
        raise Exception(f"❌ Token exchange failed: {response.text}")

    token_data = response.json()

    return Credentials(
        token=token_data["access_token"],
        refresh_token=token_data.get("refresh_token"),
        token_uri=token_url,
        client_id=client_id,
        client_secret=client_secret,
        scopes=scopes
    )
