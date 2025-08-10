from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard():
    """Create main store keyboard"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="👚 Store", callback_data="store"),
            InlineKeyboardButton(text="🛒 My Cart", callback_data="cart")
        ],
        [
            InlineKeyboardButton(text="📞 Contact", callback_data="contact"),
            InlineKeyboardButton(text="📍 Location", callback_data="location")
        ],
        [
            InlineKeyboardButton(text="⏰ Hours", callback_data="hours")
        ]
    ])
    return keyboard

def get_back_keyboard():
    """Create back to main store keyboard"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Back to Main Store", callback_data="back")]
    ])
    return keyboard