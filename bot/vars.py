from decouple import config


ADMINS = config('ADMINS', cast=lambda v: set(int(x) for x in v.split()))
DATABASE_URL = config('DATABASE_URL')
DATABASE_NAME = config('DATABASE_NAME')
GOOGLE_API_KEY = config("GOOGLE_API_KEY")
MODEL_NAME = "gemini-pro-vision"
