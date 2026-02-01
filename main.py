from src.api.headhunter_api import HeadHunterAPI
from src.models.vacancy_hh import VacancyHH
from src.utils.utils import (ask_question, choice_menu, filter_by_keywords, filter_by_salary_range, get_excluded_text,
                             get_keywords, get_quantity_vacancies, get_salary_range, get_search_string, output_data,
                             sort_by_salary, transform_to_dict)

hh_api = HeadHunterAPI()


def user_interaction() -> None:
    """
    Основная функция взаимодействия с пользователем через консоль.

    Выполняет последовательно:
    1. Запрашивает параметры поиска (фраза, зарплата, ключевые слова).
    2. Получает вакансии через API HeadHunter.
    3. Фильтрует вакансии по зарплате и ключевым словам.
    4. Выводит количество найденных вакансий.
    5. Предлагает сортировку по зарплате.
    6. Предлагает выбор действия (вывод в консоль, сохранение в JSON/Excel).
    7. Выполняет выбранное действие.
    """
    search_string = get_search_string()
    salary_range = get_salary_range()
    keywords = get_keywords()

    excluded_text = None
    if ask_question("Указать ключевые слова для исключения из поиска?"):
        excluded_text = get_excluded_text()

    hh_response = hh_api.get_vacancies(search_string, excluded_text)
    vacancies = VacancyHH.from_api_list(hh_response)

    filtered_by_salary = filter_by_salary_range(vacancies, salary_range)
    dict_vacancies = transform_to_dict(filtered_by_salary)
    filtered_vacancies = filter_by_keywords(dict_vacancies, keywords)

    count = len(filtered_vacancies)
    if count == 0:
        print("Не найдено вакансий удовлетворяющим условиям поиска\nПрограмма завершила работу")
        return

    print(
        f"Найдено {count} вакансий удовлетворяющим условиям поиска, включая вакансии в которых не указан уровень з/п"
    )
    if ask_question("Отсортировать вакансии по уровню з/п?"):
        filtered_vacancies = sort_by_salary(filtered_vacancies)
        print("Вакансии отсортированы по уровню з/п, вакансии в которых не указан уровень з/п перемещены в конец")

    quantity_vacancies = get_quantity_vacancies()
    choice = choice_menu()
    output_data(filtered_vacancies, choice, quantity_vacancies)
    print("Программа завершила работу")


if __name__ == "__main__":
    user_interaction()
