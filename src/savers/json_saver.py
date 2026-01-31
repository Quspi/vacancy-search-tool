import json
from typing import cast

from src.savers.base_saver import BaseSaver


class JSONSaver(BaseSaver):
    """
    Сохраняет вакансии в JSON-файл.
    Наследуется от BaseSaver, использует кэш URL для предотвращения дубликатов.
    """

    _extension = "json"

    def __init__(self, filename: str = "vacancies") -> None:
        """
        Инициализирует объект для работы с JSON.

        :param filename: Имя файла без расширения .json

        :raise TypeError: Если имя файла не строка.
        """
        super().__init__(filename)

    def get_all_vacancies(self) -> list[dict]:
        """
        Возвращает все вакансии из JSON-файла.

        :return: Список словарей с вакансиями.

        :raises FileNotFoundError: Если файл не найден.
        :raises ValueError: Если файл повреждён или битый JSON.
        """
        try:
            with open(self._path_to_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                data = cast(list[dict], data)
                return data

        except FileNotFoundError:
            raise FileNotFoundError("Файл не найден или удален")

        except json.JSONDecodeError as error:
            raise ValueError("Файл поврежден или пуст") from error

    def add_vacancy(self, vacancy: dict[str, str | int]) -> bool:
        """
        Добавляет вакансию в JSON-файл.
        Возвращает True/False в зависимости от успешности операции.

        :param vacancy: Словарь с данными о вакансии.

        :raises ValueError: Если структура данных вакансии неверна.
        """
        self._validate_vacancy(vacancy)

        vacancy_url = vacancy["Ссылка на вакансию"]
        if vacancy_url in self._url_cache:
            return False

        try:
            with open(self._path_to_file, "r+", encoding="utf-8") as file:
                data = json.load(file)

                data.append(vacancy)
                self._url_cache.add(vacancy_url)

                file.seek(0)
                file.truncate()
                json.dump(data, file, indent=4, ensure_ascii=False)

        except (FileNotFoundError, json.JSONDecodeError):
            with open(self._path_to_file, "w", encoding="utf-8") as file:
                json.dump([vacancy], file, indent=4, ensure_ascii=False)
                self._url_cache.add(vacancy_url)

        return True

    def delete_vacancy(self, vacancy: dict[str, str | int]) -> bool:
        """
        Удаляет вакансию из JSON-файла.
        Возвращает True/False в зависимости от успешности операции.

        :param vacancy: Словарь с данными вакансии.

        :raises ValueError: Если структура данных неверна.
        :raises FileNotFoundError: Если файл не найден.
        :raises ValueError: Если файл повреждён.
        """
        self._validate_vacancy(vacancy)

        vacancy_url = vacancy["Ссылка на вакансию"]
        if vacancy_url not in self._url_cache:
            return False

        try:
            with open(self._path_to_file, "r+", encoding="utf-8") as file:
                data = json.load(file)

                for v in data:
                    if v.get("Ссылка на вакансию") == vacancy_url:
                        data.remove(v)
                        break

                file.seek(0)
                file.truncate()
                json.dump(data, file, indent=4, ensure_ascii=False)
                self._url_cache.remove(vacancy_url)

        except FileNotFoundError:
            raise FileNotFoundError("Файл не найден или удален")

        except json.JSONDecodeError as error:
            raise ValueError("Файл поврежден или пуст") from error

        return True
