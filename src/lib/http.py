import os
import re

import httpx
from dotenv import load_dotenv

from .redis import redis

load_dotenv()


class StravaAuthError(Exception):
    """An error occurred during the authentication process."""

    pass


def create_http_client(**kwargs) -> httpx.Client:
    """
    Creates a new HTTP client for interacting with the Strava API.

    Args:
        **kwargs: Additional keyword arguments to pass to the httpx.Client constructor.

    Returns:
        httpx.Client: A new HTTP client for interacting with the Strava API.
    """

    return httpx.Client(
        base_url="https://www.strava.com/",
        headers={
            "origin": "https://www.strava.com",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        },
        **kwargs,
    )


def create_authenticated_client() -> httpx.Client:
    """
    Creates a new authenticated HTTP client for interacting with the Strava API.

    Returns:
        httpx.Client: An authenticated HTTP client for interacting with the Strava API.
    """

    is_cached_token = redis.get("strava_token")
    if is_cached_token:
        return httpx.Client(
            base_url="https://www.strava.com/",
            headers={
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
                "Authorization": f"Bearer {is_cached_token}",
            },
        )

    strava_client = create_http_client()

    auth_response = strava_client.post(
        url="/oauth/accept_application",
        params={
            "client_id": "137770",
            "response_type": "code",
            "scope": "activity:read_all",
            "redirect_uri": "http://localhost/exchange_token",
        },
        data="read=&activity%3Aread_all=on&authenticity_token=D8x6XjIh-hvMxA8yjznYd9MwTKhQPUI5R0BYxOSES1S_dODIzBMHlHTpjWVHnPjfMqIvCn3rzB8M-l4_yCUT6A&code_challenge=&code_challenge_method=",
        headers={
            "Cookie": "_strava4_session=gbllphql80760vcjr2r8hghdurfbsrao",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": f"https://www.strava.com/oauth/authorize?client_id={os.getenv("STRAVA_CLIENT_ID")}&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=activity:read_all",
        },
    )

    if auth_response.status_code != 302:
        raise StravaAuthError(
            f"Authorization request failed with status {auth_response.status_code}"
        )

    auth_code_pattern = r"code=([^&]+)"
    auth_code_match = re.search(auth_code_pattern, auth_response.text)

    if auth_code_match is None:
        raise StravaAuthError("Authorization code not found in response")

    authorization_code = auth_code_match.group(1)

    token_response = strava_client.post(
        url="/oauth/token",
        params={
            "client_id": "137770",
            "client_secret":"7b2bd8352031657fff4fcb67a14de8b51d149332",
            "code": authorization_code,
            "grant_type": "authorization_code",
        },
    )

    if token_response.status_code != 200:
        raise StravaAuthError(
            f"Token request failed with status {token_response.status_code}"
        )

    try:
        access_token = token_response.json()["access_token"]

        redis.set("strava_token", access_token, ex=17222)

        return httpx.Client(
            base_url="https://www.strava.com/",
            headers={
                "origin": "https://www.strava.com",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
                "Authorization": f"Bearer {access_token}",
            },
        )
    except (KeyError, ValueError):
        raise StravaAuthError("Invalid token response format")
