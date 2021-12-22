import asyncio
import logging
import re
from typing import Any, Dict, Tuple


log = logging.getLogger(__name__)


async def formater(movie: Dict[str, str]) -> Dict[str, Any]:
    if movie["title"] is None:
        log.warning(f"Required field missing; field=title movie={movie!r}")
        return None

    return dict(
        await asyncio.gather(
            _year(movie["year"]),
            _length(movie["length"]),
            _title(movie["title"]),
            _subject(movie["subject"]),
            _actor(movie["actor"]),
            _actress(movie["actress"]),
            _director(movie["director"]),
            _popularity(movie["popularity"]),
            _awards(movie["awards"]),
            _image(movie["image"]),
        )
    )


async def _year(year: str) -> Tuple[str, int]:
    result = None
    try:
        result = int(year)
    except ValueError as error:

        log.warning(f"{error}; field=length value={year!r}, substitution={result!r}")
    return "year", result


async def _length(length: str) -> Tuple[str, float]:
    result = None
    try:
        result = float(length)
    except ValueError as error:

        log.warning(f"{error}; field=length value={length!r}, substitution={result!r}")
    return "length", result


async def _title(title: str) -> Tuple[str, str]:
    return "title", title


async def _subject(subject: str) -> Tuple[str, str]:
    return "subject", subject


async def _actor(actor: str) -> Tuple[str, str]:
    return "actor", actor


async def _actress(actress: str) -> Tuple[str, str]:
    return "actress", actress


async def _director(director: str) -> Tuple[str, str]:
    return "director", director


async def _popularity(popularity: str) -> Tuple[str, float]:
    result = None
    try:
        result = float(popularity)
    except ValueError as error:
        log.warning(
            f"{error}; field=popularity value={popularity!r}, substitution={result!r}"
        )
    return "popularity", result


async def _awards(awards: str) -> Tuple[str, str]:
    return "awards", awards if awards in ["Yes", "No"] else "No"


async def _image(image: str) -> Tuple[str, str]:
    result = None
    try:
        result = None if re.match(r".+\.(png|jpg|jpeg)$", image) is None else image
    except Exception as error:
        log.warning(
            f"{error}; field=popularity value={image!r}, substitution={result!r}"
        )
    return ("image", result)
