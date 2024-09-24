from abc import ABC, abstractmethod

from src.models.vacancy import Vacancy


class FileWorker(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy: 'Vacancy') -> None:
        pass

    @abstractmethod
    def get_vacancies(self, criteria: dict) -> list:
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: 'Vacancy') -> None:
        pass
