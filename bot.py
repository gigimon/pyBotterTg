import os
import sys
import logging

from telegram.ext import Updater, MessageHandler, CommandHandler, Filters

from actions import currency, log, quotes, google, virus


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


def main():
    updater = Updater(token=BOT_API_KEY)
    updater.dispatcher.add_handler(
        CommandHandler(command='pizdec', callback=currency.action)
    )

    updater.dispatcher.add_handler(
        MessageHandler(filters=[Filters.regex('^!(g|гугл)')], callback=google.action)
    )

    updater.dispatcher.add_handler(
        MessageHandler(filters=[Filters.regex('^!пиздец')], callback=currency.action)
    )

    updater.dispatcher.add_handler(
        MessageHandler(filters=[Filters.regex('^!корона')], callback=virus.action)
    )

    updater.dispatcher.add_handler(
        MessageHandler(filters=[Filters.regex('^!(q|rq|fq|aq)')], callback=quotes.action)
    )

    # updater.dispatcher.add_handler(
    #     CommandHandler(command='weather', callback=weather)
    # )

    updater.dispatcher.add_handler(
        MessageHandler(filters=None, callback=log.action)
    )

    updater.start_polling()


if __name__ == '__main__':
    main()
