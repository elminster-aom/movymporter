import asyncio
import chardet
import datetime
import logging
import re
from typing import Any, Dict, Tuple

# chardet.detect(data.encode())
log = logging.getLogger(__name__)


async def formater(movie: Dict[str, str]) -> None:
    """Receives the original CSV row, converted to a dictionary, and do
    necessary transformations. Looking that new output dictionary fulfills
    requirements of storing DB

    Args:
        movie (Dict[str, str]): CSV row converted to a dictionary, with all
            information about a specific movie

    Raises:
        TypeError: If a movie does not have field `title` it cannot be
        processed farther

    Returns:
        Dict[str, Any]: The input dictionary, after transformations
    """
    if not movie.get("title", None):
        raise TypeError(f"Required field missing; field=title movie={movie!r}")

    await asyncio.gather(
        _year(movie),
        _length(movie),
        _title(movie),
        _subject(movie),
        _actor(movie),
        _actress(movie),
        _director(movie),
        _popularity(movie),
        _awards(movie),
        _image(movie),
    )


def _reencode(string: str) -> str:
    """Look for best string decoding and convert to it, the input `string`

    Args:
        string (str): String to decode

    Returns:
        str: String decoded
    """
    result = None
    if string:
        try:
            binary_string = string.encode()
            encoding = chardet.detect(binary_string)["encoding"]
            result = binary_string.decode(encoding)
        except UnicodeDecodeError as error:
            log.warning(f"{error}; string={string!r}")
    return result


async def _year(movie: Dict[str, str]) -> None:
    """Ensure `movie['year']` is an integer, however if conversion fails None
    is not accepted. We diced to set it to 1888 (the lowest valid year), when
    value cannot be converted to `int` or when it's out of range

    Args:
        movie (Dict[str, str]): Movie to transform
    """
    try:
        result = int(movie["year"])
    except (KeyError, ValueError) as error:
        log.warning(f"{error}; field=year substitution=1888 movie={movie!r}")
        movie["year"] = 1888
    else:
        if 1888 <= result <= datetime.datetime.now().year:
            movie["year"] = result
        else:
            log.warning(
                f"Movie year out of range [1888, {datetime.datetime.now().year}]; field=year substitution=1888 movie={movie!r}"
            )
            movie["year"] = 1888


async def _length(movie: Dict[str, str]) -> None:
    try:
        movie["length"] = float(movie["length"])
    except (KeyError, ValueError) as error:
        log.warning(f"{error}; field=length substitution=None movie={movie!r}")
        movie["length"] = None


async def _title(movie: Dict[str, str]) -> None:
    movie["title"] = _reencode(movie["title"])


async def _subject(movie: Dict[str, str]) -> None:
    movie["subject"] = _reencode(movie["subject"])


async def _actor(movie: Dict[str, str]) -> None:
    movie["actor"] = _reencode(movie["actor"])


async def _actress(movie: Dict[str, str]) -> None:
    movie["actress"] = _reencode(movie["actress"])


async def _director(movie: Dict[str, str]) -> None:
    movie["director"] = _reencode(movie["director"])


async def _popularity(movie: Dict[str, str]) -> None:
    try:
        result = float(movie["popularity"])
    except (KeyError, ValueError) as error:
        log.warning(f"{error}; field=popularity substitution=None movie={movie!r}")
        movie["popularity"] = None
    else:
        if 0 <= result <= 100:
            movie["popularity"] = result
        else:
            log.warning(
                f"Movie popularity out of range [0, 100]; field=popularity substitution=None movie={movie!r}"
            )
            movie["popularity"] = None


async def _awards(movie: Dict[str, str]) -> None:
    try:
        result = movie["awards"].lower()
    except AttributeError as error:
        log.warning(f"{error}; field=awards substitution=No movie={movie!r}")
        movie["awards"] = "No"
    else:
        if result == "yes":
            movie["awards"] = "Yes"
        elif result == "no":
            movie["awards"] = "No"
        else:
            log.warning(
                f"Unknown awards value; field=awards substitution=No movie={movie!r}"
            )
            movie["awards"] = "No"


async def _image(movie: Dict[str, str]) -> None:
    try:
        regex_match = re.match(r".+\.(png|jpg|jpeg)$", movie["image"])
    except (KeyError, TypeError) as error:
        log.warning(f"{error}; field=image substitution=None movie={movie!r}")
        movie["image"] = None
    else:
        if regex_match is None:
            log.warning(
                f"Supported images are: png, jpg, jpeg; field=image substitution=None movie={movie!r}"
            )
            movie["image"] = None
