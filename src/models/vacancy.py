class Vacancy:
    slots = ['title', 'url', 'salary', 'description']

    def __init__(self, title: str, url: str, salary: int, description: str):
        """
        Инициализация объекта Vacancy.

        :param title: Название вакансии.
        :param url: Ссылка на вакансию.
        :param salary: Зарплата.
        :param description: Описание вакансии.
        """
        self.title = title
        self.url = url
        self.salary = self.__validate_salary(salary)
        self.description = description

    @staticmethod
    def __validate_salary(salary: int) -> str:
        """
        Валидирует зарплату. Если зарплата не указана, возвращает строку "Зарплата не указана".

        :param salary: Зарплата.
        :return: Строка с зарплатой или "Зарплата не указана".
        """
        if salary:
            return salary
        else:
            return "Зарплата не указана"

    def __lt__(self, other: 'Vacancy') -> bool:
        """
        Сравнивает две вакансии по зарплате.

        :param other: Другая вакансия для сравнения.
        :return: True, если зарплата текущей вакансии меньше, чем у другой вакансии.
        """
        if self.salary == "Зарплата не указана" or other.salary == "Зарплата не указана":
            return False
        return self.salary < other.salary

    @staticmethod
    def cast_to_object_list(vacancies_json: list) -> list:
        """
        Преобразует список JSON-объектов в список объектов класса Vacancy.

        :param vacancies_json: Список JSON-объектов вакансий.
        :return: Список объектов класса Vacancy.
        """
        vacancies_list = []
        for vacancy in vacancies_json:
            if vacancy is None:
                continue
                # Дополнительная проверка на словарь
            if not isinstance(vacancy, dict):
                continue

            title = vacancy.get('name', '')
            url = vacancy.get('alternate_url', '')
            # Убедимся, что salary - это действительный словарь перед вызовом get на нем
            salary = None
            if vacancy.get('salary') and isinstance(vacancy.get('salary'), dict):
                salary = vacancy.get('salary').get('from', None)

            description = vacancy.get('snippet', {}).get('requirement', '')
            if description is None:
                description = ""

            vacancies_list.append(Vacancy(title, url, salary, description))
        return vacancies_list
