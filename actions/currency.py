import logging

import requests
from lxml import html

LOG = logging.getLogger(__name__)


def action(bot, update):
    LOG.debug('Handle currency price request')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.1453.93 '
                      'Safari/537.36'
    }
    currencies = {
        'XBT': 'https://www.investing.com/crypto/bitcoin',
        'USD': 'https://www.investing.com/currencies/usd-rub',
        'EUR': 'https://www.investing.com/currencies/eur-rub',
        'OIL': 'http://www.investing.com/commodities/brent-oil'
    }

    output = {}

    bot.send_message(
        chat_id=update.message.chat_id,
        text=f'_Отправляю запрос к трейдерам..._',
        parse_mode='markdown'
    )

    for name in currencies:
        try:
            tree = html.fromstring(requests.get(currencies[name], headers=headers).content)
            value = float(tree.xpath("//*[@id='last_last']")[0].text.strip().replace(',', ''))
            output[name] = value
        except Exception as e:
            LOG.exception(e)

    bot.send_message(
        chat_id=update.message.chat_id,
        text=f'₿ {output["XBT"]}$  💵 {output["USD"]}₽  💶 {output["EUR"]}₽  🛢️ {output["OIL"]}$'
    )
