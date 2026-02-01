import json

from src.models.base_vacancy import BaseVacancy
from src.savers.excel_saver import ExcelSaver
from src.savers.json_saver import JSONSaver


def get_search_string() -> str:
    """
    Запрашивает поисковую фразу для запроса вакансий.

    :return: Строка с поисковым запросом в нижнем регистре.
    """
    while True:
        search_string = input("Введите фразу для поиска вакансий: \n").strip().lower()
        if search_string:
            return search_string
        print("Поле не может быть пустым, повторите ввод")


def get_salary_range() -> tuple[int, int]:
    """
    Запрашивает диапазон заработной платы в формате 'min-max'.

    :return: Кортеж из двух целых чисел.
    """
    while True:
        try:
            salary_range = input("Введите диапазон з/п в рублях (40000 - 60000): \n").replace(" ", "").split("-")
            if len(salary_range) != 2:
                print("Некорректно введен диапазон з/п, повторите ввод")
                continue
            min_salary, max_salary = tuple(map(int, salary_range))
            if min_salary < 0 or min_salary > max_salary:
                print("Некорректно введен диапазон з/п, повторите ввод")
                continue
            return min_salary, max_salary
        except ValueError:
            print("Диапазон з/п должен состоять из целых чисел")


def get_keywords() -> list[str]:
    """
    Запрашивает ключевые слова для поиска в описании вакансий.

    :return: Список строк в нижнем регистре.
    """
    while True:
        search_string = (
            input("Введите ключевые слова для поиска в описании вакансии (через пробел): \n").strip().lower().split()
        )
        if search_string:
            return search_string
        print("Поле не может быть пустым, повторите ввод")


def get_excluded_text() -> str:
    """
    Запрашивает ключевые слова для исключения из поиска.

    :return: Строка с ключевыми словами, разделёнными запятыми.
    """
    while True:
        search_string = (
            input("Введите ключевые слова для исключения из поиска в описании вакансии (через пробел): \n")
            .strip()
            .lower()
            .split()
        )
        if search_string:
            return ",".join(search_string)
        print("Поле не может быть пустым, повторите ввод")


def get_quantity_vacancies() -> int:
    """
    Запрашивает количество вакансий для вывода в результате.

    :return: Неотрицательное целое число.
    """
    while True:
        try:
            quantity = int(input("Введите желаемое кол-во вакансий для вывода: \n"))
            if quantity < 0:
                print("Количество не может быть отрицательным")
                continue
            return quantity
        except ValueError:
            print("Количество должно быть целым числом")


def ask_question(question: str) -> bool:
    """
    Задаёт пользователю вопрос с ответом Да/Нет.

    :param question: Текст вопроса.

    :return: True если ответ "да", False если "нет".
    """
    while True:
        answer = input(f"{question} (Да/Нет): \n").strip().lower()
        if answer == "да":
            return True
        elif answer == "нет":
            return False


def get_filename() -> str:
    """
    Запрашивает имя файла для сохранения данных.

    :return: Строка с именем файла.
    """
    while True:
        filename = input("Введите имя файла: \n").strip()
        if filename:
            return filename
        print("Имя файла не может быть пустым, повторите ввод")


def filter_by_salary_range(vacancies: list[BaseVacancy], salary_range: tuple[int, int]) -> list[BaseVacancy]:
    """
    Фильтрует вакансии по диапазону заработной платы.

    :param vacancies: Список вакансий (BaseVacancy).
    :param salary_range: Кортеж (min, max) зарплаты.

    :return: Отфильтрованный список вакансий.
    """
    min_salary, max_salary = salary_range
    result = [vacancy for vacancy in vacancies if vacancy == 0 or min_salary <= vacancy <= max_salary]
    return result


def transform_to_dict(vacancies: list[BaseVacancy]) -> list[dict[str, str | int]]:
    """
    Преобразует список объектов BaseVacancy в список словарей.

    :param vacancies: Список объектов вакансий (BaseVacancy).

    :return: Список словарей с данными вакансий.
    """
    return [vacancy.to_dict() for vacancy in vacancies]


def sort_by_salary(vacancies: list[dict[str, str | int]]) -> list[dict[str, str | int]]:
    """
    Сортирует вакансии по уровню зарплаты (по убыванию).

    :param vacancies: Список словарей с вакансиями.

    :return: Отсортированный список.
    """
    return sorted(vacancies, key=lambda x: x.get("Заработная плата", 0), reverse=True)


def filter_by_keywords(vacancies: list[dict[str, str | int]], keywords: list[str]) -> list[dict[str, str | int]]:
    """
    Фильтрует вакансии по наличию ключевых слов в описании обязанностей.

    :param vacancies: Список словарей с вакансиями.
    :param keywords: Список ключевых слов для поиска.

    :return: Отфильтрованный список вакансий.
    """
    result_list = []
    for vacancy in vacancies:
        responsibilities = str(vacancy.get("Обязанности", ""))
        if responsibilities is None:
            continue

        if any(keyword in responsibilities.lower() for keyword in keywords):
            result_list.append(vacancy)

    return result_list


def choice_menu() -> str:
    """
    Предлагает пользователю выбрать действие с результатами поиска.

    :return: Строка с номером выбранного действия ("1", "2", "3").
    """
    while True:
        answer = input(
            "Выберете действие:\n"
            "1. Вывести результат в консоль\n"
            "2. Сохранить результат в JSON файл\n"
            "3. Сохранить результат в Excel\n"
        )
        if answer not in ["1", "2", "3"]:
            print("Некорректный выбор, повторите ввод")
            continue
        return answer


def output_data(vacancies: list[dict[str, str | int]], choice: str, quantity_vacancies: int) -> None:
    """
    Выводит или сохраняет результаты поиска в зависимости от выбора пользователя.

    :param vacancies: Список вакансий для обработки.
    :param choice: Выбор действия ("1" - консоль, "2" - JSON, "3" - Excel).
    :param quantity_vacancies: Количество вакансий для вывода.
    """
    vacancies = vacancies[:quantity_vacancies]

    if choice == "1":
        print(json.dumps(vacancies, indent=4, ensure_ascii=False))

    elif choice == "2":
        filename = get_filename()
        json_saver = JSONSaver(filename)
        for vacancy in vacancies:
            json_saver.add_vacancy(vacancy)
        print("Вакансии успешно загружены в JSON файл")

    elif choice == "3":
        filename = get_filename()
        excel_saver = ExcelSaver(filename)
        for vacancy in vacancies:
            excel_saver.add_vacancy(vacancy)
        print("Вакансии успешно загружены в Excel файл")
