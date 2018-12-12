import logging

import requests
from lxml import html

LOG = logging.getLogger(__name__)


def action(bot, update):
    city = update.message.text.split()[1].strip()

    get_search_results = requests.get(
        'https://www.gismeteo.ru/api/v2/search/searchresultforsuggest/%s/?lang=ru&domain=ru' % city,
        headers={
            'Host': 'www.gismeteo.ru',
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/67.0.3396.87 Safari/537.36 OPR/54.0.2952.71"
        }
    )

    weather_url = get_search_results.json()['items'][0]['url']
    weather = html.fromstring(requests.get(
        'https://www.gismeteo.ru%s' % weather_url,
        headers={
            'Host': 'www.gismeteo.ru',
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/67.0.3396.87 Safari/537.36 OPR/54.0.2952.71"
        }
    ).text)

    times = weather.xpath(".//div[@data-widget-id='forecast']//span/text()")[:8]
    temperatures = list(map(int,
                            weather.xpath(".//div[@class='chart chart__temperature']//div[@class='value']/text()")))
    sun = weather.xpath(
        ".//div[@class='widget__row widget__row_table widget__row_icon']//span[@class='tooltip']/@data-text")
    rainfall = list(map(str.strip, weather.xpath(
        ".//div[@class='widget__row widget__row_table widget__row_']//div[contains(@class, "
        "'w_precipitation__value')]/text()")))
    winds = list(map(str.strip, weather.xpath(
        ".//div[@class='widget__row widget__row_table widget__row_wind-or-gust']//div[@class='w_wind']/*//text()")))
    dates = weather.xpath(".//div[@class='tabs _center']//div[@class='tab  tooltip']//div[contains(@class, 'date')]")

    if not rainfall:
        rainfall = [0, 0, 0, 0, 0, 0, 0, 0]

    data = []

    for i in range(0, len(times), 2):
        data += times[i:i + 2]
        data += temperatures[i:i + 2]
        data += sun[i:i + 2]
        data += rainfall[i:i + 2]
        data += winds[i:i + 2]

    print('data %s ' % len(data))
    print(data)

    message = """
    Погода в городе {} на {} ({})
    Ночь ({} - {}) - температура {}-{} {} -> {} (осадки {} - {} мм) ветер {} - {} м/с 
    Утро ({} - {}) - температура {}-{} {} -> {} (осадки {} - {} мм) ветер {} - {} м/с 
    День ({} - {}) - температура {}-{} {} -> {} (осадки {} - {} мм) ветер {} - {} м/с
    Вечер ({} - {}) - температура {}-{} {} -> {} (осадки {} - {} мм) ветер {} - {} м/с
    """.format(city, dates[1].text.strip(), dates[0].text.strip(), *data)

    bot.send_message(
        chat_id=update.message.chat_id,
        text=message
    )
