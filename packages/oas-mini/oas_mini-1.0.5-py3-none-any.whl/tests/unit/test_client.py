import pytest
import requests
from oas_mini.oas_mini import run, service_url, validate_service, treat_result


def test_treat_result():
    response_mock = requests.Response()
    response_mock.status_code = 404
    treated = treat_result(response_mock)
    assert treated == response_mock


def test_service_url():
    serv = service_url("oaas-broker-adhoc")
    assert serv == "https://oaas-broker.nuvem.bb.com.br/adhoc/"


def test_validate_service():
    with pytest.raises(Exception):
        validate_service("bad_service")


def test_run():
    result = run(["oaas-analytics", "get", "metadata", "portal", "-v"])
    assert result["message"] == "Validation Succeeded. No errors found."
