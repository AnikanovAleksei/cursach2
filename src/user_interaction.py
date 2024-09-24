from src.api.hh_api import HeadHunterAPI
from src.models.vacancy import Vacancy
from src.savers.json_saver import JSONSaver


def user_interaction():
    """
    Функция для взаимодействия с пользователем.
    """
    hh_api = HeadHunterAPI()
    json_saver = JSONSaver('data/vacancies.json')

    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()

    vacancies_json = hh_api.get_vacancies(search_query)
    vacancies_list = Vacancy.cast_to_object_list(vacancies_json)

    filtered_vacancies = [v for v in vacancies_list if any(word in v.description for word in filter_words)]
    sorted_vacancies = sorted(filtered_vacancies, reverse=True)
    top_vacancies = sorted_vacancies[:top_n]

    for vacancy in top_vacancies:
        print(f"Название: {vacancy.title}")
        print(f"Ссылка: {vacancy.url}")
        print(f"Зарплата: {vacancy.salary}")
        print(f"Описание: {vacancy.description}")
        print("-" * 50)

    for vacancy in top_vacancies:
        json_saver.add_vacancy(vacancy)
