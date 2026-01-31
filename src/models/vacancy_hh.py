import datetime
from typing import Optional, Union

from src.models.base_vacancy import BaseVacancy
from src.utils.validator import Validator


class VacancyHH(BaseVacancy):
    def __init__(self, name: str, salary: int, date: str, url: str, responsibility: str, experience: str, area: str):
        """
        Инициализирует объект VacancyHH.

        :param name: Название вакансии.
        :param salary: Уровень заработной платы.
        :param date: Дата публикации.
        :param url: Ссылка на hh.ru вакансии.
        :param responsibility: Краткое описание обязанностей.
        :param experience: Требуемый опыт работы.
        :param area: Название города.

        :raise TypeError: Если зарплата не integer
        :raise ValueError: Если зарплата отрицательное число,
        некорректно указан url вакансии или некорректный формат даты.
        """
        Validator.positive_integer_validation(salary, "Зарплата должна быть положительным числом")
        Validator.str_validation(name, "Название вакансии должно быть строкой")
        self.__validate_url(url)
        self.__validate_date(date)

        self.name = name
        self.salary = salary
        self.date = date
        self.url = url
        self.responsibility = responsibility
        self.experience = experience
        self.area = area

    def __str__(self) -> str:
        """Строковое представление вакансии."""
        return f"{self.name}, {self.salary}, {self.experience}, {self.area}"

    def __lt__(self, other: Union[object, int, float]) -> bool:
        """
        Сравнивает вакансии по зарплате.

        :param other: Объект BaseVacancy или число для сравнения.

        :return: True, если зарплата текущей вакансии меньше.

        :raises TypeError: Если other не является экземпляром BaseVacancy или числом.
        """
        if not isinstance(other, (BaseVacancy, int, float)):
            raise TypeError("Сравнение возможно только с числами или объектами BaseVacancy")
        if isinstance(other, BaseVacancy):
            return self.salary < other.salary
        return self.salary < other

    def __le__(self, other: Union[object, int, float]) -> bool:
        """
        Сравнивает вакансии по зарплате.

        :param other: Объект BaseVacancy или число для сравнения.

        :return: True, если зарплата текущей вакансии меньше или равна.

        :raises TypeError: Если other не является экземпляром BaseVacancy.
        """
        if not isinstance(other, (BaseVacancy, int, float)):
            raise TypeError("Сравнение возможно только с числами или объектами BaseVacancy")
        if isinstance(other, BaseVacancy):
            return self.salary <= other.salary
        return self.salary <= other

    def __eq__(self, other: Union[object, int, float]) -> bool:
        """
        Сравнивает вакансии по зарплате.

        :param other: Объект BaseVacancy или число для сравнения.

        :return: True, если зарплаты равны.

        :raises TypeError: Если other не является экземпляром BaseVacancy.
        """
        if not isinstance(other, (BaseVacancy, int, float)):
            raise TypeError("Сравнение возможно только с числами или объектами BaseVacancy")
        if isinstance(other, BaseVacancy):
            return self.salary == other.salary
        return self.salary == other

    def __ne__(self, other: Union[object, int, float]) -> bool:
        """
        Сравнивает вакансии по зарплате.

        :param other: Объект BaseVacancy или число для сравнения.

        :return: True, если зарплаты не равны.

        :raises TypeError: Если other не является экземпляром BaseVacancy.
        """
        if not isinstance(other, (BaseVacancy, int, float)):
            raise TypeError("Сравнение возможно только с числами или объектами BaseVacancy")
        if isinstance(other, BaseVacancy):
            return self.salary != other.salary
        return self.salary != other

    def __gt__(self, other: Union[object, int, float]) -> bool:
        """
        Сравнивает вакансии по зарплате.

        :param other: Объект BaseVacancy или число для сравнения.

        :return: True, если зарплата текущей вакансии больше.

        :raises TypeError: Если other не является экземпляром BaseVacancy.
        """
        if not isinstance(other, (BaseVacancy, int, float)):
            raise TypeError("Сравнение возможно только с числами или объектами BaseVacancy")
        if isinstance(other, BaseVacancy):
            return self.salary > other.salary
        return self.salary > other

    def __ge__(self, other: Union[object, int, float]) -> bool:
        """
        Сравнивает вакансии по зарплате.

        :param other: Объект BaseVacancy или число для сравнения.

        :return: True, если зарплата текущей вакансии больше или равна.

        :raises TypeError: Если other не является экземпляром BaseVacancy.
        """
        if not isinstance(other, (BaseVacancy, int, float)):
            raise TypeError("Сравнение возможно только с числами или объектами BaseVacancy")
        if isinstance(other, BaseVacancy):
            return self.salary >= other.salary
        return self.salary >= other

    @classmethod
    def from_api_list(cls, vacancies_list: list[dict]) -> list["BaseVacancy"]:
        """
        Создаёт список объектов VacancyHH из списка словарей с данными вакансий.

        :param vacancies_list: Список словарей. Каждый словарь должен содержать ключи API HeadHunter:
        ключи: name, salary, published_at, alternate_url,
        snippet -> responsibility, experience -> name, area -> name.

        :return: Список объектов VacancyHH.
        """
        return [cls.from_api(vacancy) for vacancy in vacancies_list]

    @classmethod
    def from_api(cls, vacancies_dict: dict) -> "VacancyHH":
        """
        Создаёт экземпляр VacancyHH из словаря с данными вакансии.
        Для отсутствующих ключей используются пустые строки.

        :param vacancies_dict: Словарь, содержащий ключи API HeadHunter:
        name, salary, published_at, alternate_url,
        snippet -> responsibility, experience -> name, area -> name.

        :return: Объект VacancyHH.
        """
        return cls(
            vacancies_dict.get("name", ""),
            cls.__set_salary(vacancies_dict.get("salary")),
            datetime.datetime.fromisoformat(vacancies_dict.get("published_at", "")).strftime("%d.%m.%Y"),
            vacancies_dict.get("alternate_url", ""),
            vacancies_dict.get("snippet", {}).get("responsibility", ""),
            vacancies_dict.get("experience", {}).get("name", ""),
            vacancies_dict.get("area", {}).get("name", ""),
        )

    def to_dict(self) -> dict[str, str | int]:
        """
        Преобразует объект вакансии в словарь.

        :return: Словарь с ключами:
        "Название вакансии": (str),
        "Заработная плата": (int),
        "Дата публикации": (str),
        "Ссылка на вакансию": (str),
        "Обязанности": (str),
        "Опыт работы": (str),
        "Город": (str).
        """
        return {
            "Название вакансии": self.name,
            "Заработная плата": self.salary,
            "Дата публикации": self.date,
            "Ссылка на вакансию": self.url,
            "Обязанности": self.responsibility,
            "Опыт работы": self.experience,
            "Город": self.area,
        }

    @staticmethod
    def __set_salary(salary: Optional[dict]) -> int:
        """
        Метод для установки уровня заработной платы.

        :param salary: Словарь с ключами "from", "to" или None.

        :return: 0 если salary None или оба from/to None.
        Среднее округлённое значение, если указаны from и to.
        Иначе значение from или to, если указано одно из них.
        """
        if salary is None:
            return 0

        from_ = salary.get("from")
        to = salary.get("to")

        if from_ is not None and to is not None:
            return round((int(from_) + int(to)) / 2)
        elif from_ is not None:
            return int(from_)
        elif to is not None:
            return int(to)
        else:
            return 0

    @staticmethod
    def __validate_url(url_string: str) -> None:
        """
        Проверяет, что URL вакансии соответствует формату hh.ru.

        :param url_string: Строка с URL для проверки.

        :raises ValueError: Если URL не начинается с 'https://hh.ru/vacancy/'.
        """
        if not url_string.startswith("https://hh.ru/vacancy/"):
            raise ValueError("Некорректный url вакансии.")

    @staticmethod
    def __validate_date(date_string: str) -> None:
        """
        Проверяет, что дата соответствует формату `ДД.ММ.ГГГГ`.

        :param date_string: Строка с датой для проверки.

        :raises ValueError: Если date_string не является строкой или не соответствует формату `ДД.ММ.ГГГГ`.
        """
        Validator.str_validation(date_string, "Дата должна быть строкой")
        try:
            datetime.datetime.strptime(date_string, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Дата должна быть в формате ДД.ММ.ГГГГ.")
