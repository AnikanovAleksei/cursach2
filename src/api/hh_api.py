import requests
from src.api.vacancy_api import VacancyAPI


class HeadHunterAPI(VacancyAPI):
    def __init__(self):
        self._HeadHunterAPI__params = None
        self.__url = 'https://api.hh.ru/vacancies'
        self.__headers = {'User-Agent': 'HH-User-Agent'}
        self.__params = {'text': '', 'page': 0, 'per_page': 100}

    def _connect_to_api(self) -> requests.Response:
        response = requests.get(self.__url, headers=self.__headers, params=self.__params)
        if response.status_code == 200:
            return response
        else:
            raise Exception("Failed to connect to API")

    def get_vacancies(self, keyword: str) -> list:
        self.__params['text'] = keyword
        self.__params['page'] = 0
        vacancies = []
        while self.__params['page'] < 20:
            response = self._connect_to_api()
            data = response.json()
            vacancies.extend(data['items'])
            self.__params['page'] += 1
        return vacancies
