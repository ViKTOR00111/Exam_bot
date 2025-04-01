import json
from pathlib import Path


def load_book_mapings():
    file_path = Path(__file__).parents[1].joinpath("venv", "book_mappings.json")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        raise FileNotFoundError("Файл book_mappings.json не найден.")


def find_book(finding_book):
    books = load_book_mapings()
    file_name = books.get(finding_book)

    if file_name:
        return file_name
    else:
        raise ValueError("Книга не найдена")
