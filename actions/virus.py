import logging

import requests
from lxml import html

LOG = logging.getLogger(__name__)

def action(bot, update):
    LOG.debug('Handle coronavirus update')

    api_url = "https://jhu-parser.herokuapp.com/"

    output = {}

    bot.send_message(
        chat_id=update.message.chat_id,
        text=f'_Не сдохли еще, педики?_',
        parse_mode='markdown'
    )
    try:
        data = requests.get(api_url).json()
        total_cases = {'c':data["total"]["confirmed"]["total"], 'd':data["total"]["dead"]["total"], 'r': data["total"]["recovered"]["total"]}
        total_cases_previous = {'c': data["total"]["confirmed"]["diff"], 'd':data["total"]["dead"]["diff"], 'r': data["total"]["recovered"]["diff"]}
        russia_cases = {'c':data["Russia"]["confirmed"]["total"], 'd':data["Russia"]["dead"]["total"], 'r': data["Russia"]["recovered"]["total"]}
        russia_cases_previous = {'c': data["Russia"]["confirmed"]["diff"], 'd':data["Russia"]["dead"]["diff"], 'r': data["Russia"]["recovered"]["diff"]}

        output['total'] = f'🤒\t{total_cases["c"]} (+{total_cases_previous["c"]})\n🙂\t{total_cases["r"]} (+{total_cases_previous["r"]})\n💀\t{total_cases["d"]} (+{total_cases_previous["d"]})'
        output['russia'] = f'🤒\t{russia_cases["c"]} (+{russia_cases_previous["c"]})\n🙂\t{russia_cases["r"]} (+{russia_cases_previous["r"]})\n💀\t{russia_cases["d"]} (+{russia_cases_previous["d"]})'
    except Exception as e:
        LOG.exception(e)

    bot.send_message(
        chat_id=update.message.chat_id,
        text=f'Всего:\n{output["total"]}\n\nРоссия:\n{output["russia"]}'
    )
