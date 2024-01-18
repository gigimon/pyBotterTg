import logging
import random
import re
from pathlib import Path
from typing import TYPE_CHECKING

import aiofiles

if TYPE_CHECKING:
    from datetime import datetime

    from telegram import Update
    from telegram.ext import CallbackContext


LOG = logging.getLogger(__name__)


async def action(update: "Update", context: "CallbackContext") -> None:
    """A Quotes engine"""
    async def get_quotes(channel: str) -> list[str]:
        """Reads the quotes database file"""
        async with aiofiles.open(f'quotes/{channel}.txt') as quotes_file:
            quotes = await quotes_file.readlines()
        return quotes

    async def append_quote(channel: str, date: "datetime", author: str, msg: str) -> int:
        """Adds a quote to database"""
        async with aiofiles.open(f'quotes/{channel}.txt', 'a+') as quotes_file:
            count = len(await get_quotes(channel)) + 1
            await quotes_file.write(
                f'{count} {date.strftime("%m/%d/%Y %H:%M:%S")} {channel} {author} {msg}\n'
            )
        return count

    async def get_quote(channel: str, msg_id: int | None = None) -> str:
        """Receives a quote from database"""
        quotes = await get_quotes(channel)
        if msg_id is None:
            msg_id = random.randint(0, len(quotes))  # noqa: S311
        if msg_id > len(quotes) - 1:
            msg_id = len(quotes)
        if quotes:
            return quotes[msg_id - 1]
        return ""

    def format_msg(quote: str) -> str:
        """Formats a quote to a chat message"""
        if quote == "":
            reply_msg = "Ничего нет"
        elif not quote.startswith('-deleted-'):
            quote_id, date, time, _, author, quote_msg = quote.split(' ', 5)
            reply_msg = f'[{quote_id}] -> [{date} {time}] {author}: {quote_msg}'
        else:
            reply_msg = f'Эта цитата была удалена вот этим пидором {quote.split(" ", 2)[1]}'
        return reply_msg

    if not update or not update.message or not isinstance(update.message.text, str):
        return
    if not update.effective_chat:
        return

    channel_name = update.effective_chat.title or str(update.effective_chat.id)
    quotes_file_path = Path(f'quotes/{channel_name}.txt')
    if not quotes_file_path.is_file():
        # Create a new file if not exists
        async with aiofiles.open(quotes_file_path, "a+"):
            pass

    msg = re.sub(r'\s+', ' ', update.message.text).strip()
    action, quote_number = re.findall('^!(q|rq|fq|aq)(?: )?(.+)?', msg)[0]
    if quote_number.isdigit():
        quote_number = int(quote_number)

    if action == 'q':
        if not quote_number:
            reply_msg = 'Ты должен ввести номер цитаты!'
        else:
            reply_msg = format_msg(await get_quote(channel_name, quote_number))
    elif action == 'rq':
        quote_number = None
        reply_msg = format_msg(await get_quote(channel_name, quote_number))
    elif action == 'fq':
        found_quotes = []
        for quote in await get_quotes(channel_name):
            if str(quote_number) in quote:
                found_quotes.append(quote)
        last_quoted = '\n'.join(map(format_msg, found_quotes[-5:]))
        found_quotes_len = len(found_quotes)
        if not found_quotes_len:
            reply_msg = "Нет таких цитат"
        else:
            reply_msg = (
                f"Мы нашли {found_quotes_len} результатов: "
                f"{'|'.join(a.split()[0] for a in found_quotes)}\n"
                f"Вот последние: \n{last_quoted}")
    elif action == 'aq':
        if isinstance(quote_number, int | float) or len(quote_number) < 10 or len(quote_number.split()) < 3:
            reply_msg = 'Цитата должна быть больше 10 букв или 3-х слов'
        else:
            msg_date = update.message.date
            if update.message.from_user and update.message.from_user.username:
                author = update.message.from_user.username
            else:
                author = "Мутный юзер"
            new_count = await append_quote(channel_name, msg_date, author, quote_number)
            reply_msg = f'Цитата добавлена под номером {new_count}'
    else:
        reply_msg = 'Упс, что-то пошло не так'

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply_msg
    )
