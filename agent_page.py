import asyncio
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
import os

# ============================
# 🔑 مفتاح Gemini من البيئة
# ============================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ============================
# 🤖 دالة الاتصال بـ Gemini API
# ============================
def ask_gemini(prompt):
    """
    استدعاء Gemini API مع معالجة ذكية للأخطاء
    """
    if not GEMINI_API_KEY:
        return "⚠️ لم يتم العثور على مفتاح Gemini في الإعدادات. يرجى التواصل مع المطور."

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(url, headers=headers, params=params, json=payload, timeout=15)
        response.raise_for_status()
        result = response.json()

        text_output = ""
        for candidate in result.get("candidates", []):
            content = candidate.get("content", {})
            for part in content.get("parts", []):
                text_output += part.get("text", "") + "\n"

        return text_output.strip() if text_output else "⚠️ لم يتم العثور على نص في الرد."

    except requests.exceptions.Timeout:
        return "⏳ حدث تأخير في الاتصال بالخادم، حاول مجددًا بعد لحظة."
    except requests.exceptions.ConnectionError:
        return "📡 لا يوجد اتصال بالإنترنت، تحقق من الشبكة وحاول مرة أخرى."
    except requests.exceptions.HTTPError as e:
        return f"⚠️ خطأ في الخادم ({e.response.status_code}). حاول لاحقًا."
    except Exception as e:
        return f"⚠️ حدث خطأ غير متوقع أثناء الاتصال بالذكاء الاصطناعي: {e}"

# ============================
# 🧠 واجهة الوكيل الذكي
# ============================
async def agent_start(update: Update, context: ContextTypes.DEFAULT_TYPE, new_message=False):
    text = (
        "🤖 *مرحبًا بك في الوكيل الذكي!*\n\n"
        "أنا مساعد مخصص في مجالات البرمجة وعلوم الحاسب والذكاء الاصطناعي والأمن السيبراني وعلم البيانات.\n\n"
        "💬 يمكنك سؤالي مثلاً:\n"
        "• كيف أبدأ في الأمن السيبراني؟\n"
        "• ما الفرق بين الذكاء الاصطناعي والتعلم الآلي؟\n"
        "• اشرح لي كود بايثون بسيط."
    )

    keyboard = [
        [InlineKeyboardButton("📌 نصائح الاستخدام", callback_data="tips")],
        [InlineKeyboardButton("🏠 العودة للرئيسية", callback_data="home")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.user_data["mode"] = "agent"

    if new_message:
        await update.effective_chat.send_message(text=text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.callback_query.message.edit_text(text=text, reply_markup=reply_markup, parse_mode="Markdown")

# ============================
# 💡 واجهة النصائح
# ============================
async def agent_tips(update: Update, context: ContextTypes.DEFAULT_TYPE, new_message=False):
    tips_text = (
        "💡 *نصائح لاستخدام الوكيل الذكي بفعالية:*\n"
        "1. اطرح سؤالك بوضوح وحدد اللغة أو التقنية.\n"
        "2. يمكنك طلب أمثلة للكود أو خطوات عملية.\n"
        "3. استخدمه لتعلم المفاهيم المعقدة بطريقة مبسطة.\n"
        "4. لا تستخدمه خارج المجالات التقنية."
    )

    keyboard = [
        [InlineKeyboardButton("🤖 العودة للوكيل الذكي", callback_data="agent")],
        [InlineKeyboardButton("🏠 العودة للرئيسية", callback_data="home")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if new_message:
        await update.effective_chat.send_message(text=tips_text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.callback_query.message.edit_text(text=tips_text, reply_markup=reply_markup, parse_mode="Markdown")

# ============================
# 💬 معالجة الرسائل داخل الوكيل
# ============================
async def handle_agent_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.strip()
    chat_id = update.effective_chat.id

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

    # 🧠 كلمات المجال التقني المسموح به
    tech_keywords = [
        # لغات البرمجة
        "برمجة", "كود", "بايثون", "Python", "جافا", "Java", "C++", "C#", "HTML", "CSS", "JavaScript", "React", "Django", "Flask",
        # الذكاء الاصطناعي
        "ذكاء", "اصطناعي", "Machine Learning", "تعلم آلي", "تعلم عميق", "شبكات عصبية", "LLM", "ChatGPT", "Gemini",
        # الأمن السيبراني
        "أمن", "الأمن السيبراني", "Cybersecurity", "اختراق", "حماية", "تشفير", "Firewall", "هاكر", "هجوم", "تحليل جنائي", "Malware",
        # علم البيانات
        "بيانات", "تحليل بيانات", "Data Science", "Data Analysis", "إحصاء", "Pandas", "NumPy", "Visualization", "Big Data",
        # الشبكات والنظم
        "شبكات", "Network", "Server", "Linux", "نظام", "Operating System", "IP", "DNS", "VPN",
        # تطوير التطبيقات والمواقع
        "تطبيق", "App", "موقع", "Web", "Frontend", "Backend", "API", "واجهة", "UI", "UX", "Node.js",
        # الروبوتات
        "روبوت", "Robot", "تحكم", "Arduino", "Raspberry", "IoT",
        # هندسة البرمجيات
        "Software", "هندسة", "Git", "GitHub", "Agile", "Scrum", "DevOps", "نشر", "Deploy", "CI/CD"
    ]

    # 🚫 إذا لم يكن السؤال في المجال التقني
    if not any(keyword.lower() in user_text.lower() for keyword in tech_keywords):
        animation_task.cancel()
        try:
            await animation_task
        except asyncio.CancelledError:
            pass

        await typing_message.edit_text(
            "🤖 هذا الوكيل متخصص فقط في *البرمجة، الذكاء الاصطناعي، الأمن السيبراني، علم البيانات، وتكنولوجيا المعلومات.*\n\n"
            "🧠 يمكنك سؤالي مثلاً:\n"
            "• كيف أتعلم تحليل البيانات؟\n"
            "• ما الفرق بين الذكاء الاصطناعي والتعلم الآلي؟\n"
            "• كيف أبدأ في الأمن السيبراني؟"
        )
        return

    # ✅ تنفيذ الطلب فعليًا
    try:
        reply = await asyncio.to_thread(ask_gemini, user_text)
    except Exception as e:
        reply = f"⚠️ حدث خطأ أثناء المعالجة: {e}"

    # إيقاف الرسالة المتحركة بأمان
    animation_task.cancel()
    try:
        await animation_task
    except asyncio.CancelledError:
        pass

    await typing_message.edit_text(reply)

# ============================
# 🕹️ التعامل مع الأزرار
# ============================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "home":
        keyboard = [
            [InlineKeyboardButton("🤖 الوكيل الذكي", callback_data="agent")],
            [InlineKeyboardButton("📌 نصائح", callback_data="tips")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text("🏠 مرحبًا بك في الصفحة الرئيسية!", reply_markup=reply_markup)

    elif query.data == "tips":
        await agent_tips(update, context)

    elif query.data == "agent":
        await agent_start(update, context)
