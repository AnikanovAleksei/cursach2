import pytest
import requests
from src.api.hh_api import HeadHunterAPI


class MockResponse:
    @staticmethod
    def json():
        return {
            "items": [
                {"id": "1", "name": "Vacancy 1"},
                {"id": "2", "name": "Vacancy 2"}
            ]
        }

    status_code = 200


@pytest.fixture
def hh_api():
    return HeadHunterAPI()


def test_connect_to_api_success(monkeypatch, hh_api):
    def mock_get(*_args, **_kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)
    response = hh_api._connect_to_api()
    assert response.status_code == 200


def test_connect_to_api_failure(monkeypatch, hh_api):
    def mock_get(*_args, **_kwargs):
        response = MockResponse()
        response.status_code = 404
        return response

    monkeypatch.setattr(requests, "get", mock_get)
    with pytest.raises(Exception, match="Failed to connect to API"):
        hh_api._connect_to_api()


def test_get_vacancies(monkeypatch, hh_api):
    def mock_get(*_args, **_kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)
    vacancies = hh_api.get_vacancies("Python")
    assert len(vacancies) == 40
    assert vacancies[0]['id'] == "1"
    assert vacancies[1]['name'] == "Vacancy 2"


def test_get_vacancies_pagination(monkeypatch, hh_api):
    call_count = 0

    def mock_get(*_args, **_kwargs):
        nonlocal call_count
        call_count += 1
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)
    hh_api.get_vacancies("Python")
    assert call_count == 20
