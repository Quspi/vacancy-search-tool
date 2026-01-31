import pandas as pd

from src.savers.base_saver import BaseSaver


class ExcelSaver(BaseSaver):
    """
    Сохраняет вакансии в Excel-файл.
    Наследуется от BaseSaver, использует кэш URL для предотвращения дубликатов.
    """

    _extension = "xlsx"

    def __init__(self, filename: str = "vacancies") -> None:
        """
        Инициализирует объект для работы с Excel.

        :param filename: Имя файла без расширения .xlsx

        :raise TypeError: Если имя файла не строка.
        """
        super().__init__(filename)

    def get_all_vacancies(self) -> list[dict]:
        """
        Возвращает все вакансии из Excel-файла.

        :return: Список всех вакансий.

        :raises FileNotFoundError: Если файл не найден.
        :raises ValueError: Если файл пуст или повреждён.
        """
        try:
            df = pd.read_excel(self._path_to_file)
            data = df.to_dict(orient="records")
            return data

        except FileNotFoundError:
            raise FileNotFoundError("Файл не найден или удален")

        except pd.errors.EmptyDataError as error:
            raise ValueError("Файл пуст или поврежден") from error

    def add_vacancy(self, vacancy: dict[str, int | str]) -> None:
        """
        Добавляет вакансию в Excel-файл.

        :param vacancy: Словарь с данными о вакансии.

        :raises ValueError: Если структура данных неверна.
        """
        self._validate_vacancy(vacancy)

        vacancy_url = vacancy["Ссылка на вакансию"]
        if vacancy_url in self._url_cache:
            return None

        try:
            df = pd.read_excel(self._path_to_file)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            df = pd.DataFrame()

        vacancy_df = pd.DataFrame([vacancy])

        result_data = pd.concat([df, vacancy_df], ignore_index=True)
        result_data.to_excel(self._path_to_file, index=False)
        self._url_cache.add(vacancy_url)

        return None

    def delete_vacancy(self, vacancy: dict[str, int | str]) -> None:
        """
        Удаляет вакансию из Excel-файла.

        :param vacancy: Словарь с данными вакансии.

        :raises ValueError: Если структура данных неверна.
        :raises FileNotFoundError: Если файл не найден.
        :raises ValueError: Если файл пуст или повреждён.
        """
        self._validate_vacancy(vacancy)

        vacancy_url = vacancy["Ссылка на вакансию"]
        if vacancy_url not in self._url_cache:
            return None

        try:
            df = pd.read_excel(self._path_to_file)
        except FileNotFoundError:
            raise FileNotFoundError("Файл не найден или удален")

        except pd.errors.EmptyDataError as error:
            raise ValueError("Файл пуст или поврежден") from error

        new_df: pd.DataFrame = df.loc[df["Ссылка на вакансию"] != vacancy_url]
        new_df.to_excel(self._path_to_file, index=False)
        self._url_cache.remove(vacancy_url)

        return None
