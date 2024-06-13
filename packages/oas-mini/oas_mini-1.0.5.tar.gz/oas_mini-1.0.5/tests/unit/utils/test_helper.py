
from oas_mini.utils.helper import format_seconds_to_hms


def test_zero():
    assert format_seconds_to_hms(0) == "00:00:00"
