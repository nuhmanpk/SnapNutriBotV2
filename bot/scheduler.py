from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from bot.database import db
from .prompts import DAILY_TIPS_PROMPT
from .gemini import generate_with_gemini


async def calculate_daily_intakes(bot):
    today = datetime.now().date()
    users_cursor = await db.get_all_users()
    async for user in users_cursor:
        meals_cursor = await db.get_meals_by_user(user['id'])
        total_calories = total_protein = total_carbs = total_fat = 0
        async for meal in meals_cursor:
            total_calories += int(meal.get("calories", "0").replace(" kcal", ""))
            total_protein += int(meal.get("protein", "0").replace(" gm", ""))
            total_carbs += int(meal.get("carbs", "0").replace(" gm", ""))
            total_fat += int(meal.get("fat", "0").replace(" gm", ""))

        insights = (
            f"Daily Intake for {today}:\n"
            f"**Total Calories:** {total_calories} kcal\n"
            f"**Total Protein:** {total_protein} gm\n"
            f"**Total Carbs:** {total_carbs} gm\n"
            f"**Total Fat:** {total_fat} gm\n"
        )

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
            await bot.send_message(user['id'], tip)
        except Exception as e:
            print(e)

scheduler = AsyncIOScheduler()

def start_scheduler(bot):
    scheduler.add_job(calculate_daily_intakes, 'cron', hour=0, minute=0, args=[bot])
    scheduler.add_job(send_daily_health_tip, 'cron', hour=0, minute=0, args=[bot])
    scheduler.start()
