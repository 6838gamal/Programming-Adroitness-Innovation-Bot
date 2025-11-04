import asyncio
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
import os

# ======== مفتاح Gemini ========
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ======== دالة الاتصال بـ Gemini ========
def ask_gemini(prompt):
    """
    استدعاء Gemini API وإرجاع الرد النصي الآمن
    """
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(url, headers=headers, params=params, json=payload)
        response.raise_for_status()
        result = response.json()

        if not isinstance(result, dict):
            return "⚠️ الرد غير متوقع من Gemini."

        text_output = ""
        for candidate in result.get("candidates", []):
            content = candidate.get("content", {})
            if isinstance(content, dict):
                for part in content.get("parts", []):
                    text_output += part.get("text", "") + "\n"

        return text_output.strip() if text_output else "⚠️ لم يتم العثور على نص في الرد."
    except Exception as e:
        return f"⚠️ حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {e}"

# ======== واجهة صفحة الوكيل ========
async def agent_start(update: Update, context: ContextTypes.DEFAULT_TYPE, new_message=False):
    text = (
        "🤖 مرحبًا بك في *الوكيل الذكي*!\n\n"
        "يمكنك طرح أي سؤال مثلاً:\n"
        "• كيف أتعلم بايثون بسرعة؟\n"
        "• ما أحدث تقنيات الذكاء الاصطناعي؟"
    )

    keyboard = [
        [InlineKeyboardButton("🏠 العودة للرئيسية", callback_data="home")],
        [InlineKeyboardButton("📌 نصائح شائعة", callback_data="tips")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.user_data["mode"] = "agent"

    if new_message:
        await update.effective_chat.send_message(text=text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.callback_query.message.edit_text(text=text, reply_markup=reply_markup, parse_mode="Markdown")

# ======== واجهة النصائح ========
async def agent_tips(update: Update, context: ContextTypes.DEFAULT_TYPE, new_message=False):
    tips_text = (
        "💡 *نصائح سريعة لاستخدام الوكيل الذكي:*\n"
        "1. اطرح أسئلة محددة للحصول على إجابة دقيقة.\n"
        "2. أعد صياغة السؤال إذا لم تحصل على الرد المطلوب.\n"
        "3. يمكنك طلب أمثلة للكود أو خطوات عملية."
    )

    keyboard = [
        [InlineKeyboardButton("🏠 العودة للرئيسية", callback_data="home")],
        [InlineKeyboardButton("🤖 العودة للوكيل الذكي", callback_data="agent")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if new_message:
        await update.effective_chat.send_message(text=tips_text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.callback_query.message.edit_text(text=tips_text, reply_markup=reply_markup, parse_mode="Markdown")

# ======== معالجة الرسائل داخل الوكيل ========
async def handle_agent_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.strip()
    chat_id = update.effective_chat.id

    # رسالة مؤقتة أثناء الكتابة
    typing_message = await update.message.reply_text("✍️ المساعد يكتب الرد...")

    # محاكاة الكتابة بالنقاط المتحركة
    async def animate_typing():
        dots = [".", "..", "..."]
        i = 0
        while True:
            try:
                await typing_message.edit_text(f"🤖 المساعد يكتب{dots[i % 3]}")
                await asyncio.sleep(0.7)
                i += 1
            except:
                break

    animation_task = asyncio.create_task(animate_typing())

    try:
        loop = asyncio.get_event_loop()
        reply = await loop.run_in_executor(None, ask_gemini, user_text)
    except Exception as e:
        reply = f"⚠️ حدث خطأ أثناء المعالجة: {e}"

    # إيقاف الرسالة المتحركة
    animation_task.cancel()
    await asyncio.sleep(0.2)

    # تعديل الرسالة بالرد النهائي مباشرة
    await typing_message.edit_text(reply)

# ======== التعامل مع الأزرار ========
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "home":
        await query.message.edit_text("🏠 مرحبًا بك في الصفحة الرئيسية!")
    elif query.data == "tips":
        await agent_tips(update, context)
    elif query.data == "agent":
        await agent_start(update, context)
