import logging

import requests
from lxml import html

LOG = logging.getLogger(__name__)


def action(bot, update):
    LOG.debug('Handle coronavirus update')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.1453.93 '
                      'Safari/537.36'
    }
    api_url = "https://covid19info.live/processeddata.js"

    output = {}

    bot.send_message(
        chat_id=update.message.chat_id,
        text=f'_Не сдохли еще, педики?_',
        parse_mode='markdown'
    )
    try:
        data = requests.get(api_url, headers=headers).json()
        global_cases = data['timeline']['global'][-1]
        russia_cases = {}
        for region in data['regions']:
            if region[0]['en_name']=='Russia':
                russia_cases['c'] = region[1]
                russia_cases['d'] = region[2]
                russia_cases['r'] = region[3]
        output['global'] = f'🤒 {global_cases["c"]} 🙂 {global_cases["r"]} 💀 {global_cases["d"]}'
        output['russia'] = f'🤒 {russia_cases["c"]} 🙂 {russia_cases["r"]} 💀 {russia_cases["d"]}'
    except Exception as e:
        LOG.exception(e)

    bot.send_message(
        chat_id=update.message.chat_id,
        text=f'Мир:    {output["global"]}\nРоссия: {output["russia"]}'
    )
