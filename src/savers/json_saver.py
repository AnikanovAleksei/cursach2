import json
import os
from src.models.vacancy import Vacancy
from src.models.file_worker import FileWorker


class JSONSaver(FileWorker):
    def __init__(self, file_path: str = 'data/vacancies.json'):
        """
        Инициализация объекта JSONSaver.

        :param file_path: Путь к файлу для сохранения вакансий.
        """
        self.__file_path = file_path

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """
        Добавляет вакансию в файл.

        :param vacancy: Объект вакансии для добавления.
        """
        vacancies = self.get_vacancies()
        vacancies.append(vacancy.__dict__)
        self.save_vacancies(vacancies)

    def get_vacancies(self) -> list:
        """
        Получает вакансии из файла.

        :return: Список вакансий.
        """
        if not os.path.exists(self.__file_path):
            return []
        with open(self.__file_path, 'r', encoding='utf-8') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []

    def save_vacancies(self, vacancies: list) -> None:
        """
        Сохраняет вакансии в файл.

        :param vacancies: Список вакансий для сохранения.
        """
        with open(self.__file_path, 'w', encoding='utf-8') as file:
            json.dump(vacancies, file, ensure_ascii=False, indent=4)

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """
        Удаляет вакансию из файла.

        :param vacancy: Объект вакансии для удаления.
        """
        vacancies = self.get_vacancies()
        vacancies = [v for v in vacancies if v['url'] != vacancy.url]
        self.save_vacancies(vacancies)
