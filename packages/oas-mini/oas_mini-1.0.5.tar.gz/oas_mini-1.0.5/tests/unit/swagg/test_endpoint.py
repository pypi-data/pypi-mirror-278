import pytest
from unittest.mock import patch, Mock
from oas_mini.swagg.endpoint import Endpoint
from oas_mini.swagg.exceptions import ValidationException


def test_method():
    with pytest.raises(Exception):
        Endpoint("test")


def test_repr():
    repr = Endpoint.get_representation("object")
    assert repr == "{}"


def test_formatted():
    mock_endpoint = Endpoint("get")
    assert mock_endpoint.get_formatted_parameters() == "()"
    mock_endpoint.parameter_names = ("test", )
    assert mock_endpoint.get_formatted_parameters() == "(test)"
    mock_endpoint.parameter_names = ("test", "test2")
    assert mock_endpoint.get_formatted_parameters() == "(test, test2)"


def test_validate_parm():
    with pytest.raises(ValidationException):
        mock_endpoint = Endpoint("get")
        mock_endpoint.validate_parameters("123", "456")


def test_validate_query():
    with pytest.raises(ValidationException):
        mock_endpoint = Endpoint("get")
        mock_endpoint.validate_query(test="test")


def test_validate_schema():
    with pytest.raises(ValidationException):
        mock_endpoint = Endpoint("get")
        mock_endpoint.schema = {"fail":{"type":"object"}}
        mock_endpoint.validate_schema({"fail":"string"})


def test_call():
    mock_endpoint = Endpoint("get")
    with patch("requests.request") as response:
        response_mock = Mock()
        response.return_value = response_mock
        result = mock_endpoint.call("localhost")
        assert result == response_mock


def test_help():
    mock_endpoint = Endpoint("get")
    assert mock_endpoint.get_key() == "GET /"
    assert mock_endpoint.help_message() == "\n" + mock_endpoint.get_key() + "\n"
