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
        total_cases = {'c':0, 'd':0, 'r': 0}
        total_cases_previous = {'c':0, 'd':0, 'r': 0}
        russia_cases = {}
        russia_cases_previous = {'c':0, 'd':0, 'r': 0}
        for region in data['regions']:
            try:
                total_cases['c'] += int(region['1'])
                total_cases['d'] += int(region['2'])
                total_cases['r'] += int(region['3'])
                total_cases_previous['c'] += int(region['4'])
                total_cases_previous['d'] += int(region['5'])
                total_cases_previous['r'] += int(region['6'])
            except TypeError:
                total_cases['c'] += int(region[1])
                total_cases['d'] += int(region[2])
                total_cases['r'] += int(region[3])  
                total_cases_previous['c'] += int(region[4])
                total_cases_previous['d'] += int(region[5])
                total_cases_previous['r'] += int(region[6])              
            finally:
                pass
            
            if type(region) == list and region[0]['en_name']=='Russia':
                try:
                    russia_cases['c'] = region['1']
                    russia_cases['d'] = region['2']
                    russia_cases['r'] = region['3']
                    russia_cases_previous['c'] = int(region['4'])
                    russia_cases_previous['d'] = int(region['5'])
                    russia_cases_previous['r'] = int(region['6'])
                except TypeError:
                    russia_cases['c'] = region[1]
                    russia_cases['d'] = region[2]
                    russia_cases['r'] = region[3]
                    russia_cases_previous['c'] = int(region[4])
                    russia_cases_previous['d'] = int(region[5])
                    russia_cases_previous['r'] = int(region[6])
                finally:
                    pass
        output['total'] = f'🤒\t{total_cases["c"]} (+{total_cases_previous["c"]})\n🙂\t{total_cases["r"]} (+{total_cases_previous["r"]})\n💀\t{total_cases["d"]} (+{total_cases_previous["d"]})'
        output['russia'] = f'🤒\t{russia_cases["c"]} (+{russia_cases_previous["c"]})\n🙂\t{russia_cases["r"]} (+{russia_cases_previous["r"]})\n💀\t{russia_cases["d"]} (+{russia_cases_previous["d"]})'
    except Exception as e:
        LOG.exception(e)

    bot.send_message(
        chat_id=update.message.chat_id,
        text=f'Всего:\n{output["total"]}\n\nРоссия:\n{output["russia"]}'
    )
