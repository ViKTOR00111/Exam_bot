from keyboards.builders import get_task_folders
from settings import config


class Messages:
    WELCOME_MESSAGE = ("Привет! Я - бот для решения тестовой части ЕГЭ по обществознанию.\n"
                       "Для того, чтобы продолжить, выбери год задачника из вариантов в телеграмм-клавиатуре.\n"
                       "Удачи!")
    BOOKS = [
        "10 вариантов: \nО.А. Котова, Т.Е. Лискова",
        "30 вариантов: \nО.А. Котова, Т.Е. Лискова"
    ]

    YEARS = list(
        set(
            [int(year[:4]) for year in get_task_folders(config.TASKS_FOLDER)]
        )
    )