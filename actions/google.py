import re
import logging

import requests
from lxml import html as lhtml

LOG = logging.getLogger(__name__)


def action(bot, update):
    msg = re.sub('\s+', ' ', update.message.text).strip()
    query = msg.split(' ', 1)
    if len(query) > 1:
        query = query[1]
    else:
        bot.send_message(
            chat_id=update.message.chat_id,
            text='Нужен текст для запроса!'
        )
        return
    resp = requests.get(f'https://www.google.ru/search?client=opera&q={query}&sourceid=opera&ie=UTF-8&oe=UTF-8',
                        headers={
                            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, "
                                          "like Gecko) "
                                          "Chrome/67.0.3396.87 Safari/537.36 OPR/54.0.2952.71"})
    if not resp.status_code == 200:
        bot.send_message(
            chat_id=update.message.chat_id,
            text='Что-то пошло не так :('
        )
    else:
        tree = lhtml.fromstring(resp.content)
        record = tree.xpath('//div[@class="g"]')[0]
        url = record.xpath('.//a')[0]
        description = ' '.join(record.xpath('.//span[@class="st"]/text()'))
        count_result = ''.join(re.findall('(\d+)', tree.xpath('//div[@id="resultStats"]/text()')[0]))
        bot.send_message(
            chat_id=update.message.chat_id,
            text=f'Найдено примерно {count_result} результатов\n'
                 f'[{url.xpath(".//h3/text()")[0]}]({url.attrib["href"]})\n'
                 f'{description}\n',
            parse_mode='markdown'
        )
