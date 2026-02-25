import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Application configuration.
    All values are loaded from the .env file.
    """


    DEBUG           = os.getenv("DEBUG", "false").lower() == "true"
    HOST            = os.getenv("HOST", "0.0.0.0")
    PORT            = int(os.getenv("PORT", 8000))

    APP_TITLE       = "Document Summarizer API"
    APP_DESCRIPTION = "Connects to Google Drive, parses documents, and summarizes using OpenAI GPT."
    APP_VERSION     = "1.0.0"


    OPENAI_API_KEY      = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL        = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    OPENAI_MAX_TOKENS   = int(os.getenv("OPENAI_MAX_TOKENS", 128000))
    OPENAI_TEMPERATURE  = float(os.getenv("OPENAI_TEMPERATURE", 0.4))


    GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials/credentials.json")
    GOOGLE_TOKEN_PATH        = os.getenv("GOOGLE_TOKEN_PATH", "credentials/token.json")
    DRIVE_FOLDER_ID          = os.getenv("DRIVE_FOLDER_ID", "")


    DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "downloads")


    @classmethod
    def validate(cls):
        errors = []

        if not cls.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY is missing in .env")

        if not os.path.exists(cls.GOOGLE_CREDENTIALS_PATH):
            errors.append(
                f"Google credentials not found at: {cls.GOOGLE_CREDENTIALS_PATH}. "
                "Download from Google Cloud Console."
            )

        if errors:
            raise EnvironmentError(
                "Missing required configuration:\n" + "\n".join(f"  - {e}" for e in errors)
            )