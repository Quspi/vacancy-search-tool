from abc import ABC, abstractmethod
from typing import Any

import requests


class BaseAPI(ABC):
    """
    Абстрактный базовый класс для взаимодействия с API.
    Определяет обязательные методы для подключения к API.
    """

    @abstractmethod
    def _make_request(self) -> requests.Response:
        """
        Абстрактный метод для выполнения подключения к API.
        Должен быть реализован в дочерних классах.

        :raises NotImplementedError: Если метод не переопределен.
        """
        ...

    @abstractmethod
    def get_vacancies(self, *args: Any, **kwargs: Any) -> list[dict[str, Any]]:
        """
        Абстрактный метод для получения списка вакансий по параметрам поиска.

        Параметры могут различаться в зависимости от реализации API.
        Ожидаемые параметры (для HH API):
        search_text: Ключевое слово для поиска вакансий.
        excluded_text: Текст для исключения из результатов (опционально).

        :return: Список словарей с данными вакансий.
        """
        ...
