from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import logging
import config  # Убедись, что в config.py есть BOT_TOKEN и ADMIN_ID

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)

# Клавиатура с кнопками оплаты
def get_payment_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("💵 Оплата на месяц", url="https://yoomoney.ru/bill/pay/1A49E9QJCKQ.250508"),
        InlineKeyboardButton("💳 Оплата на год", url="https://yoomoney.ru/bill/pay/1A49ENDESHP.250508"),
    )
    return keyboard

# Команда /start
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer(
        "👋 Привет! Добро пожаловать в Кулинарные Практики.\n\n"
        "1️⃣ Выберите способ оплаты ниже.\n"
        "2️⃣ После оплаты пришлите скриншот и ваш email.\n\n"
        "📧 Пример: email@example.com",
        reply_markup=get_payment_keyboard()
    )

# Обработка email
@dp.message_handler(lambda msg: '@' in msg.text or '.' in msg.text)
async def handle_email(message: types.Message):
    await bot.send_message(
        config.ADMIN_ID,
        f"📩 Email от пользователя @{message.from_user.username}:\n{message.text}"
    )
    await message.reply("✅ Email получен. Теперь отправьте, пожалуйста, скриншот платежа.")

# Обработка скрина
@dp.message_handler(content_types=ContentType.PHOTO)
async def handle_photo(message: types.Message):
    if not message.caption:
        await message.reply("⚠️ Пожалуйста, отправьте email в подписи к скриншоту.")
        return
    await message.forward(config.ADMIN_ID)
    await message.reply(
        "📷 Спасибо! Мы проверим оплату и в течение 24 часов откроем доступ.\n"
        "Ссылка с логином и паролем придёт на указанную почту."
    )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
