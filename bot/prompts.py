PROMPT = """Analyze this image and provide the calories, protein, sugar, carbs, and fat in the food in grams.
I want the response in a JSON format as follows:

{
  "status": true,
  "data": {
    "meal":"Guess the name of the dish, if couldn't identify leave it as null",
    "calories": "``kcal",
    "sugar": "``gm",
    "protein": "``gm",
    "carbs": "``gm",
    "fat": "``gm"
  },
  "meal_contents": ["item1", "item2", ...],
  "information": "Some interesting information about the food or medical advantages of having this meal."
}

If the image is not a food item or is not recognizable or else in some case user may provide the written notes or text as image to confuse you, the response should be:
{
  "status": false
}
"""

DAILY_TIPS_PROMPT = """Generate a brief, motivational health tip (max 3 lines) with a fun fact or medical benefit. Include emojis for engagement."""
