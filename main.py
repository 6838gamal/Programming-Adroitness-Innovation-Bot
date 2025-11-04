from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from config import TOKEN
from about import about_info
from contact import contact_info
from channels import channels_info
from agent_page import agent_start, handle_agent_message, agent_tips
import asyncio

print("🚀 بوت البرمجة براعة وابتكار بدأ التشغيل بنجاح!")

# === الصفحة الرئيسية ===
async def home_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    text = f"🎓 أهلاً بك {user_name} في البرمجة براعة وابتكار!\n\nاختر القسم الذي ترغب في استكشافه:"
    keyboard = [
        [InlineKeyboardButton("🤖 الوكيل الذكي", callback_data="agent")],
        [InlineKeyboardButton("ℹ️ من نحن", callback_data="about")],
        [InlineKeyboardButton("📞 تواصل مع المطور", callback_data="contact")],
        [InlineKeyboardButton("📺 قنوات البرمجة براعة وابتكار", callback_data="channels")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.edit_text(text, reply_markup=reply_markup)

# === معالجة الأزرار ===
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

# === التعامل مع الرسائل ===
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("mode") == "agent":
        await handle_agent_message(update, context)
    else:
        await home_menu(update, context)

# === أوامر البوت ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await home_menu(update, context)

# === تشغيل البوت ===
async def main():
    app = Application.builder().token(TOKEN).build()

    # أوامر
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("agent", agent_start))
    app.add_handler(CommandHandler("about", about_info))
    app.add_handler(CommandHandler("contact", contact_info))
    app.add_handler(CommandHandler("channels", channels_info))

    # أزرار ورسائل
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    print("✅ البوت جاهز للعمل ...")
    await app.run_polling()

if __name__ == "__main__":
    # الطريقة الصحيحة لتشغيل البوت على Render
    asyncio.run(main())
