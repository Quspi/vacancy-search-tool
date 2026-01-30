from typing import Any, Optional

import requests

from src.api.base_api import BaseAPI
from src.utils.validator import Validator


class HeadHunterAPI(BaseAPI):
    """
    Класс для взаимодействия с API HeadHunter (hh.ru).
    Наследуется от абстрактного класса BaseAPI.
    """

    __API_URL: str = "https://api.hh.ru/vacancies"
    __HEADERS: dict = {"HH-User-Agent": "Python learn app/1.0 (olegtamanov@gmail.com)"}

    __params: dict

    def __init__(self) -> None:
        """
        Инициализирует экземпляр класса HeadHunterAPI.
        Устанавливает базовые параметры запроса.
        """
        self.__params = {
            "per_page": 100,
            "area": "113",
            "currency": "RUR",
            "period": 7,
        }

    def get_vacancies(
        self, search_text: str, salary: int, excluded_text: Optional[str] = None
    ) -> list[dict[str, Any]]:
        """
        Получает список вакансий по заданным параметрам поиска.

        :param search_text: Текст для поиска в вакансиях.
        :param salary: Минимальная зарплата для поиска в вакансиях.
        :param excluded_text: Текст для исключения из поиска в вакансиях.

        :return: Список словарей с данными о вакансиях.

        :raises ValueError: Если параметры не проходят валидацию.
        :raises TypeError: Если тип параметра не соответствует ожидаемому.
        :raises ConnectionError: При ошибках HTTP или соединения.
        :raises TimeoutError: При превышении времени ожидания.
        """
        self.__set_search_params(search_text, salary, excluded_text)

        vacancies = []
        page = 0

        while page < 20:
            self.__params["page"] = page
            vacancies_json = self._make_request().json().get("items", [])

            if not vacancies_json:
                break

            vacancies.extend(vacancies_json)
            page += 1

        return vacancies

    def _make_request(self) -> requests.Response:
        """
        Выполняет HTTP GET-запрос к API HeadHunter.

        :return: Объект Response библиотеки requests.

        :raises ConnectionError: При ошибках HTTP или соединения.
        :raises TimeoutError: При превышении времени ожидания.
        """
        try:
            response = requests.get(url=self.__API_URL, headers=self.__HEADERS, params=self.__params)
            response.raise_for_status()

        except requests.exceptions.HTTPError as error:
            status_code = error.response.status_code
            raise ConnectionError(f"HTTP ошибка, код ошибки: {status_code}") from error

        except requests.exceptions.ConnectionError as error:
            raise ConnectionError(f"Ошибка соединения {error}") from error

        except requests.exceptions.Timeout as error:
            raise TimeoutError(f"Таймаут запроса {error}") from error

        return response

    def __set_search_params(self, search_text: str, salary: int, excluded_text: Optional[str] = None) -> None:
        """
        Устанавливает параметры поиска вакансий с валидацией.

        :param search_text: Текст для поиска в вакансиях.
        :param salary: Минимальная зарплата для поиска в вакансиях.
        :param excluded_text: Текст для исключения из поиска в вакансиях.

        :raises ValueError: Если параметры не проходят валидацию.
        :raises TypeError: Если тип параметра не соответствует ожидаемому.
        """
        Validator.str_validation(search_text, "Параметр 'search_text' должен быть строкой")
        Validator.integer_validation(salary, "Параметр 'salary' должен быть числом")
        Validator.positive_integer_validation(salary, "Параметр 'salary' должен быть положительным числом")

        self.__params["text"] = search_text
        self.__params["salary"] = salary

        if excluded_text is not None:
            Validator.str_validation(excluded_text, "Параметр 'excluded_text' должен быть строкой")
            self.__params["excluded_text"] = excluded_text
