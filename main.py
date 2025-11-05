import os
import asyncio
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# ===== ملفات المشروع =====
from config import TOKEN
from about import about_info
from contact import contact_info
from channels import channels_info
from agent_page import agent_start, handle_agent_message, agent_tips

# ====================================================
# رسالة التشغيل
# ====================================================
print("🚀 بوت البرمجة براعة وابتكار بدأ التشغيل بنجاح (نسخة Render Flask)!")

# ====================================================
# إعداد Flask
# ====================================================
app = Flask(__name__)

# ====================================================
# إعداد تطبيق Telegram
# ====================================================
telegram_app = Application.builder().token(TOKEN).build()

# ====================================================
# القائمة الرئيسية
# ====================================================
async def home_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    text = (
        f"👋 أهلاً بك {user_name} في مشروع البرمجة براعة وابتكار!\n\n"
        "🌟 اختر ما ترغب في استكشافه من القائمة أدناه:"
    )
    keyboard = [
        [InlineKeyboardButton("🤖 الوكيل الذكي", callback_data="agent")],
        [InlineKeyboardButton("ℹ️ من نحن", callback_data="about")],
        [InlineKeyboardButton("📞 تواصل مع المطور", callback_data="contact")],
        [InlineKeyboardButton("📺 قنوات البرمجة براعة وابتكار", callback_data="channels")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.edit_text(text, reply_markup=reply_markup)

# ====================================================
# معالجة الأزرار
# ====================================================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "agent":
        await agent_start(update, context, new_message=True)
        context.user_data["mode"] = "agent"

    elif query.data == "tips":
        await agent_tips(update, context, new_message=True)

    elif query.data == "about":
        await about_info(update, context)
        context.user_data["mode"] = None

    elif query.data == "contact":
        await contact_info(update, context)
        context.user_data["mode"] = None

    elif query.data == "channels":
        await channels_info(update, context)
        context.user_data["mode"] = None

    elif query.data in ["home", "main_menu"]:
        await home_menu(update, context)
        context.user_data["mode"] = None

# ====================================================
# التعامل مع الرسائل النصية
# ====================================================
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("mode") == "agent":
        await handle_agent_message(update, context)
    else:
        await home_menu(update, context)

# ====================================================
# أوامر مباشرة
# ====================================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await home_menu(update, context)

async def agent_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await agent_start(update, context, new_message=True)
    context.user_data["mode"] = "agent"

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await about_info(update, context)
    context.user_data["mode"] = None

async def contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await contact_info(update, context)
    context.user_data["mode"] = None

async def channels_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await channels_info(update, context)
    context.user_data["mode"] = None

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await home_menu(update, context)
    context.user_data["mode"] = None

# ====================================================
# تسجيل Handlers داخل تطبيق Telegram
# ====================================================
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("agent", agent_command))
telegram_app.add_handler(CommandHandler("about", about_command))
telegram_app.add_handler(CommandHandler("contact", contact_command))
telegram_app.add_handler(CommandHandler("channels", channels_command))
telegram_app.add_handler(CommandHandler("menu", menu_command))
telegram_app.add_handler(CallbackQueryHandler(button_handler))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

# ====================================================
# إعداد Webhook لـ Render
# ====================================================
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://Programming-Adroitness-Innovation-Bot.onrender.com{WEBHOOK_PATH}"

@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    """نقطة استقبال التحديثات من Telegram"""
    data = request.get_json(force=True)
    update = Update.de_json(data, telegram_app.bot)
    asyncio.run(telegram_app.process_update(update))
    return "OK", 200

@app.route("/")
def home():
    return (
        "<h2>🤖 بوت البرمجة براعة وابتكار</h2>"
        "<p>يعمل الآن بنجاح على Render!</p>"
        "<p>👨‍💻 المطور: <b>جمال الهويش</b></p>"
        "<p>🚀 المشروع: Programming Adroitness & Innovation</p>"
    ), 200

# ====================================================
# نقطة التشغيل
# ====================================================
if __name__ == "__main__":
    # استخدام asyncio.run لضمان تنفيذ set_webhook بشكل صحيح
    async def setup_webhook():
        await telegram_app.bot.delete_webhook()
        await telegram_app.bot.set_webhook(url=WEBHOOK_URL)
        print(f"🔗 تم تعيين Webhook على: {WEBHOOK_URL}")

    asyncio.run(setup_webhook())

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
