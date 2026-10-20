import os
from pathlib import Path
from dotenv import dotenv_values

env_path = Path(".env").resolve()
print(f"Working directory: {os.getcwd()}")
print(f"Looking for .env at: {env_path}")
print(f"File exists: {env_path.exists()}")

if not env_path.exists():
    raise SystemExit("ERROR: .env not found in current directory")

raw = dotenv_values(env_path)
print(f"\nKeys found in .env: {list(raw.keys())}")

for k in ["HF_TOKEN", "HF_USERNAME", "GROQ_API_KEY"]:
    v = raw.get(k)
    if v is None:
        print(f"MISSING: {k}")
    elif v == "":
        print(f"EMPTY: {k}")
    else:
        print(f"OK: {k} (length={len(v)})")
