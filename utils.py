
from cryptography.fernet import Fernet
import mimetypes
import os
from dotenv import load_dotenv

load_dotenv()

FERNET_KEY = os.getenv("FERNET_KEY")
fernet = Fernet(FERNET_KEY.encode())

def encrypt_data(data: str) -> str:
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()

def allowed_file(filename: str) -> bool:
    return filename.endswith((".docx", ".pptx", ".xlsx"))

def simulate_email(to_email: str, verify_url: str):
    print(f"Simulated email to {to_email}: Click to verify -> {verify_url}")
