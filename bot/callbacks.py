from .database import db
from .admin import add_user
from pyromod import Client
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup
from .commands import start, help, about


@Client.on_callback_query()
async def cb_data(_, message):
    await add_user(message.from_user.id)
    if message.data == "home":
        await start(_, message, cb=True)
    elif message.data == "help":
        await help(_, message, cb=True)
    elif message.data == "about":
        await about(_, message, cb=True)
    elif message.data == "close":
        await message.message.delete()


@Client.on_callback_query(filters.regex("gender_"))
async def gender_callback(bot, query):
    message = query.message.message
    gender = query.data.split("_")[1]
    await db.update_user(message.from_user.id, {"gender": gender})
    await query.message.edit_text(f"Gender updated to {gender.capitalize()}")
