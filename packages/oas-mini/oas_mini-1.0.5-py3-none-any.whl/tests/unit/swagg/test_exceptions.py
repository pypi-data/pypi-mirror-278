from oas_mini.swagg.exceptions import ValidationException


def test_validation():
    ve_mock = ValidationException("test")
    assert isinstance(ve_mock, ValidationException)
