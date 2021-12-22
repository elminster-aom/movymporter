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


async def main(config: Dict[str, str]) -> None:
    movies_cnt = 0
    rows_cnt = 0
    async with aiohttp.ClientSession() as http_session:
        async with aiofiles.open(config["CSV_IN"]) as csv_in:

            async for row in aiocsv.AsyncDictReader(csv_in, delimiter=";"):
                rows_cnt += 1
                formated_row = await indata.formater(row)
                try:
                    await outdata.url_post(
                        http_session,
                        url=config["URL_OUT"],
                        data=formated_row,
                    )
                except ValueError as error:
                    log.error(error)
                    if int(config["STOP_ON_ERRORS"]):
                        raise
                else:
                    movies_cnt += 1
    log.info(
        f"Summary; processed_rows={rows_cnt}, successful_imported_rows={movies_cnt}"
    )


if __name__ == "__main__":
    return_code = 1
    env_config = dotenv.dotenv_values()
    logging.basicConfig(level=logging.getLevelName(env_config["LOG_LEVEL"]))
    asyncio.run(main(env_config))
    return_code = 0

    sys.exit(return_code)
