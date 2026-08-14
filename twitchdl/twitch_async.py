"""
Twitch API access, but async.
"""

import time
from typing import Any, Mapping, Optional

import httpx

from twitchdl import CLIENT_ID
from twitchdl.entities import ClipDetails, Data
from twitchdl.exceptions import ConsoleError
from twitchdl.twitch import Content, gql_raise_on_error, log_request, log_response


async def authenticated_post(
    client: httpx.AsyncClient,
    url: str,
    *,
    json: Any = None,
    content: Optional[Content] = None,
    auth_token: Optional[str] = None,
):
    headers = {"Client-ID": CLIENT_ID}
    if auth_token is not None:
        headers["authorization"] = f"OAuth {auth_token}"

    response = await request(client, "POST", url, content=content, json=json, headers=headers)
    if response.status_code == 400:
        data = response.json()
        raise ConsoleError(data["message"])

    response.raise_for_status()

    return response


async def request(
    client: httpx.AsyncClient,
    method: str,
    url: str,
    json: Any = None,
    content: Optional[Content] = None,
    headers: Optional[Mapping[str, str]] = None,
):
    request = client.build_request(method, url, json=json, content=content, headers=headers)
    log_request(request)
    start = time.time()
    response = await client.send(request)
    duration = time.time() - start
    log_response(response, duration)
    return response


async def gql_persisted_query(client: httpx.AsyncClient, query: Data):
    url = "https://gql.twitch.tv/gql"
    response = await authenticated_post(client, url, json=query)
    gql_raise_on_error(response)
    return response.json()


async def get_clip_details(client: httpx.AsyncClient, slug: str) -> ClipDetails:
    query = {
        "operationName": "ShareClipRenderStatus",
        "variables": {"slug": slug},
        "extensions": {
            "persistedQuery": {
                "version": 1,
                "sha256Hash": "0a02bb974443b576f5579aab0fef1d4b7f44e58a8a256f0c5adfead0db70640f",
            }
        },
    }

    response = await gql_persisted_query(client, query)
    return response["data"]["clip"]
