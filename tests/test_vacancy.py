from src.models.vacancy import Vacancy


def test_vacancy_initialization():
    vacancy = Vacancy(title="Developer", url="http://example.com", salary=5000, description="Software Developer")

    assert vacancy.title == "Developer"
    assert vacancy.url == "http://example.com"
    assert vacancy.salary == 5000
    assert vacancy.description == "Software Developer"


def test_validate_salary():
    vacancy_with_salary = Vacancy(title="Developer", url="http://example.com", salary=5000, description="Developer")
    vacancy_without_salary = Vacancy(title="Manager", url="http://example.com", salary=0,
                                     description="Manager")

    assert vacancy_with_salary.salary == 5000
    assert vacancy_without_salary.salary == "Зарплата не указана"


def test_vacancy_lt():
    vacancy1 = Vacancy(title="Developer", url="http://example.com", salary=5000, description="Developer")
    vacancy2 = Vacancy(title="Manager", url="http://example.com", salary=7000, description="Manager")
    vacancy3 = Vacancy(title="Analyst", url="http://example.com", salary=0, description="Analyst")

    assert vacancy1 < vacancy2  # 5000 < 7000
    assert not (vacancy2 < vacancy1)  # 7000 > 5000
    assert not (vacancy1 < vacancy3)  # Нельзя сравнивать, если зарплата не указана


def test_cast_to_object_list():
    vacancies_json = [
        {'name': 'Developer', 'alternate_url': 'http://example.com', 'salary': {'from': 6000},
         'snippet': {'requirement': 'Experienced in Python'}},
        {'name': 'Manager', 'alternate_url': 'http://example.com/manager', 'salary': {},
         'snippet': {'requirement': 'Leadership skills'}},
        None,
        {'not_a_valid_key': 'Not a valid value'},
    ]

    vacancies = Vacancy.cast_to_object_list(vacancies_json)

    assert len(vacancies) == 3
    assert vacancies[0].title == "Developer"
    assert vacancies[0].salary == 6000
    assert vacancies[1].title == "Manager"
    assert vacancies[1].salary == "Зарплата не указана"
