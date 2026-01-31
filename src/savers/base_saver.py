import os
from abc import ABC, abstractmethod
from typing import Any

from src.utils.validator import Validator


class BaseSaver(ABC):
    """
    Базовый абстрактный класс для сохранения вакансий в файлы.
    Обеспечивает общую логику: создание директории data, кэш URL, интерфейс методов.
    Наследники определяют конкретный формат (JSON, Excel и др.).

    Структура данных вакансии должна соблюдаться для всех классов наследников и быть в виде словаря с ключами:
    - "Название вакансии": (str)
    - "Заработная плата": (int)
    - "Дата публикации": (str)
    - "Ссылка на вакансию": (str)
    - "Обязанности": (str)
    - "Опыт работы": (str)
    - "Город": (str).
    """

    _extension: str
    """Расширение файла. Переопределяется в дочерних классах."""

    _BASE_DIR_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    """Абсолютный путь к корневой директории проекта."""

    _PATH_TO_DATA = os.path.join(_BASE_DIR_PATH, "data")
    """Путь к директории 'data' для хранения файлов."""

    def __init__(self, filename: str = "vacancies") -> None:
        """
        Инициализирует объект класса для работы с файлами.

        :param filename: Имя файла без расширения.

        :raises TypeError: Если имя файла не строка.
        """
        Validator.str_validation(filename, "Имя файла должно быть строкой")
        os.makedirs(self._PATH_TO_DATA, exist_ok=True)
        self._path_to_file = os.path.join(self._PATH_TO_DATA, f"{filename}.{self._extension}")
        self._url_cache: set[str | Any] = set()
        self._load_cache()

    @abstractmethod
    def add_vacancy(self, vacancy: dict[str, int | str]) -> None:
        """
        Добавляет одну вакансию в файл.

        :param vacancy: Словарь с данными о вакансии.

        :raises ValueError: При неверной структуре данных.
        """
        ...

    @abstractmethod
    def delete_vacancy(self, vacancy: dict[str, int | str]) -> None:
        """
        Удаляет одну вакансию из файла.

        :param vacancy: Словарь с данными для удаления.

        :raises ValueError: При неверной структуре данных.
        :raises FileNotFoundError: Если файл не найден.
        """
        ...

    @abstractmethod
    def get_all_vacancies(self) -> list[dict]:
        """
        Возвращает все вакансии из файла.

        :return: Список словарей с вакансиями.

        :raises FileNotFoundError: Если файл не найден.
        :raises ValueError: Если файл повреждён.
        """
        ...

    def _load_cache(self) -> None:
        """
        Загружает URL вакансий из файла в кэш.
        Используется для проверки дубликатов.
        """
        if os.path.exists(self._path_to_file):
            data = self.get_all_vacancies()
            for vacancy in data:
                vacancy_url = vacancy.get("Ссылка на вакансию")
                self._url_cache.add(vacancy_url)
