import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from telegram import Update
    from telegram.ext import CallbackContext


LOG = logging.getLogger(__name__)


async def action(update: "Update", context: "CallbackContext") -> None:
    """Handle instagram link"""
    LOG.debug("Handle instagram.com link")

    if not update or not update.message or not isinstance(update.message.text, str):
        return
    if not update.effective_chat:
        return

    if "https://www.instagram.com/" in update.message.text:
        vx_message = update.message.text.replace(
            "https://www.instagram.com/", "https://ddinstagram.com/"
        )
    elif "https://instagram.com/" in update.message.text:
        vx_message = update.message.text.replace(
            "https://instagram.com/", "https://ddinstagram.com/"
        )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=vx_message,
    )

