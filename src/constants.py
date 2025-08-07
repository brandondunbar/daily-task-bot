import os
from dotenv import load_dotenv

# Load environment variables from a .env file if it exists
load_dotenv()

# Required: path to your service account JSON file
GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH")

if not GOOGLE_CREDENTIALS_PATH:
    raise RuntimeError("Missing required environment variable: GOOGLE_CREDENTIALS_PATH")

BOT_CONFIG_PATH = os.getenv("BOT_CONFIG_PATH")