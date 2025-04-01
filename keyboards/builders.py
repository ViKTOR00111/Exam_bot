from pathlib import Path
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def get_years_keyboard():
    task_images_path = Path(__file__).parents[1].joinpath("task_images")
    directory_names = [directory.name for directory in task_images_path.iterdir() if directory.is_dir()]
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


def get_books_keyboard():
    books = ["10 вариантов: \nО.А. Котова, Т.Е. Лискова", "30 вариантов: \nО.А. Котова, Т.Е. Лискова"]
    buttons = [[KeyboardButton(text=book)] for book in books]
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


get_years_keyboard()