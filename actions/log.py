import pathlib
import logging

LOG = logging.getLogger(__name__)

LOG_PATH = pathlib.Path('./logs').expanduser()


async def action(update, context) -> None:
    """Saving message to log"""
    LOG.debug('Saving message to log')

    if update.effective_chat.id is None:
        return

    chat_name = update.effective_chat.title or str(update.effective_chat.id)
    username = update.message.from_user.first_name
    date = update.message.date

    log_dir = LOG_PATH / chat_name / str(date.year) / str(date.month) / str(date.day)

    if not log_dir.is_dir():
        log_dir.mkdir(parents=True)

    log_path = log_dir / 'logs.log'

    with open(log_path, 'a') as log_file:
        log_file.write('[%s] [%s] %s\n' % (date.strftime('%H:%M:%S'), username, update.message.text))
