import PIL
import os
import random
import json
from hydrogram import filters
from hydrogram import Client
from hydrogram.types import Message
from hydrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .database import db
from .admin import add_user
from .buttons import HELP_BUTTONS, START_BUTTONS, ABOUT_BUTTONS, CLOSE_BUTTON
from .constants import (
    START_TEXT,
    HELP_TEXT,
    ABOUT_TEXT,
    ANALYZING_MESSAGE,
    GENDER_PROMPT,
    GENDERS,
)
from .prompts import PROMPT
from .gemini import inference_image
from .stickers import LOADING_STICKERS


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
async def snap_nutri(bot: Client, message: Message):
    if message.photo:
        try:
            await add_user(message.from_user.id)
            user = await db.get_user(message.from_user.id)
            stkr = await message.reply_sticker(random.choice(LOADING_STICKERS))
            txt = await message.reply(ANALYZING_MESSAGE)
            file_path = await message.download(f"{message.chat.id}.jpg")
            img = PIL.Image.open(file_path)
            os.remove(file_path)
            response = await inference_image(PROMPT, img)
            response_data = json.loads(response)

            if response_data.get("status"):

                data = response_data["data"]
                meal_contents = response_data["meal_contents"]
                information = response_data["information"]

                response_message = (
                    f"🍽️ **Nutritional Information:**\n"
                    f"**Dish:** {data['meal']}\n"
                    f"**Calories:** {data['calories']}\n"
                    f"**Sugar:** {data['sugar']}\n"
                    f"**Protein:** {data['protein']}\n"
                    f"**Carbs:** {data['carbs']}\n"
                    f"**Fat:** {data['fat']}\n\n"
                    f"**Meal Contents:** {', '.join(meal_contents)}\n\n"
                    f"**Information:** {information}"
                )

                meal_data = {
                    "calories": data["calories"],
                    "sugar": data["sugar"],
                    "protein": data["protein"],
                    "carbs": data["carbs"],
                    "fat": data["fat"],
                    "meal_contents": meal_contents,
                    "information": information,
                    "timestamp": message.date,
                }
                meal_id = await db.add_meal(message.from_user.id, meal_data)
                DELETE_MEAL_BUTTON = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Wrong prediction? Delete this entry.",
                                callback_data=f"delete_{meal_id}",
                            )
                        ]
                    ]
                )
                await message.reply(response_message, reply_markup=DELETE_MEAL_BUTTON)
                await stkr.delete()
                await txt.delete()
            else:
                await stkr.delete()
                await txt.edit(
                    "❌ The provided image doesn't seem to be a meal. Please try again with a different photo."
                )

        except Exception as e:
            print("snap_nutri:Error", e)
            await stkr.delete()
            await txt.edit("Oops , I broke something in backend")
