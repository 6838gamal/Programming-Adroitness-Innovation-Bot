import requests
from config import GEMINI_API_KEY

def ask_gemini_safe(prompt):
    """
    دالة آمنة للتعامل مع Gemini 2.5 Flash (v1beta/generateContent)
    وتستخرج كل النصوص من أي بنية محتملة.
    """
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(url, headers=headers, params=params, json=payload)
        response.raise_for_status()
        result = response.json()

        # التحقق من وجود 'candidates'
        candidates = result.get("candidates")
        if not candidates:
            return "⚠️ لم يتم الحصول على أي رد من الذكاء الاصطناعي."

        text_output = ""

        # المرور على كل المرشحين
        for candidate in candidates:
            content = candidate.get("content", [])
            if isinstance(content, list):
                for item in content:
                    if isinstance(item, dict):
                        # النصوص داخل 'parts'
                        parts = item.get("parts")
                        if isinstance(parts, list):
                            for part in parts:
                                if isinstance(part, dict) and "text" in part:
                                    text_output += part["text"] + "\n"
                        # النصوص مباشرة من النوع 'text' أو 'output_text'
                        if item.get("type") in ["text", "output_text"] and "text" in item:
                            text_output += item["text"] + "\n"
                    # إذا كان العنصر نص مباشر
                    elif isinstance(item, str):
                        text_output += item + "\n"
            # إذا كان 'content' نص مباشر
            elif isinstance(content, str):
                text_output += content + "\n"

        return text_output.strip() if text_output else "⚠️ لم يتم العثور على نص في الرد."

    except Exception as e:
        return f"⚠️ حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {e}"

# مثال استخدام
# print(ask_gemini_safe("Hello from Termux!"))
