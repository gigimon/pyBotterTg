import re
import random
import logging
from pathlib import Path
LOG = logging.getLogger(__name__)


async def action(update, context) -> None:
    """A Quotes engine"""
    def get_quotes(channel):
        with open(f'quotes/{channel}.txt', 'r') as quotes_file:
            quotes = quotes_file.readlines()
        return quotes

    def append_quote(channel, date, author, msg):
        with open(f'quotes/{channel}.txt', 'a+') as quotes_file:
            count = len(get_quotes(channel)) + 1
            quotes_file.write(
                f'{count} {date.strftime("%m/%d/%Y %H:%M:%S")} {channel} {author} {msg}\n'
            )
        return count

    def get_quote(channel, msg_id=None):
        quotes = get_quotes(channel)
        if msg_id is None:
            msg_id = random.randint(0, len(quotes))
        if msg_id > len(quotes) - 1:
            msg_id = len(quotes)
        return quotes[msg_id - 1]

    def format_msg(quote):
        if not quote.startswith('-deleted-'):
            quote_id, date, time, _, author, quote_msg = quote.split(' ', 5)
            reply_msg = f'[{quote_id}] -> [{date} {time}] {author}: {quote_msg}'
        else:
            reply_msg = f'Эта цитата была удалена вот этим пидором {quote.split(" ", 2)[1]}'
        return reply_msg

    channel_name = update.effective_chat.title or str(update.effective_chat.id)
    quotes_file_path = Path(f'quotes/{channel_name}.txt')
    if not quotes_file_path.is_file():
        # Create a new file if not exists
        with open(quotes_file_path, "a+") as f:
            pass
    
    msg = re.sub('\s+', ' ', update.message.text).strip()
    action, quote_number = re.findall('^!(q|rq|fq|aq)(?: )?(.+)?', msg)[0]
    if quote_number.isdigit():
        quote_number = int(quote_number)

    if action == 'q':
        if not quote_number:
            reply_msg = 'Ты должен ввести номер цитаты!'
        else:
            reply_msg = format_msg(get_quote(channel_name, quote_number))
    elif action == 'rq':
        quote_number = None
        reply_msg = format_msg(get_quote(channel_name, quote_number))
    elif action == 'fq':
        found_quotes = []
        for quote in get_quotes(channel_name):
            if str(quote_number) in quote:
                found_quotes.append(quote)
        last_quoted = '\n'.join(map(format_msg, found_quotes[-5:]))
        found_quotes_len = len(found_quotes)
        if not found_quotes_len:
            reply_msg = f"Нет таких цитат"
        else:
            reply_msg = f"Мы нашли {found_quotes_len} результатов: {'|'.join(a.split()[0] for a in found_quotes)}\n"\
                f"Вот последние: \n{last_quoted}"
    elif action == 'aq':
        if len(quote_number) < 10 or len(quote_number.split()) < 3:
            reply_msg = 'Цитата должна быть больше 10 букв или 3-х слов'
        else:
            msg_date = update.message.date
            author = update.message.from_user.username
            new_count = append_quote(channel_name, msg_date, author, quote_number)
            reply_msg = f'Цитата добавлена под номером {new_count}'
    else:
        reply_msg = 'Упс, что-то пошло не так'

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply_msg
    )
