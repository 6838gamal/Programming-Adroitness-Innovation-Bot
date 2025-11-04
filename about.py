from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

async def about_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👨‍💻 مشروع البرمجة براعة وابتكار\n"
        "تم تطويره بواسطة Gamal Almaqtary.\n\n"
        "🎯 الهدف: تقديم تجربة تعليمية ذكية ومبسطة باستخدام أحدث تقنيات الذكاء الاصطناعي."
    )
    keyboard = [[InlineKeyboardButton("🏠 العودة للرئيسية", callback_data="home")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # التعامل مع الرسائل العادية أو الأزرار
    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.edit_text(text, reply_markup=reply_markup)
