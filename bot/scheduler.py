from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from bot.database import db
from .prompts import DAILY_TIPS_PROMPT
from .gemini import generate_with_gemini
from time import sleep

def safe_int_conversion(value, unit):
    try:
        return int(value.replace(unit, "").strip())
    except ValueError:
        return 0

async def calculate_daily_intakes(bot):
    today = datetime.now().date()
    users_cursor = await db.get_all_users()
    async for user in users_cursor:
        meals_cursor = await db.get_meals_by_user(user['id'])
        total_calories = total_protein = total_carbs = total_fat = 0
        async for meal in meals_cursor:
                total_calories += safe_int_conversion(meal.get("calories", "0 kcal"), "kcal")
                total_protein += safe_int_conversion(meal.get("protein", "0 gm"), "gm")
                total_carbs += safe_int_conversion(meal.get("carbs", "0 gm"), "gm")
                total_fat += safe_int_conversion(meal.get("fat", "0 gm"), "gm")

        insights = (
            f"Daily Intake for {today}:\n"
            f"**Total Calories:** {total_calories} kcal\n"
            f"**Total Protein:** {total_protein} gm\n"
            f"**Total Carbs:** {total_carbs} gm\n"
            f"**Total Fat:** {total_fat} gm\n"
        )
        sleep(3)
        await send_insight_to_user(bot, user['id'], insights)

async def send_insight_to_user(bot, user_id, insights):
    try:
        await bot.send_message(user_id, insights)
    except Exception as e:
        print(e)

async def send_daily_health_tip(bot):
    users_cursor = await db.get_all_users()
    tip = await generate_with_gemini(DAILY_TIPS_PROMPT,)

    async for user in users_cursor:
        try:
            sleep(3)
            await bot.send_message(user['id'], tip)
        except Exception as e:
            print(e)

scheduler = AsyncIOScheduler()

def start_scheduler(bot):
    scheduler.add_job(calculate_daily_intakes, 'cron', hour=0, minute=0, args=[bot])
    scheduler.add_job(send_daily_health_tip, 'cron', hour=0, minute=10, args=[bot])
    scheduler.start()
