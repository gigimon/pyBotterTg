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
        'XBT': 'https://finance.yahoo.com/quote/BTC-USD?p=BTC-USD&.tsrc=fin-srch',
        'ETH': 'https://finance.yahoo.com/quote/ETH-USD?p=ETH-USD&.tsrc=fin-srch',
        'USD': 'https://finance.yahoo.com/quote/RUB=X?p=RUB=X&.tsrc=fin-srch',
        'EUR': 'https://finance.yahoo.com/quote/EURRUB=X?p=EURRUB=X&.tsrc=fin-srch',
        'OIL': 'https://finance.yahoo.com/quote/BZJ23.NYM?p=BZJ23.NYM',
        'GAS': 'https://finance.yahoo.com/quote/TTF=F?p=TTF=F&.tsrc=fin-srch'
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
            value = tree.xpath('//*[@data-test="qsp-price"]')[0].attrib["value"]
            output[name] = float(value)
        except Exception as e:
            LOG.exception(e)
    
    bot.send_message(
        chat_id=update.message.chat_id,
        text=f'₿ ${output["XBT"]}  ♦ ${output["ETH"]}  💵 {output["USD"]}₽  💶 {output["EUR"]}₽  🛢️ ${output["OIL"]}  ⛽️ €{round(float(output["GAS"]) * 10, 2)}'
    )
