from typing import Any


class Validator:
    """Класс для валидации данных с помощью статических методов."""

    @staticmethod
    def str_validation(value: Any, message: str) -> None:
        """
        Проверяет, является ли значение строкой.

        :param value: Проверяемое значение.
        :param message: Сообщение об ошибке, если проверка не пройдена.
        :raises ValueError: Если значение не является строкой.
        """
        if not isinstance(value, str):
            raise ValueError(message)

    @staticmethod
    def integer_validation(value: Any, message: str) -> None:
        """
        Проверяет, является ли значение целым числом.

        :param value: Проверяемое значение.
        :param message: Сообщение об ошибке, если проверка не пройдена.
        :raises TypeError: Если значение не является целым числом.
        """
        if not isinstance(value, int):
            raise TypeError(message)

    @staticmethod
    def positive_integer_validation(value: int, message: str) -> None:
        """
        Проверяет, является ли число положительным целым.

        :param value: Проверяемое число.
        :param message: Сообщение об ошибке, если значение отрицательное.
        :raises TypeError: Если значение не является целым числом.
        :raises ValueError: Если число отрицательное.
        """
        Validator.integer_validation(value, f"Ожидается целое число, получено {type(value).__name__}")
        if value < 0:
            raise ValueError(message)
