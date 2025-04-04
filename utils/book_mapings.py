import json
from pathlib import Path
from typing import List
from settings import config


def load_book_mapings(file: str = config.FILE_BOOK_MAPINGS):
    """
    Функция загружает файл конфигурацию с парами:
    "Название книги, отправляемое пользователю": "Псевдоним в файловой системе"

    :param file:
    :return: json-объект
    """

    file_path = Path(__file__).parents[1].joinpath("venv", file)

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        raise FileNotFoundError("Файл book_mappings.json не найден.")


def find_nickname_book(book: str):
    """
    Фукнция ищет в файле конфигурации псведоним,
    используемый в файловой системе для названия книги,
    которое отправляется пользователю

    :param book:
    :return:
    """

    books = load_book_mapings()
    nick_name = books.get(book)

    if nick_name:
        return nick_name
    else:
        raise ValueError("Книга не найдена")


def find_title_book(nicknames: List[str]):
    """
    Функция принимает список псевдонимов книг,
    которые используются в файловой системе, и возрващает список
    названий книг из конфигурационного файла

    :param nicknames: Список псевдонимов для поиска
    :return: Список названий книг
    """

    books = load_book_mapings()
    result = [key for key, value in books.items() if value in nicknames]
    return result


