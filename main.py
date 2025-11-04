import asyncio
import streamlit as st
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from config import TOKEN
from about import about_info
from contact import contact_info
from channels import channels_info
from agent_page import agent_start, handle_agent_message, agent_tips

print("🚀 بوت البرمجة براعة وابتكار بدأ التشغيل بنجاح عبر Streamlit!")

# === الصفحة الرئيسية للبوت ===
async def home_menu(update, context):
    user_name = update.effective_user.first_name
    text = f"🎓 أهلاً بك {user_name} في البرمجة براعة وابتكار!\n\nاختر القسم الذي ترغب في استكشافه:"
    keyboard = [
        [dict(text="🤖 الوكيل الذكي", callback_data="agent")],
        [dict(text="ℹ️ من نحن", callback_data="about")],
        [dict(text="📞 تواصل مع المطور", callback_data="contact")],
        [dict(text="📺 قنوات البرمجة براعة وابتكار", callback_data="channels")]
    ]
    markup = {"inline_keyboard": [[{"text": b["text"], "callback_data": b["callback_data"]}] for b in keyboard]}
    if update.message:
        await update.message.reply_text(text, reply_markup=markup)
    elif update.callback_query:
        await update.callback_query.message.edit_text(text, reply_markup=markup)

# === معالجات ===
async def button_handler(update, context):
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

async def message_handler(update, context):
    if context.user_data.get("mode") == "agent":
        await handle_agent_message(update, context)
    else:
        await home_menu(update, context)

# === أوامر ===
async def start(update, context):
    await home_menu(update, context)

async def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("agent", agent_start))
    app.add_handler(CommandHandler("about", about_info))
    app.add_handler(CommandHandler("contact", contact_info))
    app.add_handler(CommandHandler("channels", channels_info))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    print("✅ البوت جاهز للعمل ...")
    await app.run_polling()

# تشغيل البوت داخل Streamlit
st.title("🤖 بوت البرمجة براعة وابتكار")
st.success("يتم تشغيل البوت الآن في الخلفية ✅")

asyncio.run(main())
