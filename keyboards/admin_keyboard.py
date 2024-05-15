from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

main_admin = [
        [InlineKeyboardButton(text="🔎 Категории автомобилей", callback_data="kategory_admin")],
        [InlineKeyboardButton(text="📝 Автомобили", callback_data="katalog_admin")],
        [InlineKeyboardButton(text="💸 Добавить город", callback_data="drygoe_admin")],
        [InlineKeyboardButton(text="💸 Заявки", callback_data="zayvka")],
]
main_admin = InlineKeyboardMarkup(inline_keyboard=main_admin)


kategory_admin = [
        [InlineKeyboardButton(text="☑️ Добавить категорию", callback_data="add_category")],
        [InlineKeyboardButton(text="✖️ Удалить категорию", callback_data="delete_category")],
        [InlineKeyboardButton(text="🔎 Доступные категории", callback_data="get_category")],
        [InlineKeyboardButton(text="️✖️ Назад", callback_data="back_admin")]
]
kategory_admin = InlineKeyboardMarkup(inline_keyboard=kategory_admin)

katalog_admin = [
        [InlineKeyboardButton(text="☑️ Добавить авто", callback_data="add_car")],
        [InlineKeyboardButton(text="✖️ Удалить авто", callback_data="delete_car")],
]
katalog_admin = InlineKeyboardMarkup(inline_keyboard=katalog_admin)


back_admin = [
        [InlineKeyboardButton(text="✖️ Назад", callback_data="back_admin")],
]
back_admin = InlineKeyboardMarkup(inline_keyboard=back_admin)


auto_admin = [
        [InlineKeyboardButton(text="☑️ Добавить  автомобиль", callback_data="add_auto")],
        [InlineKeyboardButton(text="🔎 Актуальные автомобили", callback_data="get_auto")],
        [InlineKeyboardButton(text="️✖️ Назад", callback_data="back_admin")]
]
auto_admin = InlineKeyboardMarkup(inline_keyboard=auto_admin)

