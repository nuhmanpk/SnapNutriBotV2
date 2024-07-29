"""
==========================================
 Title:        Pyrogram Bot Template
 Description:  Template for creating a Pyrogram bot.
 Author:       Nuhman (https://github.com/nuhmanpk)
 Created:      22-Jun-2024
 License:      MIT License
==========================================
"""

from decouple import config
from hydrogram import Client

from bot.scheduler import start_scheduler

BOT_TOKEN = config('BOT_TOKEN')
API_ID = config('API_ID', cast=int)
API_HASH = config('API_HASH')

Bot = Client(
    "SnapNutriV2 Bot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
    plugins=dict(root="bot"),
)

if __name__ == "__main__":
    start_scheduler(Bot)
    Bot.run(print('Bot is Cooking...'))
