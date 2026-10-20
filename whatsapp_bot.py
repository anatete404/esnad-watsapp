import os
import requests
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# إعداد عميل الموديل (Groq)
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

# إعدادات واتساب
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

# قراءة معلومات الشركة
def get_company_info():
    try:
        with open("company_info.txt", "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading company info: {e}")
        return "معلومات الشركة غير متاحة حالياً."

company_context = get_company_info()

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Esnad Chatbot is running!"}

# 1) التحقق من الـ Webhook
@app.get("/webhook")
async def verify(request: Request):
    params = request.query_params
    if params.get("hub.mode") == "subscribe" and params.get("hub.verify_token") == VERIFY_TOKEN:
        return PlainTextResponse(content=params.get("hub.challenge"), status_code=200)
    raise HTTPException(status_code=403, detail="Verification failed")

# 2) استقبال الرسايل والرد
@app.post("/webhook")
async def receive_message(request: Request):
    data = await request.json()
    try:
        entry = data["entry"][0]
        changes = entry["changes"][0]["value"]
        
        if "messages" in changes:
            msg = changes["messages"][0]
            from_number = msg["from"]
            
            if msg["type"] == "text":
                user_text = msg["text"]["body"]
                print(f"Received message from {from_number}: {user_text}")

                # إرسال السؤال للموديل
                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[
                        {"role": "system", "content": f"أنت مساعد خدمة عملاء ذكي ومحترف لشركة إسناد. استخدم المعلومات دي للرد على العميل: {company_context}"},
                        {"role": "user", "content": user_text}
                    ],
                    temperature=0.5,
                    max_tokens=500
                )
                reply_text = response.choices[0].message.content

                # إرسال الرد لواتساب
                send_whatsapp_message(from_number, reply_text)
                
    except Exception as e:
        print(f"Error handling message: {e}")
        
    return {"status": "ok"}

def send_whatsapp_message(to, text):
    url = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
    res = requests.post(url, headers=headers, json=payload)
    if res.status_code != 200:
        print(f"Failed to send message: {res.text}")

