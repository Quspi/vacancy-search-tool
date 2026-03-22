import os
from unittest.mock import patch

import pandas as pd
import pytest

from src.savers.excel_saver import ExcelSaver


def test_init_json_saver():
    saver = ExcelSaver("test_init")
    assert os.path.exists(saver._PATH_TO_DATA)
    assert not os.path.exists(saver._path_to_file)


def test_add_vacancy(valid_vacancies):
    saver = ExcelSaver("test_add")

    try:
        for vacancy in valid_vacancies:
            result = saver.add_vacancy(vacancy)
            assert vacancy["Ссылка на вакансию"] in saver._url_cache
            assert result is True

        df = pd.read_excel(saver._path_to_file)
        assert len(df) == 5
        data = df.to_dict(orient="records")

        for i in range(5):
            assert data[i] == valid_vacancies[i]

    finally:
        if os.path.exists(saver._path_to_file):
            os.remove(saver._path_to_file)


def test_add_same_vacancy(valid_vacancies):
    saver = ExcelSaver("test_add_same")

    try:
        for vacancy in valid_vacancies:
            result = saver.add_vacancy(vacancy)
            assert vacancy["Ссылка на вакансию"] in saver._url_cache
            assert result is True

        for vacancy in valid_vacancies:
            result = saver.add_vacancy(vacancy)
            assert result is False

        df = pd.read_excel(saver._path_to_file)
        assert len(df) == 5
        data = df.to_dict(orient="records")

        for i in range(5):
            assert data[i] == valid_vacancies[i]

    finally:
        if os.path.exists(saver._path_to_file):
            os.remove(saver._path_to_file)


def test_get_all_vacancies(valid_vacancies):
    saver = ExcelSaver("get_all_vacancies")

    try:
        df = pd.DataFrame(valid_vacancies)
        df.to_excel(saver._path_to_file, index=False)

        data = saver.get_all_vacancies()

        for i in range(5):
            assert data[i] == valid_vacancies[i]

    finally:
        if os.path.exists(saver._path_to_file):
            os.remove(saver._path_to_file)


@patch("pandas.read_excel")
def test_get_all_vacancies_file_not_found(mock_read):
    saver = ExcelSaver("file_not_found")

    mock_read.side_effect = FileNotFoundError()

    with pytest.raises(FileNotFoundError, match="Файл не найден или удален"):
        saver.get_all_vacancies()


@patch("pandas.read_excel")
def test_get_all_vacancies_empty_data(mock_read):
    saver = ExcelSaver("empty_data")

    mock_read.side_effect = pd.errors.EmptyDataError()

    with pytest.raises(ValueError, match="Файл пуст или поврежден"):
        saver.get_all_vacancies()


def test_delete_vacancy(valid_vacancies):
    saver = ExcelSaver("test_delete")

    try:
        for vacancy in valid_vacancies:
            result = saver.add_vacancy(vacancy)
            assert vacancy["Ссылка на вакансию"] in saver._url_cache
            assert result is True

        result = saver.delete_vacancy(valid_vacancies[4])
        data = saver.get_all_vacancies()

        assert len(data) == 4
        assert result is True
        assert valid_vacancies[4]["Ссылка на вакансию"] not in saver._url_cache

        for i in range(4):
            assert valid_vacancies[i] == data[i]
            assert valid_vacancies[i]["Ссылка на вакансию"] in saver._url_cache

    finally:
        if os.path.exists(saver._path_to_file):
            os.remove(saver._path_to_file)


def test_delete_vacancy_non_existent_vacancy(valid_vacancies):
    saver = ExcelSaver("test_delete_non_existent_vacancy")

    try:
        saver.add_vacancy(valid_vacancies[1])
        result = saver.delete_vacancy(valid_vacancies[0])
        vacancy = saver.get_all_vacancies()

        assert result is False
        assert len(vacancy) == 1
        assert vacancy[0] == valid_vacancies[1]

    finally:
        if os.path.exists(saver._path_to_file):
            os.remove(saver._path_to_file)


@patch("pandas.read_excel")
def test_delete_vacancy_file_not_found(mock_read, valid_vacancies):
    saver = ExcelSaver("file_not_found_delete")

    mock_read.side_effect = FileNotFoundError()
    saver._url_cache.add(valid_vacancies[0]["Ссылка на вакансию"])

    with pytest.raises(FileNotFoundError, match="Файл не найден или удален"):
        saver.delete_vacancy(valid_vacancies[0])


@patch("pandas.read_excel")
def test_delete_vacancy_empty_data(mock_read, valid_vacancies):
    saver = ExcelSaver("file_empty_data")

    mock_read.side_effect = pd.errors.EmptyDataError()
    saver._url_cache.add(valid_vacancies[0]["Ссылка на вакансию"])

    with pytest.raises(ValueError, match="Файл пуст или поврежден"):
        saver.delete_vacancy(valid_vacancies[0])


def test_validate_vacancy_negative():
    saver = ExcelSaver("test_validate_vacancy")

    with pytest.raises(ValueError, match="Ошибка в структуре данных вакансии"):
        saver.add_vacancy({"Название вакансии": "Разработчик"})


@patch("os.path.exists")
def test_load_cache_file_not_exists(mock_os_patch):
    mock_os_patch.return_value = False
    saver = ExcelSaver("non_existent_file")

    assert len(saver._url_cache) == 0
    assert saver._url_cache == set()


def test_load_cache(valid_vacancies):
    saver = ExcelSaver("test_cache")

    try:
        saver.add_vacancy(valid_vacancies[0])
        saver._load_cache()
        assert saver._url_cache == {"https://hh.ru/vacancy/130171080"}

    finally:
        if os.path.exists(saver._path_to_file):
            os.remove(saver._path_to_file)
