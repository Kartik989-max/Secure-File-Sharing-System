

users = []
files = []

def initialize_default_users():
    from auth import hash_password
    if not get_user_by_email("ops@example.com"):
        users.append({
            "email": "ops@example.com",
            "password": hash_password("ops123"),
            "role": "ops",
            "verified": True
        })

def get_user_by_email(email):
    return next((u for u in users if u["email"] == email), None)

def create_user(user):
    users.append(user)

def verify_user(email):
    for u in users:
        if u["email"] == email:
            u["verified"] = True

def add_file(file):
    files.append(file)

def get_all_files():
    return files
