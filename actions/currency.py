
import aiohttp
import logging
import asyncio

from lxml import html

LOG = logging.getLogger(__name__)


async def fetch_data(currencies: dict[str, str], headers: dict) -> dict[str, str]:
    """Fetchnig data from sources"""
    async with aiohttp.ClientSession() as session:
        tasks = []
        for symbol in currencies:
            tasks.append(asyncio.create_task(session.get(currencies[symbol]["url"], headers=headers)))
        completed_responses = await asyncio.gather(*tasks)
        results = [await r.text() for r in completed_responses]
    return dict(zip(currencies.keys(), results))


async def action(update, context) -> None:
    """Handle currency price request"""
    LOG.debug('Handle currency price request')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.1453.93 '
                      'Safari/537.36'
    }
    currencies = {
        'XBT': {
            'url': 'https://finance.yahoo.com/quote/BTC-USD?p=BTC-USD&.tsrc=fin-srch',
            'format': '₿ ${}',
        },
        'ETH': {
            'url': 'https://finance.yahoo.com/quote/ETH-USD?p=ETH-USD&.tsrc=fin-srch',
            'format': '♦ ${}',
        },
        'USD': {
            'url': 'https://finance.yahoo.com/quote/RUB=X?p=RUB=X&.tsrc=fin-srch',
            'format': '💵 {}₽',
        },
        'EUR': {
            'url': 'https://finance.yahoo.com/quote/EURRUB=X?p=EURRUB=X&.tsrc=fin-srch',
            'format': '💶 {}₽',
        },
        'OIL': {
            'url': 'https://finance.yahoo.com/quote/BZM23.NYM?p=BZM23.NYM',
            'format': '🛢️ ${}',
        },
        'GAS': {
            'url': 'https://finance.yahoo.com/quote/TTF=F?p=TTF=F&.tsrc=fin-srch',
            'format': '⛽️ €{}',
            'preparing_fn': lambda x: round(float(x) * 10, 2),
        },
    }

    output = {}

    response = await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'_Отправляю запрос к трейдерам..._',
        parse_mode='markdown'
    )
    # Get initial message ID for the further editing
    pre_message_id = response.message_id

    results = await fetch_data(currencies=currencies, headers=headers)

    for symbol, data in results.items():
        try:
            tree = html.fromstring(data)
            value = tree.xpath('//*[@data-test="qsp-price"]')[0].attrib["value"]
            if "preparing_fn" in currencies[symbol]:
                value = currencies[symbol]["preparing_fn"](value)
            output[symbol] = currencies[symbol]["format"].format(value)
        except Exception as e:
            LOG.exception(e)
            output[symbol] = currencies[symbol]["format"].format('n/a')
    
    text = "  ".join([data for symbol, data in output.items()])

    # Update the initial message with fetched data
    await context.bot.edit_message_text(
        message_id=pre_message_id,
        chat_id=update.effective_chat.id,
        text=text
    )
