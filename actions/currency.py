
import asyncio
import logging
from collections.abc import Callable
from typing import TYPE_CHECKING

import aiohttp
from lxml import html
from typing_extensions import TypedDict

if TYPE_CHECKING:
    from telegram import Update
    from telegram.ext import CallbackContext


LOG = logging.getLogger(__name__)

class CurrencyBase(TypedDict):
    """A Currency data base dict"""
    url: str
    format: str

class Currency(CurrencyBase, total=False):
    """A Currency data dict with optional preparing function"""
    preparing_fn: Callable[[int | float], int | float]


def round_fn(value: int | float) -> int | float:
    """Rounds numeric value to 2 places"""
    result = round(float(value) * 10, 2)
    return result


async def fetch_data(currencies: dict[str, Currency], headers: dict) -> dict[str, str]:
    """Fetchnig data from sources"""
    async with aiohttp.ClientSession() as session:
        tasks = []
        for symbol in currencies:
            tasks.append(
                asyncio.create_task(
                    session.get(
                        currencies[symbol]["url"],
                        headers=headers
                    )
                )
            )
        completed_responses = await asyncio.gather(*tasks)
        results = [await r.text() for r in completed_responses]
    return dict(zip(currencies.keys(), results, strict=False))


async def action(update: "Update", context: "CallbackContext") -> None:
    """Handle currency price request"""
    LOG.debug('Handle currency price request')

    if not update or not update.message or not isinstance(update.message.text, str):
        return
    if not update.effective_chat:
        return

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.1453.93 '
                      'Safari/537.36'
    }
    currencies = {
        'XBT': Currency(
            url='https://finance.yahoo.com/quote/BTC-USD?p=BTC-USD&.tsrc=fin-srch',
            format='₿ ${}',
            preparing_fn=round_fn,
        ),
        'ETH': Currency(
            url='https://finance.yahoo.com/quote/ETH-USD?p=ETH-USD&.tsrc=fin-srch',
            format='♦ ${}',
            preparing_fn=round_fn,
        ),
        'USD': Currency(
            url='https://finance.yahoo.com/quote/RUB=X?p=RUB=X&.tsrc=fin-srch',
            format='💵 {}₽',
        ),
        'EUR': Currency(
            url='https://finance.yahoo.com/quote/EURRUB=X?p=EURRUB=X&.tsrc=fin-srch',
            format='💶 {}₽',
        ),
        'OIL': Currency(
            url='https://finance.yahoo.com/quote/BZM23.NYM?p=BZM23.NYM',
            format='🛢️ ${}',
        ),
        'GAS': Currency(
            url='https://finance.yahoo.com/quote/TTF=F?p=TTF=F&.tsrc=fin-srch',
            format='⛽️ €{}',
            preparing_fn=round_fn,
        ),
    }

    output = {}

    response = await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='_Отправляю запрос к трейдерам..._',
        parse_mode='markdown'
    )
    # Get initial message ID for the further editing
    pre_message_id = response.message_id

    results = await fetch_data(currencies=currencies, headers=headers)

    for symbol, data in results.items():
        try:
            tree = html.fromstring(data)
            xpath_result = tree.xpath('//*[@data-test="qsp-price"]')

            # Checks required by mypy
            if not xpath_result:
                msg = f"{symbol}: xpath returned no data"
                raise ValueError(msg)

            if isinstance(xpath_result, list | tuple):
                item = xpath_result[0]
            else:
                msg = f"{symbol}: xpath returned non iterable data"
                raise ValueError(msg)

            if not hasattr(item, "attrib"):
                msg = f"{symbol}: xpath item has no 'attrib'"
                raise ValueError(msg)
            attrib = item.attrib  # type: ignore

            if not hasattr(attrib, "get"):
                msg = f"{symbol}: xpath item attrib item has no 'get'"
                raise ValueError(msg)
            value = attrib.get(
                "value", ""
            )

            if not value:
                msg = f"{symbol}: xpath item has no value"
                raise ValueError(msg)

            if "preparing_fn" in currencies[symbol]:
                if isinstance(value, str):
                    try:
                        value = float(value)
                    except ValueError as err:
                        msg = f"{symbol}: value error {value}"
                        raise ValueError(msg) from err
                if not isinstance(value, int | float):
                    msg = f"{symbol}: value error {value}"
                    raise ValueError(msg)

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
