import os
import uuid

from aiogram import types, Router
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from keyboards import admin_keyboard
from state.admin import AdminState
from bd import Db

ADMIN_IDS = "1383157406"
db = Db()
router = Router()



@router.message(Command("admin"))
async def cmd_start(message: types.Message):
    if str(message.from_user.id) == ADMIN_IDS:
        await message.reply("Привет!👋 Это административная панель бота.", reply_markup=admin_keyboard.main_admin)
    else:
        await message.answer(text="Нет доступа")


@router.callback_query(F.data == "kategory_admin")
async def category_admin(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(text="📍Управление категориями", reply_markup=admin_keyboard.kategory_admin)


@router.callback_query(F.data == "back_admin")
async def category_admin(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(text="📍Главное меню", reply_markup=admin_keyboard.main_admin)


@router.callback_query(F.data == "add_category")
async def add_category(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Введите категорию, которую хотите добавить...",
                                  reply_markup=admin_keyboard.back_admin)
    await state.set_state(AdminState.category)
    await callback.message.delete()


@router.message(AdminState.category)
async def category_state(msg: types.Message, state: FSMContext):
    category = msg.text
    db.insert_category(category)
    await msg.answer(text=f"Категория успешно добавлена!")
    await msg.answer(text="📍Главное меню", reply_markup=admin_keyboard.main_admin)
    await state.clear()


@router.callback_query(F.data == "get_category")
async def get_categories(callback: types.CallbackQuery):
    categories = db.select_category()
    if not categories:
        await callback.message.answer(text="Нет доступных категорий!", reply_markup=admin_keyboard.kategory_admin)
    else:
        categories_text = "\n\n".join(
            f"<b>ID:</b> {category[0]}\n<b>Имя категории:</b> {category[1]}" for category in categories)
        await callback.message.answer(text=f"Доступные категории:\n{categories_text}",
                                      reply_markup=admin_keyboard.kategory_admin)
    await callback.message.delete()


@router.callback_query(F.data == "delete_category")
async def get_categories(callback: types.CallbackQuery, state: FSMContext):
    category_select = db.select_category()

    if not category_select:
        await callback.message.answer(text="Нет доступных категорий для удаления.")
        return

    categories_text = "\n\n".join(
        f"<b>ID:</b> {category[0]}\n<b>Имя категории:</b> {category[1]}" for category in category_select)
    await callback.message.answer(text=f"<b>Ниже представлены все доступные категории</b>\n\n{categories_text}")
    await callback.message.answer(text="Введите <b>ID</b> категории, которую хотите удалить!")
    await state.set_state(AdminState.delete_category)
    await callback.message.delete()


@router.message(AdminState.delete_category)
async def category_state(msg: types.Message, state: FSMContext):
    category_id = msg.text
    if not db.delete_category_by_id(category_id):  # Проверка на неудачное удаление
        await msg.answer(text=f"Категория с ID {category_id} не найдена.")
    else:
        await msg.answer(text=f"Категория с ID {category_id} успешно удалена!")
    await msg.answer(text="📍Главное меню", reply_markup=admin_keyboard.main_admin)
    await state.clear()


# Каталог авто

@router.callback_query(F.data == "katalog_admin")
async def get_categories(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("📍Каталог авто", reply_markup=admin_keyboard.auto_admin)


@router.callback_query(F.data == "add_auto")
async def get_categories(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer("<b>Введите название машины!</b>", reply_markup=admin_keyboard.back_admin)
    await state.set_state(AdminState.name_auto)


@router.message(AdminState.name_auto)
async def category_state(msg: types.Message, state: FSMContext):
    name_auto = msg.text
    await state.update_data(name_auto=name_auto)
    await msg.answer(text="<b>Введите цену машины!</b>", reply_markup=admin_keyboard.back_admin)
    await state.set_state(AdminState.price)


@router.message(AdminState.price)
async def category_state(msg: types.Message, state: FSMContext):
    price = msg.text
    await state.update_data(price=price)
    await msg.answer(text="<b>Напишите описание машины!</b>", reply_markup=admin_keyboard.back_admin)
    await state.set_state(AdminState.description)


@router.message(AdminState.description)
async def category_state(msg: types.Message, state: FSMContext):
    description = msg.text
    await state.update_data(description=description)
    await msg.answer(text="<b>Введите название картинки!</b>", reply_markup=admin_keyboard.back_admin)
    await state.set_state(AdminState.img)


@router.message(AdminState.img)
async def category_state(msg: types.Message, state: FSMContext):
    img = msg.text
    await state.update_data(img=img)
    await msg.answer(text="<b>Введите количество машин!</b>", reply_markup=admin_keyboard.back_admin)
    await state.set_state(AdminState.kolvo)


@router.message(AdminState.kolvo)
async def category_state(msg: types.Message, state: FSMContext):
    kolvo = msg.text
    await state.update_data(kolvo=kolvo)
    await msg.answer(text="<b>Введите мощность машины!</b>", reply_markup=admin_keyboard.back_admin)
    await state.set_state(AdminState.engine_power)


@router.message(AdminState.engine_power)
async def category_state(msg: types.Message, state: FSMContext):
    engine_power = msg.text

    try:
        engine_power_float = float(engine_power)
        if engine_power_float <= 0:
            raise ValueError("Мощность двигателя должна быть положительным числом.")
    except ValueError:
        await msg.answer(text="Ошибка! Введите положительное число для мощности двигателя.")
        return

    await state.update_data(engine_power=engine_power)
    data = await state.get_data()
    unique_code = str(uuid.uuid4())[:8]
    await state.update_data(unique_code=unique_code)
    img_base_path = "img/"
    img_file_name = data['img']
    img_path = os.path.join(img_base_path, img_file_name + ".jpg")
    db.fill_auto_table(unique_code, data['name_auto'], data['price'], data['description'], img_path, data['kolvo'],
                       data['engine_power'])
    category_select = db.select_category()
    categories_text = "\n\n".join(
        f"<b>ID:</b> {category[0]}\n<b>Имя категории:</b> {category[1]}" for category in category_select)
    await msg.answer(text="<u>Ниже представлены все доступные категории</u>")
    await msg.answer(text=f"{categories_text}\n\nНапишите <b>ID</b> категории")
    await state.set_state(AdminState.id_category)


@router.message(AdminState.id_category)
async def category_state(msg: types.Message, state: FSMContext):
    id_category = msg.text
    if not id_category.isdigit():
        await msg.answer(text="Ошибка! Введите число для категории.")
        return
    data = await state.get_data()
    auto_id = db.select_auto_code(data['unique_code'])
    number = auto_id[0][0]
    db.insert_auto_category_table(number, id_category)
    await state.clear()
    await msg.answer(text="Машина успешно добавлена!")


@router.callback_query(F.data == "get_auto")
async def get_categories(callback: types.CallbackQuery):
    auto_category_data = db.select_all_auto_category_data()
    message_text = "<b>Данные о машинах и их категориях:</b>\n"
    for row in auto_category_data:
        name_auto, name_kategory = row
        message_text += f"<b>Название машины:</b> {name_auto}\n<b>Категория:</b> {name_kategory}\n\n"

    await callback.message.answer(text=message_text)


@router.callback_query(F.data == "zayvka")
async def get_categories(callback: types.CallbackQuery):
    orders_data = db.select_all_orders_with_details()
    message_text = "<b>Данные о заявках:</b>\n"
    for row in orders_data:
        order_id, username, name_auto, price, description, img, kolvo, engine_power, status = row
        message_text += (
            f"<b>ID заявки:</b> {order_id}\n"
            f"<b>Пользователь:</b> {username}\n"
            f"<b>Название машины:</b> {name_auto}\n"
            f"<b>Цена:</b> {price}\n"
            f"<b>Описание:</b> {description}\n"
            f"<b>Изображение:</b> {img}\n"
            f"<b>Количество:</b> {kolvo}\n"
            f"<b>Мощность двигателя:</b> {engine_power}\n"
            f"<b>Статус:</b> {status}\n\n"
        )

    await callback.message.answer(text=message_text)


@router.message(Command("good_status"))
async def update_status_command(message: types.Message):
    if str(message.from_user.id) == ADMIN_IDS:
        text = message.text
        args = text.split()[1:]
        order_id = args[0]
        status = "Одобрено ✔️"
        if order_id:
            db.update_order_status(order_id, status)
            await message.answer(f"<b>ID заказа:</b> {order_id}\n<b>Статус:</b> {status}.")
        else:
            await message.answer("Пользователь с таким именем не найден.")
    else:
        await message.answer("У вас нет прав на выполнение этой команды.")


@router.message(Command("block"))
async def update_status_command(message: types.Message):
    if str(message.from_user.id) == ADMIN_IDS:
        text = message.text
        args = text.split()[1:]
        order_id = args[0]
        status = "Не одобрено ⛔️"
        if order_id:
            db.update_order_status(order_id, status)
            await message.answer(f"<b>ID заказа:</b> {order_id}\n<b>Статус:</b> {status}.")
        else:
            await message.answer("Пользователь с таким именем не найден.")
    else:
        await message.answer("У вас нет прав на выполнение этой команды.")
