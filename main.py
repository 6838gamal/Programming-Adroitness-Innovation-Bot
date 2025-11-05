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

app = Flask(__name__)

telegram_app = Application.builder().token(TOKEN).build()

# ==========================
# وظائف البوت
# ==========================
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

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("mode") == "agent":
        await handle_agent_message(update, context)
    else:
        await home_menu(update, context)

# ==========================
# تسجيل Handlers
# ==========================
telegram_app.add_handler(CommandHandler("start", home_menu))
telegram_app.add_handler(CommandHandler("agent", button_handler))
telegram_app.add_handler(CommandHandler("about", about_info))
telegram_app.add_handler(CommandHandler("contact", contact_info))
telegram_app.add_handler(CommandHandler("channels", channels_info))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
telegram_app.add_handler(CallbackQueryHandler(button_handler))

# ==========================
# Webhook route
# ==========================
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    asyncio.create_task(telegram_app.process_update(update))
    return "OK", 200

@app.route("/")
def home():
    return "🤖 بوت البرمجة براعة وابتكار يعمل بنجاح على Render!"

# ==========================
# نقطة التشغيل
# ==========================
if __name__ == "__main__":
    async def start_bot():
        await telegram_app.initialize()
        await telegram_app.start()
        await telegram_app.bot.set_webhook(url="https://Programming-Adroitness-Innovation-Bot.onrender.com/webhook")
        print("🔗 تم تعيين Webhook بنجاح!")

    asyncio.run(start_bot())
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
