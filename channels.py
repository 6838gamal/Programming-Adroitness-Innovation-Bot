import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, CallbackQueryHandler

# =====================
# الرموز التعبيرية لكل منصة
# =====================
emoji_options = {
    "youtube": ["📺", "🎬", "🍿"],
    "telegram": ["✈️", "📨", "🛩️"]
}

def random_emoji(platform):
    return random.choice(emoji_options.get(platform, ["🌐"]))

# =====================
# لوحة القنوات
# =====================
def build_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(
                f"{random_emoji('youtube')} يوتيوب", 
                url="https://www.youtube.com/@ProgramingAdroitnessInnovation"
            ),
            InlineKeyboardButton(
                f"{random_emoji('telegram')} تليجرام", 
                url="https://t.me/ProgrammingAdroitnessInnovation"
            )
        ],
        [
            InlineKeyboardButton("🏠 العودة للرئيسية", callback_data="home")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# =====================
# لوحة الرئيسية
# =====================
def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("📬 القنوات والمنصات", callback_data="channels")],
        [InlineKeyboardButton("ℹ️ عن المشروع", callback_data="about")],
        [InlineKeyboardButton("💡 نصائح الوكيل الذكي", callback_data="agent_tips")]
    ]
    return InlineKeyboardMarkup(keyboard)

# =====================
# صفحة القنوات
# =====================
async def channels_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📺 قنوات مشروع البرمجة براعة وابتكار:\n\n"
        "اختر المنصة المفضلة لديك 👇\n\n"
        "💬 تواصل معنا وشاركنا أفكارك!"
    )

    if update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.message.edit_text(text=text, reply_markup=build_keyboard())
    elif update.message:
        await update.message.reply_text(text=text, reply_markup=build_keyboard())

# =====================
# العودة للرئيسية
# =====================
async def home_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.edit_text(
        text="🏠 مرحبًا بك في القائمة الرئيسية!",
        reply_markup=main_menu_keyboard()
    )

# =====================
# التسجيل في main.py (عند الحاجة)
# =====================
# application.add_handler(CallbackQueryHandler(channels_info, pattern="^channels$"))
# application.add_handler(CallbackQueryHandler(home_handler, pattern="^home$"))
