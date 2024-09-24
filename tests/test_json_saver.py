import tempfile
import os
import pytest
import json
from abc import ABC, abstractmethod


# Ваши классы и импорт здесь
# from src.models.vacancy import Vacancy
# from src.models.file_worker import FileWorker
# from src.api.json_saver import JSONSaver

class VacancyAPI(ABC):
    @abstractmethod
    def get_vacancies(self, keyword: str) -> list:
        pass


# Mock Vacancy class, in case it's not implemented
class Vacancy:
    def __init__(self, url, title, description):
        self.url = url
        self.title = title
        self.description = description


# Предположим, что JSONSaver в src/api/json_saver.py
class JSONSaver:
    def __init__(self, file_path):
        self.__file_path = file_path
        # Initialize file
        with open(self.__file_path, 'w', encoding='utf-8') as file:
            json.dump([], file)

    def add_vacancy(self, vacancy):
        vacancies = self.get_vacancies()
        vacancies.append(vars(vacancy))
        self.save_vacancies(vacancies)

    def get_vacancies(self):
        with open(self.__file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def save_vacancies(self, vacancies):
        with open(self.__file_path, 'w', encoding='utf-8') as file:
            json.dump(vacancies, file)

    def delete_vacancy(self, vacancy):
        vacancies = self.get_vacancies()
        vacancies = [v for v in vacancies if v['url'] != vacancy.url]
        self.save_vacancies(vacancies)


@pytest.fixture
def temp_json_file():
    with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as temp_file:
        yield temp_file.name
    os.remove(temp_file.name)


@pytest.fixture
def json_saver(temp_json_file):
    return JSONSaver(file_path=temp_json_file)


def test_add_vacancy(json_saver):
    vacancy = Vacancy(url="http://example.com", title="Python Developer", description="Developing with Python.")
    json_saver.add_vacancy(vacancy)

    with open(json_saver._JSONSaver__file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        assert len(data) == 1
        assert data[0]['url'] == "http://example.com"


def test_get_vacancies_empty(json_saver):
    assert json_saver.get_vacancies() == []


def test_save_and_get_vacancies(json_saver):
    vacancies = [{'url': 'http://example.com', 'title': 'Python Developer', 'description': 'Developing with Python.'}]
    json_saver.save_vacancies(vacancies)

    assert json_saver.get_vacancies() == vacancies


def test_delete_vacancy(json_saver):
    vacancy_1 = Vacancy(url="http://example.com/1", title="Developer 1", description="Description 1")
    vacancy_2 = Vacancy(url="http://example.com/2", title="Developer 2", description="Description 2")

    json_saver.add_vacancy(vacancy_1)
    json_saver.add_vacancy(vacancy_2)

    json_saver.delete_vacancy(vacancy_1)

    vacancies = json_saver.get_vacancies()
    assert len(vacancies) == 1
    assert vacancies[0]['url'] == "http://example.com/2"
