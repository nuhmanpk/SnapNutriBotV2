import google.generativeai as genai
from .vars import GOOGLE_API_KEY, GEMINI_VISION, GEMINI_FLASH_1_5

genai.configure(api_key=GOOGLE_API_KEY)


async def generate_with_gemini(prompt, image=None):
    message = ""
    if prompt and image:
        MODEL = genai.GenerativeModel(GEMINI_VISION)
        response = MODEL.generate_content([prompt, image])
        print('Resp 1 from default prompt',response)
        pro = 'identify the food items , and return the nutrients , fat, calore and items includes in the food item'
        response1 = MODEL.generate_content([pro, image])
        print('Resp 2 from custom prompt',response1)
    else:
        MODEL = genai.GenerativeModel(GEMINI_FLASH_1_5)
        response = MODEL.generate_content(prompt)
    if response.parts:
        for part in response.parts:
            message += part.text
    return message
