


from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordRequestForm
from auth import create_access_token, get_current_user, verify_password, hash_password
from utils import encrypt_data, decrypt_data, allowed_file, simulate_email
from schema import UserCreate, User, Role
from database import get_user_by_email, create_user, verify_user, add_file, get_all_files, initialize_default_users
from file_handler import save_file, get_file_by_id
import uuid

app = FastAPI()

initialize_default_users()

@app.post("/client/signup")
async def signup(user: UserCreate, request: Request):
    if get_user_by_email(user.email):
        raise HTTPException(status_code=400, detail="User already exists")

    user_data = user.dict()
    user_data["role"] = Role.client
    user_data["password"] = hash_password(user.password)
    user_data["verified"] = False
    create_user(user_data)

    token = encrypt_data(user.email)
    verify_url = f"{request.base_url}client/verify-email?token={token}"
    simulate_email(user.email, verify_url)

    return {"message": "Verify email", "verify_url": verify_url}

@app.get("/client/verify-email")
async def verify_email(token: str):
    email = decrypt_data(token)
    user = get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    verify_user(email)
    return {"message": "Email verified successfully"}

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    if user["role"] == Role.client and not user["verified"]:
        raise HTTPException(status_code=401, detail="Please verify your email")
    token = create_access_token(user["email"], user["role"])
    return {"access_token": token, "token_type": "bearer"}

@app.post("/ops/upload")
async def upload_file(file: UploadFile = File(...), user=Depends(get_current_user)):
    if user["role"] != Role.ops:
        raise HTTPException(status_code=403, detail="Only Ops can upload")
    if not allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="File type not allowed")
    file_id = str(uuid.uuid4())
    path = save_file(file, file_id)
    add_file({"id": file_id, "name": file.filename, "path": path, "uploaded_by": user["email"]})
    return {"message": "File uploaded", "file_id": file_id}

@app.get("/client/files")
async def list_files(user=Depends(get_current_user)):
    if user["role"] != Role.client:
        raise HTTPException(status_code=403, detail="Only Clients can view")
    return get_all_files()

@app.get("/client/download-link/{file_id}")
async def get_download_link(file_id: str, user=Depends(get_current_user), request: Request = None):
    if user["role"] != Role.client:
        raise HTTPException(status_code=403, detail="Only Clients can generate link")
    token = encrypt_data(file_id)
    return {"download-link": f"{request.base_url}download-file/{token}", "message": "success"}

@app.get("/download-file/{token}")
async def download_file(token: str, user=Depends(get_current_user)):
    if user["role"] != Role.client:
        raise HTTPException(status_code=403, detail="Only Clients can download")
    file_id = decrypt_data(token)
    file = get_file_by_id(file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file["path"], filename=file["name"])
