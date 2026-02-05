import datetime

import pytest

from src.models.vacancy_hh import VacancyHH


def test_vacancy_hh_init(vacancy_1):
    assert vacancy_1.name == "name"
    assert vacancy_1.salary == 95000
    assert vacancy_1.date == "05.02.2026"
    assert vacancy_1.url == "https://hh.ru/vacancy/"
    assert vacancy_1.responsibility == "test"
    assert vacancy_1.experience == "experience"
    assert vacancy_1.area == "area"


def test_vacancy_hh_init_invalid_date():
    with pytest.raises(ValueError, match="Дата должна быть строкой"):
        vacancy_1 = VacancyHH("name", 95000, 15022026, "https://hh.ru/vacancy/", "test", "experience", "area")


def test_vacancy_hh_init_invalid_format_date():
    with pytest.raises(ValueError, match="Дата должна быть в формате ДД.ММ.ГГГГ."):
        vacancy_1 = VacancyHH("name", 95000, "2026.11.15", "https://hh.ru/vacancy/", "test", "experience", "area")


def test_vacancy_hh_init_invalid_format_url():
    with pytest.raises(ValueError, match="Некорректный url вакансии."):
        vacancy_1 = VacancyHH("name", 95000, "05.02.2026", "https://hh.ru/vk.ru", "test", "experience", "area")


def test_vacancy_hh_init_invalid_salary():
    with pytest.raises(ValueError, match="Зарплата должна быть положительным числом"):
        vacancy_1 = VacancyHH("name", -95000, "05.02.2026", "https://hh.ru/vacancy/", "test", "experience", "area")


def test_str_vacancy_hh(vacancy_1):
    assert str(vacancy_1) == "name, 95000, experience, area"


def test_it_vacancy_hh(vacancy_1, vacancy_2):
    assert vacancy_2 < vacancy_1
    assert vacancy_2 < 100000
    assert vacancy_1 < 112345.12


def test_le_vacancy_hh(vacancy_1, vacancy_2):
    assert vacancy_2 <= vacancy_1
    assert vacancy_2 <= 50000
    assert vacancy_1 <= 112345.12


def test_eq_vacancy_hh(vacancy_1, vacancy_2):
    assert vacancy_2 == VacancyHH("name", 50000, "05.02.2026", "https://hh.ru/vacancy/", "test", "experience", "area")
    assert vacancy_2 == 50000.00
    assert vacancy_1 == 95000.00


def test_ne_vacancy_hh(vacancy_1, vacancy_2):
    assert vacancy_2 != vacancy_1
    assert vacancy_2 != 1000000000
    assert vacancy_1 != 21312451.124


def test_gt_vacancy_hh(vacancy_1, vacancy_2):
    assert vacancy_1 > vacancy_2
    assert vacancy_2 > 49.999
    assert vacancy_1 > 50000


def test_ge_vacancy_hh(vacancy_1, vacancy_2):
    assert vacancy_1 >= vacancy_2
    assert vacancy_2 >= 49.999
    assert vacancy_1 >= 95000


@pytest.mark.parametrize("invalid_value", ["test", [], {}, set(), tuple(), None])
def test_type_error_for_all_operators(vacancy_1, invalid_value):
    with pytest.raises(TypeError, match="Сравнение возможно только с числами или объектами BaseVacancy"):
        vacancy_1 < invalid_value

    with pytest.raises(TypeError, match="Сравнение возможно только с числами или объектами BaseVacancy"):
        vacancy_1 <= invalid_value

    with pytest.raises(TypeError, match="Сравнение возможно только с числами или объектами BaseVacancy"):
        vacancy_1 == invalid_value

    with pytest.raises(TypeError, match="Сравнение возможно только с числами или объектами BaseVacancy"):
        vacancy_1 != invalid_value

    with pytest.raises(TypeError, match="Сравнение возможно только с числами или объектами BaseVacancy"):
        vacancy_1 > invalid_value

    with pytest.raises(TypeError, match="Сравнение возможно только с числами или объектами BaseVacancy"):
        vacancy_1 >= invalid_value


def test_from_api_list_vacancy_hh(vacancies_from_hh):
    result = VacancyHH.from_api_list(vacancies_from_hh)
    assert len(result) == 30

    for vacancy in result:
        assert isinstance(vacancy.name, str)
        assert isinstance(vacancy.salary, int)
        assert vacancy.url.startswith("https://hh.ru/vacancy/")
        datetime.datetime.strptime(vacancy.date, "%d.%m.%Y")


def test_from_api_vacancy_hh(vacancies_from_hh):
    vacancy = VacancyHH.from_api_list(vacancies_from_hh)[2]
    assert vacancy.name == "Фронтенд и бэкенд разработчик"
    assert vacancy.salary == 350000
    assert vacancy.date == "03.02.2026"
    assert vacancy.url == "https://hh.ru/vacancy/130143835"
    assert vacancy.responsibility == "Разработка и поддержка фронтенд- и бэкенд-частей современного "
    assert vacancy.experience == "Более 6 лет"
    assert vacancy.area == "Москва"


def test_to_dict_vacancy_hh(vacancies_from_hh):
    vacancy = VacancyHH.from_api_list(vacancies_from_hh)[1]
    assert vacancy.to_dict() == {
        "Название вакансии": "Специалист по ведению базы данных / Менеджер отдела сопровождения",
        "Заработная плата": 100000,
        "Дата публикации": "02.02.2026",
        "Ссылка на вакансию": "https://hh.ru/vacancy/130100802",
        "Обязанности": "Поддержание в актуальном состоянии технической информации.",
        "Опыт работы": "От 1 года до 3 лет",
        "Город": "Санкт-Петербург",
    }
