from unittest.mock import Mock, patch

import pytest
import requests


@patch("requests.get")
def test_get_vacancies(mock_get, hh_api, hh_vacancies):
    mock_response = Mock()
    mock_response.json.return_value = hh_vacancies
    mock_response.status_code = 200

    mock_empty_response = Mock()
    mock_empty_response.json.return_value = {"items": []}
    mock_empty_response.status_code = 200

    mock_get.side_effect = [mock_response, mock_empty_response]

    result = hh_api.get_vacancies("python", "senior")

    assert len(result) == 30
    assert isinstance(result, list)
    assert mock_get.call_count == 2
    for vacancy in result:
        salary = vacancy["salary"]
        assert salary is None or salary.get("currency") == "RUR"


@patch("requests.get")
def test_get_vacancies_http_error(mock_get, hh_api):
    http_error = requests.exceptions.HTTPError()
    http_error.response = Mock(status_code=404)
    mock_get.side_effect = http_error
    with pytest.raises(ConnectionError, match="HTTP ошибка, код ошибки: 404"):
        hh_api.get_vacancies("python")


@patch("requests.get")
def test_get_vacancies_connection_error(mock_get, hh_api):
    mock_get.side_effect = requests.exceptions.ConnectionError
    with pytest.raises(ConnectionError, match="Ошибка соединения "):
        hh_api.get_vacancies("python")


@patch("requests.get")
def test_get_vacancies_timeout_error(mock_get, hh_api):
    mock_get.side_effect = requests.exceptions.Timeout
    with pytest.raises(TimeoutError, match="Таймаут запроса "):
        hh_api.get_vacancies("python")
