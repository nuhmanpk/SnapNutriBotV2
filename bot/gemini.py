import google.generativeai as genai
from .vars import GOOGLE_API_KEY, GEMINI_VISION, GEMINI_FLASH_1_5

genai.configure(api_key=GOOGLE_API_KEY)


async def generate_with_gemini(prompt, image=None):
    message = ""
    if prompt and image:
        MODEL = genai.GenerativeModel(GEMINI_VISION)
        response = MODEL.generate_content([prompt, image])
    else:
        MODEL = genai.GenerativeModel(GEMINI_FLASH_1_5)
        response = MODEL.generate_content(prompt)
    if response.parts:
        for part in response.parts:
            message += part.text
    return message
