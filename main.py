from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType
from aiogram.utils import executor
import logging
import config

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer("Отправьте скриншот оплаты и ваш email. Пример:\n\nemail@example.com")

@dp.message_handler(content_types=ContentType.PHOTO)
async def handle_photo(message: types.Message):
    if not message.caption:
        await message.reply("Пожалуйста, отправьте email в подписи к скриншоту.")
        return
    await message.forward(config.ADMIN_ID)
    await message.reply("Спасибо! Мы проверим оплату и в течении 24 часов откроем доступ. Ссылка с логином и паролем придёт на указанную почту.")

@dp.message_handler(lambda msg: '@' in msg.text or '.' in msg.text)
async def handle_email(message: types.Message):
    await bot.send_message(config.ADMIN_ID, f"Email от пользователя @{message.from_user.username}: {message.text}")
    await message.reply("Теперь отправьте, пожалуйста, скриншот платежа.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
