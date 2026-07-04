from datetime import datetime, timezone

from . import timestamps


def test_now_iso_and_parse_iso_roundtrip():
    s = timestamps.now_iso()
    dt = timestamps.parse_iso(s)
    assert isinstance(dt, datetime)
    assert dt.tzinfo is not None


def test_parse_variants():
    # parse ISO without fractional seconds
    s = "2020-01-01T00:00:00Z"
    dt = timestamps.parse_iso(s)
    assert dt.year == 2020
    assert dt.tzinfo is not None
