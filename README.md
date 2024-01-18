# Description

Small telegram bot for #nnm irc channel which migrated to telegram #nnm chat

# Run using docker-compose

Copy config file from example:
`cp .bot.env.example .bot.env`

Edit .bot.env file and provide your Telegram API Token and Allowed chats list.

Run container:
`docker-compose up -d`

# Development

To generate the production requirements.txt file from pyproject.toml use pip-tools utility:

`pip-compile -o requirements.txt pyproject.toml`

To generate the development requirements-dev.txt file from pyproject.toml use pip-tools utility:

`pip-compile --extra dev -o requirements-dev.txt pyproject.toml`

To run the bot from console provide required environment variables (TELEGRAM_BOT_TOKEN, ALLOWED_CHATS) and run the python script:

`TELEGRAM_BOT_TOKEN=123456:AAAAA_BBBBB-CCCCC_DDDDDD ALLOWED_GROUPS=1234 python bot.py`
