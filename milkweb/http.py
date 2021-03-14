import requests
from typing import List
from aiohttp import request
from milkweb import CLIENT_ID, CLIENT_SECRET, AUTHORIZATION_URL, REDIRECT_URI, TOKEN_URL, SCOPES

def get_redirect_url(*, state: str) -> str:
    URL = (
        AUTHORIZATION_URL
        + "?"
        + "response_type=code"
        + f"&client_id={CLIENT_ID}"
        + f"&scope={'%20'.join(SCOPES)}"
        + f"&state={state}"
        + f"&redirect_uri={REDIRECT_URI}"
        + "&prompt=consent"
    )

    return URL

async def get_user_token(*, code: str) -> str:
    scopes = " ".join(SCOPES)
    async with request(
        "POST",
        TOKEN_URL,
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "scope": scopes
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        }
    ) as resp:
        resp.raise_for_status()
        data = await resp.json()
        return data["access_token"]