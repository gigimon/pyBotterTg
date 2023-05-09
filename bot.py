import os
import sys
import logging

from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters

from actions import currency, log, quotes, google


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, os.environ.get('LOG_LEVEL', 'DEBUG'))
)

BOT_NAME = 'pyBotterBot'
BOT_API_KEY = os.environ.get('TG_API_KEY', None)

if BOT_API_KEY is None:
    print('API key not found. Use TG_API_KEY environment variable')
    sys.exit(1)


LOG = logging.getLogger(__name__)


def main() -> None:
    application = ApplicationBuilder().token(BOT_API_KEY).build()

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
        MessageHandler(filters=None, callback=log.action)
    )

    application.run_polling()


if __name__ == '__main__':
    main()
