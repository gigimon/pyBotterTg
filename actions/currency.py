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
        'ETH': 'https://www.investing.com/crypto/ethereum',
        'USD': 'https://www.investing.com/currencies/usd-rub',
        'EUR': 'https://www.investing.com/currencies/eur-rub',
        'OIL': 'https://www.investing.com/commodities/brent-oil'
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
            elem_last_last = tree.xpath("//*[@id='last_last']")
            elem_data_test = tree.xpath("//*[@data-test='instrument-price-last']")
            if len(elem_last_last)>0:
                output[name]=float(elem_last_last[0].text.strip().replace(',', ''))
            elif len(elem_data_test)>0:
                output[name] = float(elem_data_test[0].text.strip().replace(',', ''))
        except Exception as e:
            LOG.exception(e)

    bot.send_message(
        chat_id=update.message.chat_id,
        text=f'₿ {output["XBT"]}$  ♦ {output["ETH"]}$  💵 {output["USD"]}₽  💶 {output["EUR"]}₽  🛢️ {output["OIL"]}$'
    )
