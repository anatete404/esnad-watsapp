import os
from dotenv import load_dotenv
from huggingface_hub import HfApi, create_repo

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
GROQ_KEY = os.getenv("GROQ_API_KEY")

# اسم المستخدم ثابت هنا لتخطي مشاكل قراءة .env
HF_USERNAME = "esnad"
SPACE_NAME = "esnad-chatbot"

if not HF_TOKEN:
    raise SystemExit("ERROR: HF_TOKEN is missing in .env")
if not GROQ_KEY:
    raise SystemExit("ERROR: GROQ_API_KEY is missing in .env")

print("Loaded HF_TOKEN: yes (value hidden)")
print("Loaded GROQ_API_KEY: yes (value hidden)")
print(f"Deploying to Space: {HF_USERNAME}/{SPACE_NAME}")

api = HfApi(token=HF_TOKEN)

print("\nCreating Space ...")
try:
    create_repo(
        repo_id=f"{HF_USERNAME}/{SPACE_NAME}",
        repo_type="space",
        space_sdk="docker",
        private=False,
        token=HF_TOKEN,
        exist_ok=True,
    )
    print("Space created (or already exists).")
except Exception as e:
    print(f"Error creating space: {e}")
    raise

print("\nUploading files ...")
api.upload_folder(
    folder_path=".",
    repo_id=f"{HF_USERNAME}/{SPACE_NAME}",
    repo_type="space",
    token=HF_TOKEN,
    allow_patterns=[
        "whatsapp_bot.py",
        "company_info.txt",
        "requirements.txt",
        "Dockerfile",
        "README.md",
    ],
    commit_message="Initial deploy from local",
)
print("Files uploaded.")

print("\nSetting secrets ...")
api.add_space_secret(repo_id=f"{HF_USERNAME}/{SPACE_NAME}", key="GROQ_API_KEY", value=GROQ_KEY, token=HF_TOKEN)
api.add_space_secret(repo_id=f"{HF_USERNAME}/{SPACE_NAME}", key="VERIFY_TOKEN", value="esnad_secret_2026", token=HF_TOKEN)
api.add_space_secret(repo_id=f"{HF_USERNAME}/{SPACE_NAME}", key="WHATSAPP_TOKEN", value="temp", token=HF_TOKEN)
api.add_space_secret(repo_id=f"{HF_USERNAME}/{SPACE_NAME}", key="PHONE_NUMBER_ID", value="temp", token=HF_TOKEN)
print("Secrets set.")

print("\nSpace URL:", f"https://huggingface.co/spaces/{HF_USERNAME}/{SPACE_NAME}")
print("Live App URL:", f"https://{HF_USERNAME}-{SPACE_NAME}.hf.space")
