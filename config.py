from dotenv import load_dotenv
import os

# تحميل القيم من ملف .env إذا موجود
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_KEY")
