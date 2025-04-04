from pathlib import Path
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from utils.book_mapings import find_title_book
from settings import config


def get_task_folders(path: str):
    task_path = Path(__file__).parents[1].joinpath(path)
    directory_names = [directory.name for directory in task_path.iterdir() if directory.is_dir()]
    return directory_names


def get_years_keyboard():
    directory_names = get_task_folders(config.TASKS_FOLDER)
    years = [year[:4] for year in directory_names]
    unique_years = list(set(years))

    buttons = [
        [KeyboardButton(text=str(year)) for year in unique_years[i:i + 2]]
        for i in range(0, len(years), 3)
    ]
    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )


def get_books_keyboard(year: int):
    directory_names = get_task_folders(config.TASKS_FOLDER)
    books = [name[5:] for name in directory_names if int(name[:4]) == year]
    unique_books = list(set(books))

    title_books = find_title_book(unique_books)
    buttons = [[KeyboardButton(text=book)] for book in title_books]
    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )


def get_variants_keyboard(max_variant):
    buttons = []
    for i in range(1, max_variant+1, 5):
        row = [KeyboardButton(text=str(num)) for num in range(i, min(i+5, max_variant+1))]
        buttons.append(row)
    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )


def get_final_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Решать задачи", callback_data="solve_tasks")],
        [InlineKeyboardButton(text="❌ Сбросить всё", callback_data="reset_all")]
    ])