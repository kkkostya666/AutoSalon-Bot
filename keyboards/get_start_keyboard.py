from aiogram import types


async def get_start_keyboard():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[[
            types.InlineKeyboardButton(
                text="Казань",
                callback_data="kazan"
            ),
        ]]
    )


async def get_order_keyboard():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[[
            types.InlineKeyboardButton(
                text="Забронировать ✔️",
                callback_data="create_order"
            ),
            types.InlineKeyboardButton(
                text="Следующая ➡️",
                callback_data="next"
            ),
        ]]
    )
