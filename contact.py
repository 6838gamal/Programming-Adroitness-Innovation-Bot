import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, CallbackQueryHandler

# =====================
# قائمة الرموز التعبيرية لكل منصة
# =====================
emoji_options = {
    "twitter": ["🐦", "🕊️", "🌬️"],
    "facebook": ["📘", "💙", "📖"],
    "whatsapp": ["📱", "💬", "📲"],
    "telegram": ["✈️", "📨", "🛩️"],
    "linkedin": ["💼", "📊", "🏢"],
    "youtube": ["📺", "🎬", "🍿"],
    "tiktok": ["🎵", "🎶", "🎤"],
    "instagram": ["📸", "🌟", "📷"],
    "x": ["🐦", "🪶", "🌐"]
}

def random_emoji(platform):
    return random.choice(emoji_options.get(platform, ["🌐"]))

# =====================
# لوحة مفاتيح التواصل
# =====================
def build_contact_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(f"{random_emoji('x')} X", url="https://x.com/alhwysh787472?s=09"),
            InlineKeyboardButton(f"{random_emoji('facebook')} فيسبوك", url="https://www.facebook.com/jmal.alhwysh.2025?mibextid=rS40aB7S9Ucbxw6v")
        ],
        [
            InlineKeyboardButton(f"{random_emoji('whatsapp')} واتساب", url="https://wa.me/774440982"),
            InlineKeyboardButton(f"{random_emoji('telegram')} تلجرام", url="https://t.me/Gamalalhwish")
        ],
        [
            InlineKeyboardButton(f"{random_emoji('linkedin')} لينكدإن", url="https://www.linkedin.com/in/gamal-alhwish")
        ],
        [
            InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# =====================
# لوحة مفاتيح القائمة الرئيسية
# =====================
def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("📬 تواصل معنا", callback_data="contact")],
        [InlineKeyboardButton("ℹ️ عن المشروع", callback_data="about")],
        [InlineKeyboardButton("💡 نصائح الوكيل الذكي", callback_data="agent_tips")]
    ]
    return InlineKeyboardMarkup(keyboard)

# =====================
# صفحة التواصل
# =====================
async def contact_info(update: Update, context: ContextTypes.DEFAULT_TYPE = None):
    text = (
        "🤝 تواصل معنا على المنصات التالية:\n\n"
        "اختر المنصة التي تفضلها 👇\n\n"
        "💬 فريقنا جاهز دائمًا للرد على استفساراتك!"
    )

    if hasattr(update, "callback_query") and update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.message.edit_text(text=text, reply_markup=build_contact_keyboard())
    elif hasattr(update, "message") and update.message:
        await update.message.reply_text(text=text, reply_markup=build_contact_keyboard())

# =====================
# معالج زر الرجوع للقائمة الرئيسية
# =====================
async def main_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.edit_text(
        text="🏠 مرحبًا بك في القائمة الرئيسية!",
        reply_markup=main_menu_keyboard()
    )

# =====================
# معالج زر الانتقال لصفحة التواصل من القائمة الرئيسية
# =====================
async def contact_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await contact_info(update, context)

# =====================
# لتسجيل المعالجات داخل البوت الرئيسي
# =====================
# application.add_handler(CallbackQueryHandler(main_menu_handler, pattern="^main_menu$"))
# application.add_handler(CallbackQueryHandler(contact_button_handler, pattern="^contact$"))
