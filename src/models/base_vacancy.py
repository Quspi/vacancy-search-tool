from abc import ABC, abstractmethod


class BaseVacancy(ABC):
    """
    Абстрактный базовый класс для представления вакансии.

    Определяет общую структуру и обязательные методы для всех типов вакансий.
    """

    salary: int

    __slots__ = (
        "name",
        "salary",
        "date",
        "url",
        "responsibility",
        "experience",
        "area",
    )

    @abstractmethod
    def __init__(
        self, name: str, salary: int, date: str, url: str, responsibility: str, experience: str, area: str
    ) -> None:
        """Инициализирует объект вакансии."""
        ...

    @abstractmethod
    def __str__(self) -> str:
        """Строковое представление вакансии."""
        ...

    @abstractmethod
    def __lt__(self, other: object) -> bool:
        """
        Сравнивает вакансии по зарплате.

        :param other: Объект для сравнения.

        :return: True, если зарплата текущей вакансии меньше.

        :raises TypeError: Если other не является экземпляром BaseVacancy.
        """
        ...

    @abstractmethod
    def __le__(self, other: object) -> bool:
        """
        Сравнивает вакансии по зарплате.

        :param other: Объект для сравнения.

        :return: True, если зарплата текущей вакансии меньше или равна.

        :raises TypeError: Если other не является экземпляром BaseVacancy.
        """
        ...

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        """
        Сравнивает вакансии по зарплате.

        :param other: Объект для сравнения.

        :return: True, если зарплаты равны.

        :raises TypeError: Если other не является экземпляром BaseVacancy.
        """
        ...

    @abstractmethod
    def __ne__(self, other: object) -> bool:
        """
        Сравнивает вакансии по зарплате.

        :param other: Объект для сравнения.

        :return: True, если зарплаты не равны.

        :raises TypeError: Если other не является экземпляром BaseVacancy.
        """
        ...

    @abstractmethod
    def __gt__(self, other: object) -> bool:
        """
        Сравнивает вакансии по зарплате.

        :param other: Объект для сравнения.

        :return: True, если зарплата текущей вакансии больше.

        :raises TypeError: Если other не является экземпляром BaseVacancy.
        """
        ...

    @abstractmethod
    def __ge__(self, other: object) -> bool:
        """
        Сравнивает вакансии по зарплате.

        :param other: Объект для сравнения.

        :return: True, если зарплата текущей вакансии больше или равна.

        :raises TypeError: Если other не является экземпляром BaseVacancy.
        """
        ...

    @classmethod
    @abstractmethod
    def from_dict(cls, vacancies_dict: dict) -> "BaseVacancy":
        """Создаёт экземпляр вакансии из словаря."""
        ...

    @classmethod
    @abstractmethod
    def from_list(cls, vacancies_list: list[dict]) -> list["BaseVacancy"]:
        """Создаёт список экземпляров вакансий из списка словарей."""
        ...

    @abstractmethod
    def to_dict(self) -> dict[str, int]:
        """Преобразует объект вакансии в словарь."""
        ...
