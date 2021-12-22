import aiofiles
import asyncio
import aiocsv
import aiohttp
import dotenv
import logging
import sys
import indata
import outdata
from typing import Dict


log = logging.getLogger(__name__)


async def _wrapper(
    movie: str,
    session: aiohttp.ClientSession,
    url: str,
    stop: int,
) -> None:
    formated_movie = await indata.formater(movie)
    try:
        await outdata.url_post(
            session,
            url=url,
            data=formated_movie,
        )
    except ValueError as error:
        log.error(error)
        if stop:
            raise


async def main(config: Dict[str, str]) -> None:
    async with aiohttp.ClientSession() as http_session:
        async with aiofiles.open(config["CSV_IN"]) as csv_in:
            tasks = [
                _wrapper(
                    movie=movie,
                    session=http_session,
                    url=config["URL_OUT"],
                    stop=int(config["STOP_ON_ERRORS"]),
                )
                async for movie in aiocsv.AsyncDictReader(csv_in, delimiter=";")
            ]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    return_code = 1
    env_config = dotenv.dotenv_values()
    logging.basicConfig(level=logging.getLevelName(env_config["LOG_LEVEL"]))
    asyncio.run(main(env_config))
    return_code = 0

    sys.exit(return_code)
