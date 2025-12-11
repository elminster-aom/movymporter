import pytest
import datetime

from .indata import _reencode, _year


@pytest.mark.parametrize(
    "input_str,expected",
    [
        ("hello", "hello"), # standard characters
        ("café", "café"), # extended
        ("食べろ", "食べろ"), # more unusual encoding
        ("", None), # empty string
    ]
)
def test_reencode(input_str, expected):
    # _reencode expects str, so skip None input manually
    if expected is None:
        assert _reencode(input_str) is None
    else:
        result = _reencode(input_str)
        assert result == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "movie,expected_year",
    [
        ({"year": "1999"}, 1999), # normal low
        ({"year": str(datetime.datetime.now().year)}, datetime.datetime.now().year), # now
        ({"year": "1000"}, 1888),  # too low
        ({"year": str(datetime.datetime.now().year + 1)}, 1888),  # too high
        ({"year": "notanint"}, 1888),  # invalid int
        ({}, 1888),  # missing key
    ]
)
async def test_year_function(movie, expected_year, caplog):
    await _year(movie)
    assert movie["year"] == expected_year
    # Ensure logs when substituting
    if expected_year == 1888:
        assert "substitution=1888" in caplog.text

