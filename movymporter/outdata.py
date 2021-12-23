import aiohttp
import asyncio
import logging
import asyncio
from typing import Any, Dict


log = logging.getLogger(__name__)


async def url_post(
    session: aiohttp.ClientSession,
    url: str,
    data: Dict[str, Any],
) -> None:

    if data is not None:
        async with session.post(url, json=data) as response:
            if response.status == 201:
                log.info(f"Register created for, title={data['title']!r}")
            else:
                http_resp = await response.read()
                raise ValueError(
                    f"http_status={response.status} http_reason={response.reason} http_resp='{http_resp.decode()}' post_data={data}"
                )
