import PIL
from .database import db
from .admin import add_user
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from .buttons import HELP_BUTTONS, START_BUTTONS, ABOUT_BUTTONS, CLOSE_BUTTON
from .constants import START_TEXT, HELP_TEXT, ABOUT_TEXT
from .prompts import PROMPT
from .gemini import inference_image
import os


@Client.on_message(filters.private & filters.command(["start"]))
async def start(bot, message, cb=False):
    if cb:
        message = message.message
    await add_user(message.from_user.id)
    await message.reply_text(
        text=START_TEXT,
        reply_markup=START_BUTTONS,
        disable_web_page_preview=True,
        quote=True,
    )


@Client.on_message(filters.private & filters.command(["help"]))
async def help(bot, message, cb=False):
    if cb:
        message = message.message
    await add_user(message.from_user.id)
    await message.reply_text(
        text=HELP_TEXT,
        reply_markup=HELP_BUTTONS,
        disable_web_page_preview=True,
        quote=True,
    )


@Client.on_message(filters.private & filters.command(["about"]))
async def about(bot, message, cb=False):
    if cb:
        message = message.message
    await add_user(message.from_user.id)
    await message.reply_text(
        text=ABOUT_TEXT,
        reply_markup=ABOUT_BUTTONS,
        disable_web_page_preview=True,
        quote=True,
    )


@Client.on_message(filters.photo and filters.private)
async def something(bot: Client, message: Message):
    if message.photo:
        file_path = await message.download(f"{message.chat.id}.jpg")
        img = PIL.Image.open(file_path)
        os.remove(file_path)
        response = await inference_image(PROMPT, img)
        await message.reply(response)
    else:
        pass
