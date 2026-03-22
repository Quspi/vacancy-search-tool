# Приложение поиска вакансий

Проект предоставляет инструменты для поиска вакансий на HeadHunter, фильтрации по зарплате и ключевым словам, а также сохранения результатов в JSON или Excel. Реализован с использованием абстрактных классов, паттернов наследования и покрыт валидацией данных.

![Python 3.12](https://img.shields.io/badge/python-3.12-blue)
![Tests](https://img.shields.io/badge/tests-100%25_passing-success)
![Coverage](https://img.shields.io/badge/coverage-76%25-brightgreen)

## Оглавление

1. [Технологии](#технологии)
2. [Функциональность](#функциональность)
3. [Поддерживаемые форматы данных](#поддерживаемые-форматы-данных)
4. [Логирование](#логирование)
5. [Установка](#установка)
6. [Использование модулей](#использование-модулей)
7. [Тестирование](#тестирование)
8. [Лицензия](#лицензия)
9. [Автор](#автор)

## Технологии
- Python 3.12
- Pandas (анализ данных)
- Requests (API запросы)
- Pytest (тестирование)

## Функциональность

### Реализовано
- Поиск вакансий через API HeadHunter
- Фильтрация по зарплате, ключевым словам и исключающим словам
- Сортировка вакансий по уровню зарплаты
- Сохранение результатов в JSON и Excel
- Валидация входных данных и URL
- Кэширование URL для предотвращения дубликатов

## Поддерживаемые форматы данных
- **Excel**: .xlsx
- **JSON**: .json

## Установка
```
# Клонирование репозитория
git clone https://github.com/Quspi/vacancy-search-tool

# Установка зависимостей
poetry install
```

## Использование модулей
<details>
<summary>API (headhunter_api.py)</summary>

```python
from src.api.headhunter_api import HeadHunterAPI

hh_api = HeadHunterAPI()
vacancies = hh_api.get_vacancies("python", excluded_text="junior")
# Возвращает список словарей с данными вакансий
```
</details>

<details>
<summary>Модели вакансий (vacancy_hh.py)</summary>

```python
from src.models.vacancy_hh import VacancyHH

# Создание вакансии из словаря API
vacancy = VacancyHH.from_api({
    "name": "Python Developer",
    "salary": {"from": 100000, "to": 150000},
    "published_at": "2025-01-01T12:00:00+03:00",
    "alternate_url": "https://hh.ru/vacancy/123",
    "snippet": {"responsibility": "Разработка бэкенда"},
    "experience": {"name": "от 3 лет"},
    "area": {"name": "Москва"} 
})

# Сравнение вакансий по зарплате
if vacancy > 120000:
    print("Высокооплачиваемая вакансия")

# Преобразование в словарь для сохранения
vacancy_dict = vacancy.to_dict()
```
</details>

<details>
<summary>Сохранение (json_saver.py, excel_saver.py)</summary>

```python
# JSON
json_saver = JSONSaver("my_vacancies")
json_saver.add_vacancy(vacancy_dict)  # Возвращает True/False
all_vacancies = json_saver.get_all_vacancies()
json_saver.delete_vacancy(vacancy_dict)

# Excel
excel_saver = ExcelSaver("my_vacancies")
excel_saver.add_vacancy(vacancy_dict)
```
</details>

<details>
<summary>Утилиты (utils.py)</summary>

```python
from src.utils import (
    get_search_string,
    get_salary_range,
    filter_by_salary_range,
    sort_by_salary,
    filter_by_keywords,
    transform_to_dict,
    choice_menu,
    output_data
)

# Получение параметров от пользователя
search_text = get_search_string()
min_salary, max_salary = get_salary_range()
keywords = get_keywords()

# Вакансии после API и преобразования в объекты
vacancies = VacancyHH.from_api_list(hh_response)
filtered_by_salary = filter_by_salary_range(vacancies, (50000, 150000))
dict_vacancies = transform_to_dict(filtered_by_salary)
filtered_vacancies = filter_by_keywords(dict_vacancies, keywords)

# Сортировка и вывод
sorted_vacancies = sort_by_salary(filtered_vacancies)
choice = choice_menu()
output_data(sorted_vacancies, choice, quantity=10)
```
</details>

<details>
<summary>Основной сценарий (main.py)</summary>

Файл `main.py` демонстрирует работу всех функциональностей проекта:

```bash
# Запуск демонстрации
python main.py
```

Что выполняется при запуске:
- Запрос параметров поиска (ключевая фраза, диапазон зарплаты, ключевые слова)
- Получение вакансий через API HeadHunter
- Фильтрация вакансий по зарплате и ключевым словам
- Сортировка по уровню зарплаты (опционально)
- Вывод результатов в консоль или сохранение в JSON/Excel

Результаты:
- Найденные вакансии выводятся в консоль в формате JSON
- Файлы сохраняются в папку data/ с указанным пользователем именем
- Автоматическая проверка дубликатов при сохранении

</details>

## Тестирование

Проект покрыт юнит-тестами Pytest. Для их запуска выполните команды:
```
# Запуск всех тестов
pytest

# Запуск с отчетом о покрытии в консоли
pytest --cov=src

# Генерация HTML отчета о покрытии (будет создана папка htmlcov/)
pytest --cov=src --cov-report=html
```

## Лицензия
Этот проект распространяется под лицензией MIT.

## Автор
**Oleg Tamanov**

Email: olegtamanov@gmail.com