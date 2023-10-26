
import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from telegram import Update
    from telegram.ext import CallbackContext


LOG = logging.getLogger(__name__)


async def action(update: "Update", context: "CallbackContext") -> None:
    """Handle x.com and twitter.com link"""
    LOG.debug('Handle x.com and twitter.com link')

    if not update or not update.message or not isinstance(update.message.text, str):
        return
    if not update.effective_chat:
        return

    if "https://twitter.com/" in update.message.text:
        vx_message = update.message.text.replace("https://twitter.com/", "https://vxtwitter.com/")
    elif "https://x.com/" in update.message.text:
        vx_message = update.message.text.replace("https://x.com/", "https://vxtwitter.com/")

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=vx_message,
    )
