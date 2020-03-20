import logging

import requests
from lxml import html

LOG = logging.getLogger(__name__)

def diff(current,previous):
    if current>previous:
        return f'+{current-previous}'
    return '0'


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
        total_cases = data['timeline']['global'][-1]
        total_cases_previous = data['timeline']['global'][-2]
        russia_cases = {}
        russia_cases_previous = {}
        for region in data['regions']:
            if region[0]['en_name']=='Russia':
                russia_cases['c'] = region[1]
                russia_cases['d'] = region[2]
                russia_cases['r'] = region[3]
                russia_cases_previous = region[4][-2]
                break
        output['total'] = f'🤒\t{total_cases["c"]} ({diff(total_cases["c"], total_cases_previous["c"])})\n🙂\t{total_cases["r"]} ({diff(total_cases["r"], total_cases_previous["r"])})\n💀\t{total_cases["d"]} ({diff(total_cases["d"], total_cases_previous["d"])})'
        output['russia'] = f'🤒\t{russia_cases["c"]} ({diff(russia_cases["c"], russia_cases_previous["c"])})\n🙂\t{russia_cases["r"]} ({diff(russia_cases["r"], russia_cases_previous["r"])})\n💀\t{russia_cases["d"]} ({diff(russia_cases["d"], russia_cases_previous["d"])})'
    except Exception as e:
        LOG.exception(e)

    bot.send_message(
        chat_id=update.message.chat_id,
        text=f'Всего:\n{output["total"]}\n\nРоссия:\n{output["russia"]}'
    )
