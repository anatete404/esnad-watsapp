import sys
import io

if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from whatsapp_bot import client, company_context

def test_llm():
    user_text = "إيه هي منصة إسناد؟ ومين اللي بيستخدمها؟"
    print(f"User: {user_text}\n")
    print("Waiting for bot response...\n")
    
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": f"أنت مساعد خدمة عملاء ذكي ومحترف لشركة إسناد. استخدم المعلومات دي للرد على العميل: {company_context}"},
                {"role": "user", "content": user_text}
            ],
            temperature=0.5,
            max_tokens=500
        )
        print("Bot Reply:")
        print("-" * 40)
        print(response.choices[0].message.content)
        print("-" * 40)
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    test_llm()
