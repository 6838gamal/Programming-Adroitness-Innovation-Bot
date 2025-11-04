import asyncio
import nest_asyncio
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
print("🚀 بوت البرمجة براعة وابتكار بدأ التشغيل بنجاح!")


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
# معالجة الأزرار (Callback Buttons)
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
    # إذا المستخدم في وضع "الوكيل الذكي"
    if context.user_data.get("mode") == "agent":
        await handle_agent_message(update, context)
    else:
        await home_menu(update, context)


# ====================================================
# أوامر مباشرة (Commands)
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


# ====================================================
# تشغيل التطبيق
# ====================================================
async def main():
    print("✅ بدء تشغيل البوت (Polling Mode)...")

    app = Application.builder().token(TOKEN).build()

    # أوامر
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("agent", agent_command))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(CommandHandler("contact", contact_command))
    app.add_handler(CommandHandler("channels", channels_command))

    # الأزرار والرسائل
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    # بدء التشغيل
    await app.run_polling(drop_pending_updates=True)


# ====================================================
# نقطة الدخول للتشغيل
# ====================================================
if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.run(main())
