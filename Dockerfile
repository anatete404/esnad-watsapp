FROM python:3.11-slim

# إنشاء مستخدم UID 1000 عشان صلاحيات Hugging Face
RUN useradd -m -u 1000 user

WORKDIR /home/user/app

# نسخ المتطلبات وتثبيتها الأول
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# نسخ باقي الملفات
COPY --chown=user . .

USER user
ENV HOME=/home/user
PATH=/home/user/.local/bin:$PATH

# Hugging Face بيستخدم بورت 7860
EXPOSE 7860

# تشغيل السيرفر
CMD ["uvicorn", "whatsapp_bot:app", "--host", "0.0.0.0", "--port", "7860"]
