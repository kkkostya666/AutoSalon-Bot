from aiogram import Router
from aiogram import types
from aiogram.filters import CommandStart
from aiogram import F
from keyboards.get_start_keyboard import get_start_keyboard
from keyboards import msk
import text

router = Router()


@router.message(CommandStart())
async def start(message: types.Message):
    await message.answer(text.start_text,
                         reply_markup=await get_start_keyboard())


@router.callback_query(F.data == "MSK")
async def start_msk(callback: types.CallbackQuery):
    await callback.message.answer(text.msk, reply_markup=msk.main_msk)


@router.callback_query(F.data == "kazan")
async def start_kzn(callback: types.CallbackQuery):
    await callback.message.answer(text.kazan, reply_markup=msk.main_msk)