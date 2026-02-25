import os
import logging
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import app.config as config

logger = logging.getLogger(__name__)

# Read-only access to Google Drive files
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

GOOGLE_CREDENTIALS_PATH = config.Config.GOOGLE_CREDENTIALS_PATH
GOOGLE_TOKEN_PATH = config.Config.GOOGLE_TOKEN_PATH

def get_credentials(
    credentials_path: str =GOOGLE_CREDENTIALS_PATH,
    token_path: str = GOOGLE_TOKEN_PATH
) -> Credentials:
    """
    Authenticate with Google using OAuth2.
    - First run: Opens browser for user login and saves token.
    - Next runs: Loads saved token and auto-refreshes if expired.

    Args:
        credentials_path (str): Path to OAuth2 credentials JSON from Google Cloud Console.
        token_path (str): Path to save/load the access token.

    Returns:
        Credentials: Valid Google OAuth2 credentials object.
    """
    creds = None

    # Load existing token if available
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        logger.info("Loaded existing token from file.")

    # If no valid credentials, refresh or re-authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            logger.info("Token refreshed successfully.")
        else:
            if not os.path.exists(credentials_path):
                raise FileNotFoundError(
                    f"credentials.json not found at: {credentials_path}\n"
                    "Download it from Google Cloud Console > APIs & Services > Credentials."
                )
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
            logger.info("New OAuth2 login completed.")

        # Save token for future use
        os.makedirs(os.path.dirname(token_path), exist_ok=True)
        with open(token_path, "w") as token_file:
            token_file.write(creds.to_json())
        logger.info(f"Token saved to: {token_path}")

    return creds