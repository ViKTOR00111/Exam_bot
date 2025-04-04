import json
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, ReplyKeyboardRemove
from keyboards.builders import (
    get_years_keyboard,
    get_books_keyboard,
    get_variants_keyboard,
    get_final_keyboard
)
from states.form import Form
from settings import Messages
from pathlib import Path
from utils.book_mapings import find_nickname_book
from loguru import logger

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    username = message.from_user.username or "Неизвестный пользователь"

    logger.trace(f"User {username} (ID: {user_id}) started the bot")
    await message.answer(
        Messages.WELCOME_MESSAGE,
        reply_markup=get_years_keyboard()
    )
    await state.set_state(Form.choosing_year)


@router.message(Form.choosing_year)
async def choose_year_handler(message: Message, state: FSMContext) -> None:
    if message.text.isdigit() and int(message.text) in Messages.YEARS:
        await state.update_data(selected_year=message.text)
        await message.answer(
            f"Выбран год: {message.text}\nТеперь выберите задачник:",
            reply_markup=get_books_keyboard(year=int(message.text))
        )
        logger.trace(f"The user chose the year {message.text}")
        await state.set_state(Form.choosing_book)
    else:
        await message.answer("❌ Пожалуйста, используйте кнопки для выбора года")


@router.message(Form.choosing_book)
async def choose_book_handler(message: Message, state: FSMContext) -> None:
    if message.text in Messages.BOOKS:
        await state.update_data(selected_book=message.text)
        data = await state.get_data()
        await message.answer(
            f"Выбрано: {data['selected_year']} год, {message.text}\nВыберите вариант:",
            reply_markup=get_variants_keyboard(max_variant=int(message.text.split()[0]))
        )
        logger.trace(f"The user chose the book {message.text}")
        await state.set_state(Form.choosing_variant)
    else:
        await message.answer("❌ Пожалуйста, используйте кнопки для выбора задачника")


@router.message(Form.choosing_variant)
async def choose_variant_handler(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    max_variant = int(data["selected_book"].split()[0])

    if message.text.isdigit():
        variant = int(message.text)
        if 1 <= variant <= max_variant:
            await state.update_data(selected_variant=variant)

            logger.trace(f"The user chose the variant {variant}")

            year = data["selected_year"]
            book = find_nickname_book(data["selected_book"])
            answers = load_answer(year, book)
            await state.update_data(answers=answers)

            user_data = {
                "current_task": 1,
                "results": []
            }
            await state.update_data(test_data=user_data)
            await message.answer(
                f"✅ Выбор завершен!\n"
                f"Год: {data['selected_year']}\n"
                f"Задачник: {data['selected_book']}\n"
                f"Вариант: {variant}\n"
                "Нажмите 'Решать задачи', чтобы приступить к заданиям.",
                reply_markup=get_final_keyboard()
            )
        else:
            await message.answer(f"❌ Введите число от 1 до {max_variant}")
    else:
        await message.answer("❌ Пожалуйста, введите номер варианта цифрой")


def load_answer(year, author):
    file_path = Path(__file__).parents[1].joinpath(f"data_answers/{year}_{author}.json")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return {f"{item['variant']}_{item['exercise']}": item['answer'] for item in data['answers']}
    except FileNotFoundError:
        logger.error(f"Файл с ответами для учебника '{year, author}' не найден.")


async def send_task(message: Message, state: FSMContext):
    data = await state.get_data()
    current_task = data["test_data"]["current_task"]
    selected_variant = data["selected_variant"]
    book_name = find_nickname_book(data["selected_book"])
    year = data["selected_year"]

    task_image_path = Path(__file__).parents[1].joinpath("task_images", f"{year}_{book_name}",
                                                         f"{selected_variant}_{current_task}.png")

    try:
        photo = FSInputFile(task_image_path)
        await message.answer_photo(
            photo=photo,
            caption=f"📝 Задание {current_task}:",
            reply_markup=ReplyKeyboardRemove()
        )
        logger.trace(f"Task {task_image_path} has been sent: "
                     f"variant = {selected_variant},"
                     f"book_name = {book_name},"
                     f"year = {year}")
    except FileNotFoundError:
        await message.answer("❌ Не удалось найти заданиe. Попробуйте снова.")
        await state.clear()


@router.callback_query(lambda c: c.data == "reset_all")
async def reset_all_handler(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    logger.trace(f"The user has reset the selection, the FSM is cleared")
    await callback.message.answer(
        "🔄 Выбор сброшен. Выберите год:",
        reply_markup=get_years_keyboard()
    )
    await state.set_state(Form.choosing_year)
    await callback.answer()


@router.message(Form.solving_tasks)
async def handle_task_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    test_data = data["test_data"]
    current_task = test_data["current_task"]
    selected_variant = data["selected_variant"]
    answers = data["answers"]

    if not message.text or not message.text.strip():
        await message.answer("❌ Пожалуйста, отправьте ваш ответ текстом.")
        return

    user_answer = message.text.strip()
    answer_key = f"{selected_variant}_{current_task}"

    if answer_key not in answers:
        await message.answer("❌ Произошла ошибка при проверке ответа. Попробуйте снова.")
        return

    correct_answer = str(answers[answer_key])
    is_correct = user_answer == correct_answer

    result = {
        "task": current_task,
        "user_answer": user_answer,
        "is_correct": is_correct
    }
    test_data["results"].append(result)

    test_data["current_task"] += 1
    await state.update_data(test_data=test_data)

    if is_correct:
        await message.answer("✅ Правильно!")
    else:
        await message.answer(f"❌ Неправильно. Правильный ответ: {correct_answer}")

    if test_data["current_task"] > 16:
        await finish_test(message, state)
    else:
        await send_task(message, state)


async def finish_test(message: Message, state: FSMContext):
    data = await state.get_data()
    results = data["test_data"]["results"]

    total_tasks = len(results)
    correct_tasks = sum(1 for result in results if result["is_correct"])

    result_message = (
        f"🎉 Тест завершен!\n"
        f"Правильных ответов: {correct_tasks}/{total_tasks}\n\n"
        f"📝 Подробные результаты:\n"
    )

    for result in results:
        status = "✅" if result["is_correct"] else "❌"
        result_message += (
            f"{status} Задание {result['task']}: "
            f"Ваш ответ: {result['user_answer']}\n"
        )

    await message.answer(result_message)
    await state.clear()
    logger.trace("The test results have been sent, FSM is cleared")


@router.callback_query(lambda c: c.data == "solve_tasks")
async def solve_tasks_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Form.solving_tasks)
    await send_task(callback.message, state)
    await callback.answer()
