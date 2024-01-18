import logging
import pathlib
from typing import TYPE_CHECKING

import aiofiles

if TYPE_CHECKING:
    from telegram import Update
    from telegram.ext import CallbackContext

LOG = logging.getLogger(__name__)

LOG_PATH = pathlib.Path('./logs').expanduser()


async def action(update: "Update", context: "CallbackContext") -> None:
    """Saving message to log"""
    LOG.debug('Saving message to log')

    if not update or not update.message or not isinstance(update.message.text, str):
        return
    if not update.effective_chat:
        return

    chat_name = update.effective_chat.title or str(update.effective_chat.id)
    if update.message.from_user:
        username = update.message.from_user.first_name or \
            update.message.from_user.username or str(update.message.from_user.id)
    else:
        username = f"Unkown user from chat {update.effective_chat}"

    date = update.message.date

    log_dir = LOG_PATH / chat_name / str(date.year) / str(date.month) / str(date.day)

    if not log_dir.is_dir():
        log_dir.mkdir(parents=True)

    log_path = log_dir / 'logs.log'

    async with aiofiles.open(log_path, 'a') as log_file:
        await log_file.write(
            '[{}] [{}] {}\n'.format(
                date.strftime('%H:%M:%S'), username, update.message.text
            )
        )
