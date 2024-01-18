import logging
import os
import sys

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from actions import currency, instagram, log, quotes, xcom

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, os.environ.get('LOG_LEVEL', 'DEBUG'))
)

BOT_NAME = 'pyBotterBot'
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', "")
ALLOWED_CHATS = os.environ.get("ALLOWED_CHATS", "")


if not TELEGRAM_BOT_TOKEN:
    print('API key not found. Use TELEGRAM_BOT_TOKEN environment variable')
    sys.exit(1)


LOG = logging.getLogger(__name__)


def main() -> None:

    allowed_chats_list = None

    if len(ALLOWED_CHATS):
        allowed_chats_list = [int(x) for x in ALLOWED_CHATS.split(",")]

    print("Use filters.Chat(allowed_chats_list) with handlers to control chats access")

    if allowed_chats_list:
        print(f"Allowed chats are: {allowed_chats_list}")
    else:
        print("This bot is public and could be used in any chat")

    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(
        CommandHandler(command='pizdec', callback=currency.action)
    )

    application.add_handler(
        MessageHandler(filters=filters.Regex('^!пиздец'), callback=currency.action)
    )

    application.add_handler(
        MessageHandler(filters=filters.Regex('^!(q|rq|fq|aq)'), callback=quotes.action)
    )
    # application.add_handler(
    #     MessageHandler(filters=filters.regex('^!(g|гугл)'), callback=google.action)
    # )

    # application.add_handler(
    #     CommandHandler(command='weather', callback=weather)
    # )

    application.add_handler(
        MessageHandler(
            filters.Regex(r"^(https\:\/\/twitter\.com\/|https\:\/\/x\.com\/)"),
            callback=xcom.action,
        )
    )

    application.add_handler(
        MessageHandler(
            filters.Regex(
                r"^(https\:\/\/instagram\.com\/|https\:\/\/www\.instagram\.com\/)"
            ),
            callback=instagram.action,
        )
    )

    application.add_handler(
        MessageHandler(filters=filters.BaseFilter(), callback=log.action)
    )

    application.run_polling()


if __name__ == '__main__':
    main()
