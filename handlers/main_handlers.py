import re

from aiogram import Router
from aiogram import types
from aiogram.filters import CommandStart
from aiogram import F
from aiogram.fsm.context import FSMContext

from keyboards.get_start_keyboard import get_start_keyboard, get_order_keyboard
from keyboards import msk
import text
from bd import Db
router = Router()
db = Db()
current_index = 0


@router.callback_query(F.data == "katalog")
async def create_order(callback: types.CallbackQuery):
    global current_index
    results = db.select_all_auto_data()
    if results:
        result = results[current_index]
        formatted_text = f"📍 <b>Марка:</b> {result[2]}\n💰 <b>Цена:</b> {result[3]}\n\n{result[4]}\n<b>Доступных для заказа: {result[6]} штук</b>\n💪 <b>Мощность двигателя:</b> {result[7]}"
        await callback.message.answer(formatted_text, reply_markup=await get_order_keyboard())
    else:
        await callback.message.answer("Нет доступных данных о машинах")


@router.callback_query(F.data == "next")
async def create_order(callback: types.CallbackQuery):
    global current_index
    current_index += 1
    results = db.select_all_auto_data()
    if results and current_index < len(results):
        result = results[current_index]
        formatted_text = f"📍 <b>Марка:</b> {result[2]}\n💰 <b>Цена:</b> {result[3]}\n\n{result[4]}\n<b>Доступных для заказа: {result[6]} штук</b>\n💪 <b>Мощность двигателя:</b> {result[7]}"
        await callback.message.edit_text(formatted_text, reply_markup=await get_order_keyboard())
    else:
        current_index = 0
        results = db.select_all_auto_data()
        if results:
            result = results[current_index]
            formatted_text = f"📍 <b>Марка:</b> {result[2]}\n💰 <b>Цена:</b> {result[3]}\n\n{result[4]}\n<b>Доступных для заказа: {result[6]} штук</b>\n💪 <b>Мощность двигателя:</b> {result[7]}"
            await callback.message.edit_text(formatted_text, reply_markup=await get_order_keyboard())
        else:
            await callback.message.edit_text("No data available")


@router.callback_query(F.data == "create_order")
async def create_order(callback: types.CallbackQuery, state: FSMContext):
    message = callback.message.text
    address_pattern = re.compile(r"📍 Марка: (.+)")
    address_match = address_pattern.search(message)
    if address_match:
        full_address = address_match.group(1).strip()
        name_auto = db.select_id_by_name_auto(full_address)
        db.insert_order(1, name_auto, status="В рассмотрении")
        await callback.message.answer(text="Автомобиль успешно забронирован.\nОжидайте, когда Ваша заявка рассмотрится модераторами")
    else:
        print("Адрес не найден в сообщении.")


@router.callback_query(F.data == "find_auto")
async def create_order(callback: types.CallbackQuery, state: FSMContext):
    results = db.select_all_orders_with_details_user("kkkostya666")
    if results:
        message_text = ""
        for result in results:
            formatted_text = (
                f"📍 <b>Марка:</b> {result[2]}\n"
                f"💰 <b>Цена:</b> {result[3]}\n\n"
                f"{result[4]}\n"
                f"<b>Доступных для заказа: {result[6]} штук</b>\n"
                f"💪 <b>Мощность двигателя:</b> {result[7]}\n"
                f"<b>Статус:</b> {result[8]}\n\n"
            )
            message_text += formatted_text

        await callback.message.edit_text(message_text, reply_markup=msk.main_msk)
    else:
        await callback.message.answer("Нет данных")
