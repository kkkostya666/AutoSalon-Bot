from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

main_msk = [
        [InlineKeyboardButton(text="🔎 Мои заявки", callback_data="find_auto")],
        [InlineKeyboardButton(text="📝 Актуальный каталог", callback_data="katalog")],
        [InlineKeyboardButton(text="💸 Сменить город", callback_data="drygoe")],
]
main_msk = InlineKeyboardMarkup(inline_keyboard=main_msk)