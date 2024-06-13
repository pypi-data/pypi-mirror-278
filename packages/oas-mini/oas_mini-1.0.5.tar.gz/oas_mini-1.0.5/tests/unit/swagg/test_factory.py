import json
import pytest
import os
from oas_mini.swagg.factory import Factory
from oas_mini.swagg.endpoint import Endpoint


def test_factory():
    with pytest.raises(Exception):
        Factory("test")


def test_usage_msg():
    factory_mock = Factory("test", "a", "b")
    mock_endpoint = Endpoint("get")
    u_msg = factory_mock._create_usage_message(mock_endpoint)
    assert u_msg == ""


def test_get_file():
    file_name = "test_file.txt"
    file_content = {"test":"test"}

    factory_mock = Factory("test", "a", "b")
    factory_mock.flag_args["-f"] = file_name

    with open(file_name, "w+") as f:
        json.dump(file_content, f)

    assert factory_mock.get_file() == file_content
    os.remove(file_name)
