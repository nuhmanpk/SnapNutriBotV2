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

BOT_TOKEN = config('BOT_TOKEN')
API_ID = config('API_ID', cast=int)
API_HASH = config('API_HASH')
SESSION_STRING = config('SESSION_STRING')

# async def main():
#     async with Client(":memory:", api_id=int(API_ID), api_hash=API_HASH) as app:
#         # Generate the session string
#         session_string = await app.export_session_string()
#         print("Your session string is:", session_string)

# import asyncio
# asyncio.run(main())

Bot = Client(
    "Crypto Bot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
    plugins=dict(root="bot"),
    in_memory=True,
    session_string=SESSION_STRING
)


Bot.run(print('Bot is Cooking...'))
