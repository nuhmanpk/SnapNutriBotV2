import google.generativeai as genai
from .vars import GOOGLE_API_KEY, MODEL_NAME

genai.configure(api_key=GOOGLE_API_KEY)
MODEL = genai.GenerativeModel(MODEL_NAME)


async def inference_image(prompt, image):
    message = ""
    response = MODEL.generate_content([prompt, image])
    if response.parts:
        for part in response.parts:
            message += part.text
    return message
