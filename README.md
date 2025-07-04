# Secure File Sharing System

This project is a secure file-sharing system built with FastAPI. It supports two types of users — Ops and Clients — with different roles and permissions for uploading and downloading files. The goal was to implement authentication, role-based access, secure file handling, and email verification using encrypted links.


## Technologies Used

- **Python 3.8+**
- **FastAPI** – Web framework for building APIs
- **Uvicorn** – ASGI server for running FastAPI
- **Fernet (Cryptography)** – For secure encryption/decryption of tokens
- **JWT (JSON Web Tokens)** – Authentication and access control
- **Passlib (bcrypt)** – Password hashing and verification
- **Pydantic** – Data validation and serialization
- **Python’s pathlib and os modules** – File handling
- **Postman** – API testing and collection sharing
- **dotenv** – Managing environment variables
- **In-memory mock database** – Python lists (users and files)

## Features

### Ops User
- Login
- Upload files (`.docx`, `.pptx`, `.xlsx` only)

### Client User
- Sign up (returns an encrypted email verification URL)
- Email verification
- Login
- List all uploaded files
- Request secure download links
- Download files through encrypted token URLs

## Tech Stack
- FastAPI (Python)
- JWT for authentication
- Fernet for encrypted URLs
- Local file storage
- In-memory storage (mocked DB using Python lists)

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/secure-file-sharing-api.git
   cd secure-file-sharing-api```

2. Create a virtual environment:

  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
````

4. Create a .env file:

```bash
SECRET_KEY=your-secret-key
FERNET_KEY=your-fernet-key
```

5. To generate a Fernet key:

```bash
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
```

6. Start the server:

```bash
uvicorn main:app --reload
```

# API Endpoints

| Method | Endpoint                          | Description                        |
|--------|-----------------------------------|------------------------------------|
| POST   | /client/signup                    | Client registration                |
| GET    | /client/verify-email?token=...    | Email verification                 |
| POST   | /login                            | Login (for both roles)             |
| POST   | /ops/upload                       | File upload (Ops only)             |
| GET    | /client/files                     | List all uploaded files (Clients)  |
| GET    | /client/download-link/{file_id}   | Generate encrypted download link   |
| GET    | /download-file/{token}            | Download file securely             |

---

# Postman Collection

A Postman collection is included to test all endpoints from signup to secure file download.

---

# Test Cases and Deployment Plan

## 1. Write Test Cases for the Above

Below are suggested test cases for the secure file-sharing API, organized by user role and feature:

### Client User

- **Signup**
  - Should register a new client and return an encrypted verification link
  - Should reject duplicate email registrations

- **Email Verification**
  - Should verify the email when a valid token is passed
  - Should return an error for an invalid or expired token

- **Login**
  - Should login after email verification and return a JWT token
  - Should prevent login before email verification
  - Should reject login with wrong credentials

- **List Files**
  - Should list all uploaded files for an authenticated client
  - Should return 403 if accessed by a non-client or unauthenticated user

- **Download Link**
  - Should generate an encrypted download link for a valid file
  - Should deny link generation for non-clients

- **Download File**
  - Should allow downloading the file using the encrypted token
  - Should reject access if role is not client or token is invalid

### Ops User

- **Login**
  - Should allow valid ops user login
  - Should reject login with invalid credentials

- **Upload File**
  - Should upload a valid `.docx`, `.pptx`, or `.xlsx` file
  - Should reject unsupported file types
  - Should restrict access to non-ops users

---

## 2. Deployment Plan for Production Environment

To deploy the application to production, follow these steps:

### Application Packaging
- Containerize the app using **Docker**
- Serve using **Gunicorn + Uvicorn workers** for performance

### Environment Management
- Store sensitive data in a `.env` file or cloud secrets manager
- Ensure `SECRET_KEY` and `FERNET_KEY` are securely managed

### Database
- Replace in-memory storage with a real database (e.g., PostgreSQL or MongoDB)
- Add persistence for user and file metadata

### Hosting Options
- Use one of the following platforms:
  - **Render.com** (simple for FastAPI)
  - **AWS EC2 / Lightsail** for manual control

### SSL & Security
- Enable HTTPS
- Add CORS policy for frontend domains
- Secure file uploads and ensure tokens are time-limited


---

![Image](https://github.com/user-attachments/assets/d32181ea-fca4-4394-a0df-4b48a9446d5b)
![Image](https://github.com/user-attachments/assets/a5e70b2c-4e9b-4cf2-9c3b-80616dc779e5)
![Image](https://github.com/user-attachments/assets/4707af9f-513b-4f79-8cc9-d321bfad976b)
![Image](https://github.com/user-attachments/assets/e7bfdda8-0e47-457e-bae9-bb31995714d7)
![Image](https://github.com/user-attachments/assets/96ec7a02-8725-47da-82d4-3d197482296f)


---


# Author

**Kartik Bhatnagar**  
B.Tech CS, NIET Greater Noida  
GitHub: (https://github.com/kartik989-max)
