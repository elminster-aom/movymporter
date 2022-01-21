""" From a CSV file containing movie metadata that we want to "import" into a
web service using a supplied endpoint. This endpoint only accepts one object at
a time. 
Since data can be inacurate, this code will run the main transformations needed
for importing as much data (movies) as possible
"""
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
    movie: Dict[str, str],
    session: aiohttp.ClientSession,
    url: str,
    stop: int,
) -> None:
    """Wrapper which defines the application main logic to parallelize
    (`syncio.gather()`).
    In our case, for every row in CSV file, the actions of reading, process and
    store it must be sequential, therefore they are carried out under this
    method.
    On the other hand, all rows can be processed parallely, so every row is
    assigned to a different `_wrapper()`

    Args:
        movie (Dict[str,str]): CSV row converted to a dictionary, with all
            information about a specific movie
        session (aiohttp.ClientSession): HTTP Session to movies backup
            interface
        url (str): URL of our POST call to movies backup interface
        stop (int): Do we stop after fist error (`stop!=0') or continue
            processing the full CSV file
    """
    try:
        await indata.formater(movie)
        await outdata.url_post(
            session,
            url=url,
            data=movie,
        )
    except (TypeError, ValueError) as error:
        log.error(error)
        if stop:
            raise


async def main(config: Dict[str, str]) -> None:
    """Main coroutine block

    Args:
        config (Dict[str, str]): Basic environment settings for our application
    """
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


return_code = 1
env_config = dotenv.dotenv_values()
logging.basicConfig(level=logging.getLevelName(env_config["LOG_LEVEL"]))
asyncio.run(main(env_config))
return_code = 0
sys.exit(return_code)
