
from os import environ
if not environ.get("BOT_TOKEN"):
    from dotenv import load_dotenv
    load_dotenv()
from telegram.ext import ApplicationBuilder

from telegram_ecommerce.utils.consts import bot_token 
from telegram_ecommerce.utils.log import logger
from telegram_ecommerce.handlers import (
    all_public_commands_descriptions, 
    all_handlers)
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from telegram_ecommerce.tamplates.buy_callbacks import handle_payment_method_callback

async def post_init(app):
    await app.bot.set_my_commands(all_public_commands_descriptions)

def main():
    app = ApplicationBuilder().token(bot_token).post_init(post_init).build()

    for handler in all_handlers:
        app.add_handler(handler)

    app.add_handler(CallbackQueryHandler(handle_payment_method_callback))




    logger.info("bot started")
    app.run_polling()
    logger.info("bot closed")


if __name__ == "__main__":
    main()


