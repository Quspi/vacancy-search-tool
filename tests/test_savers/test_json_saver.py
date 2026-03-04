import json
import os
from unittest.mock import patch

import pytest

from src.savers.json_saver import JSONSaver


def test_init_json_saver():
    saver = JSONSaver("test_init")
    assert os.path.exists(saver._PATH_TO_DATA)
    assert not os.path.exists(saver._path_to_file)


def test_add_vacancy(valid_vacancies):
    saver = JSONSaver("test_add")
    try:
        for vacancy in valid_vacancies:
            result = saver.add_vacancy(vacancy)
            assert vacancy["Ссылка на вакансию"] in saver._url_cache
            assert result is True

        with open(saver._path_to_file, "r", encoding="utf-8") as file:
            data = json.load(file)
            assert len(data) == 5
            for i in range(5):
                assert data[i] == valid_vacancies[i]

    finally:
        if os.path.exists(saver._path_to_file):
            os.remove(saver._path_to_file)


def test_add_same_vacancies(valid_vacancies):
    saver = JSONSaver("test_add_same_vacancies")
    try:
        for vacancy in valid_vacancies:
            result = saver.add_vacancy(vacancy)
            assert result is True

        for vacancy in valid_vacancies:
            result = saver.add_vacancy(vacancy)
            assert result is False

        with open(saver._path_to_file, "r", encoding="utf-8") as file:
            data = json.load(file)
            assert len(data) == 5
            for i in range(5):
                assert data[i] == valid_vacancies[i]

    finally:
        if os.path.exists(saver._path_to_file):
            os.remove(saver._path_to_file)


def test_get_all_vacancies(valid_vacancies):
    saver = JSONSaver("test_get_all")
    try:
        with open(saver._path_to_file, "w", encoding="utf-8") as f:
            json.dump(valid_vacancies, f, ensure_ascii=False, indent=4)

        vacancies = saver.get_all_vacancies()

        assert len(vacancies) == 5
        assert vacancies == valid_vacancies

    finally:
        if os.path.exists(saver._path_to_file):
            os.remove(saver._path_to_file)


def test_delete_vacancy(valid_vacancies):
    saver = JSONSaver("test_delete_vacancy")
    try:
        for vacancy in valid_vacancies:
            saver.add_vacancy(vacancy)

        result = saver.delete_vacancy(valid_vacancies[0])
        vacancies = saver.get_all_vacancies()

        assert result is True
        assert len(vacancies) == 4
        assert vacancies == valid_vacancies[1:]
        assert "https://hh.ru/vacancy/130171080" not in saver._url_cache

    finally:
        if os.path.exists(saver._path_to_file):
            os.remove(saver._path_to_file)


def test_delete_non_existent_vacancy(valid_vacancies):
    saver = JSONSaver("test_delete_same_vacancy")
    try:
        saver.add_vacancy(valid_vacancies[1])
        result = saver.delete_vacancy(valid_vacancies[0])
        vacancy = saver.get_all_vacancies()

        assert len(vacancy) == 1
        assert result is False
        assert vacancy[0] == valid_vacancies[1]

    finally:
        if os.path.exists(saver._path_to_file):
            os.remove(saver._path_to_file)


@patch("builtins.open")
def test_delete_vacancy_file_not_found(mocked_open, valid_vacancies):
    saver = JSONSaver("test_delete_file_not_found")
    saver._url_cache.add(valid_vacancies[0]["Ссылка на вакансию"])
    mocked_open.side_effect = FileNotFoundError

    with pytest.raises(FileNotFoundError, match="Файл не найден или удален"):
        saver.delete_vacancy(valid_vacancies[0])


@patch("builtins.open")
def test_delete_vacancy_json_decode_error(mocked_open, valid_vacancies):
    saver = JSONSaver("test_delete_json_decode_error")
    saver._url_cache.add(valid_vacancies[0]["Ссылка на вакансию"])
    mocked_open.side_effect = json.JSONDecodeError("test", "test", 1)

    with pytest.raises(ValueError, match="Файл поврежден или пуст"):
        saver.delete_vacancy(valid_vacancies[0])


@patch("builtins.open")
def test_get_all_vacancies_file_not_found(mocked_open, valid_vacancies):
    saver = JSONSaver("get_all_vacancies_file_not_found")
    mocked_open.side_effect = FileNotFoundError

    with pytest.raises(FileNotFoundError, match="Файл не найден или удален"):
        saver.get_all_vacancies()


@patch("builtins.open")
def test_get_all_vacancies_json_decode_error(mocked_open, valid_vacancies):
    saver = JSONSaver("get_all_vacancies_json_decode_error")
    mocked_open.side_effect = json.JSONDecodeError("test", "test", 1)

    with pytest.raises(ValueError, match="Файл поврежден или пуст"):
        saver.get_all_vacancies()
