import os
from dotenv import load_dotenv
from typing import Final, List

load_dotenv()

REDIRECT_URI: Final[str] = "http://127.0.0.1:5000/callback"
SCOPES: Final[List[str]] = ["identify", "guilds"]
OAUTH2_URL: Final[str] = "https://discord.com/api/oauth2"
AUTHORIZATION_URL: Final[str] = OAUTH2_URL + "/authorize"
TOKEN_URL: Final[str] = OAUTH2_URL + "/token"
CLIENT_ID: Final[int] = int(os.environ["CLIENT_ID"])
CLIENT_SECRET: Final[str] = os.environ["CLIENT_SECRET"]
APP_SECRET: Final[str] = os.environ["APP_SECRET"]