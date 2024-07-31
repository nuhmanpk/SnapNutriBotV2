import PIL
import os
import re
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
)
from .prompts import PROMPT
from .gemini import generate_with_gemini
from .stickers import LOADING_STICKERS


@Client.on_message(filters.private & filters.command(["start"]))
async def start(bot, message, cb=False):
    if cb:
        message = message.message
        await message.reply_text(
        text=START_TEXT,
        reply_markup=START_BUTTONS,
        disable_web_page_preview=True,
        quote=True,
        )
        return
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
        await message.reply_text(
        text=HELP_TEXT,
        reply_markup=HELP_BUTTONS,
        disable_web_page_preview=True,
        quote=True,
        )
        return
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
        await message.reply_text(
        text=ABOUT_TEXT,
        reply_markup=ABOUT_BUTTONS,
        disable_web_page_preview=True,
        quote=True,
        )
        return
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
            stkr = await message.reply_sticker(random.choice(LOADING_STICKERS))
            txt = await message.reply(ANALYZING_MESSAGE)
            file_path = await message.download(f"{message.chat.id}.jpg")
            img = PIL.Image.open(file_path)
            os.remove(file_path)
            response = await generate_with_gemini(PROMPT, img)
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
                    f"\n\n\nUse /today to track daily intake\n\n"
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


@Client.on_message(filters.command("today") & filters.private)
async def today_meals(bot: Client, message: Message):
    try:
        stkr = await message.reply_sticker(random.choice(LOADING_STICKERS))
        txt = await message.reply(ANALYZING_MESSAGE)
        user_id = message.from_user.id

        # Fetch today's meals from the database
        meals = await db.get_meals_by_user_and_date(user_id)

        if not meals:
            await stkr.delete()
            await txt.delete()
            await message.reply("You haven't logged any meals today.")
            return

        total_calories = 0
        total_protein = 0
        total_sugar = 0
        total_carbs = 0
        total_fat = 0

        meals_summary = "🍽️ **Today's Meal Summary:**\n\n"

        for meal in meals:
            def extract_number(value):
                match = re.search(r'(\d+)', value)
                return int(match.group(1)) if match else 0

            total_calories += extract_number(meal.get("calories", "0 kcal"))
            total_protein += extract_number(meal.get("protein", "0 gm"))
            total_carbs += extract_number(meal.get("carbs", "0 gm"))
            total_sugar += extract_number(meal.get("sugar", "0 gm"))
            total_fat += extract_number(meal.get("fat", "0 gm"))

            meals_summary += (
                f"**Meal at {meal['timestamp'].strftime('%H:%M')}** (UTC Time)\n"
                f"**Calories:** {meal.get('calories')}\n"
                f"**Protein:** {meal.get('protein')}\n"
                f"**Carbs:** {meal.get('carbs')}\n"
                f"**Fat:** {meal.get('fat')}\n"
                f"**Contents:** {', '.join(meal.get('meal_contents', []))}\n\n"
            )

        total_summary = (
            f"**Total Calories:** {total_calories} kcal\n"
            f"**Total Protein:** {total_protein} gm\n"
            f"**Total Carbs:** {total_carbs} gm\n"
            f"**Total Fat:** {total_fat} gm\n"
        )
        await stkr.delete()
        await txt.delete()
        await message.reply(meals_summary + total_summary)
    except Exception as e:
        print("Today:Error", e)
        await stkr.delete()
        await txt.edit("Oops, something went wrong on our end. Please try again later.")



