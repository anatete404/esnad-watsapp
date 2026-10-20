import sys
import io

if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from fastapi.testclient import TestClient
import whatsapp_bot

# هنعمل "محاكاة" لدالة إرسال واتساب عشان متحاولش تتصل بـ Meta وتفشل لأننا لسه مجبناش التوكن
def mock_send_whatsapp(to, text):
    print(f"\n[MOCK WHATSAPP] Sending to {to}:\n{text}\n")

whatsapp_bot.send_whatsapp_message = mock_send_whatsapp

client = TestClient(whatsapp_bot.app)

def run_test():
    print("1. Testing Root Endpoint (GET /):")
    res = client.get("/")
    print(f"Status: {res.status_code}, Response: {res.json()}\n")

    print("2. Testing Webhook Verification (GET /webhook):")
    # بنجرب بكلمة سر غلط عشان نتأكد إنه بيرفض
    res = client.get("/webhook?hub.mode=subscribe&hub.verify_token=wrong&hub.challenge=123")
    print(f"Status: {res.status_code} (Expected: 403)\n")

    print("3. Testing Webhook Receiving (POST /webhook):")
    # بنعمل شكل الرسالة اللي واتساب بيبعتها بالظبط
    payload = {
        "entry": [{
            "changes": [{
                "value": {
                    "messages": [{
                        "from": "201012345678",
                        "type": "text",
                        "text": {"body": "مين اللي بيستخدم منصة إسناد؟"}
                    }]
                }
            }]
        }]
    }
    res = client.post("/webhook", json=payload)
    print(f"Status: {res.status_code}, Response: {res.json()}\n")
    print("لو ظهر [MOCK WHATSAPP] فوق، يبقى السيرفر استقبل الرسالة وبعت الرد بنجاح.")

if __name__ == "__main__":
    run_test()
