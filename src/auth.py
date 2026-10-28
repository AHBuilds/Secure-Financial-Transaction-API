'''
    auth.py

    Author: Abraham Horta

    Purpose: This file handles all security-related functions for the application,
    which includes password hashing with bcrypt, password verification during login,
    JWT token creation, and token validation for protected routes. In addition,
    It serves as the main security layer for authentication and authorization.

    Sources: The following code was inspired/influenced by the following
    -- sources, but adapted and altered for the API project.

    1. https://www.geeksforgeeks.org/python/authentication-and-authorization-with-fastapi/
    2. https://www.youtube.com/watch?v=gbk6SsxZVG8
    3. https://www.youtube.com/watch?v=0A_GCXBCNUQ
    4. https://medium.com/@hadiyolworld007/how-i-built-a-secure-jwt-auth-system-in-just-20-minutes-0d2ae5d0a5ad
    5. https://medium.com/@dasunjayassri/implementing-bcrypt-password-verification-in-python-a76aeff74438

'''

from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext

# -- Password Hashing(Using bcrypt)
password_context = CryptContext(
   schemes = ["bcrypt"],
   deprecated = "auto"
)

# -- Hashing Helper Functions
def to_secure_password(password: str):
   return password_context.hash(password)

def to_validate_secure_password(plaintext: str, ciphertext: str):
   return password_context.verify(plaintext, ciphertext)

security = HTTPBearer()
SECRET_KEY = "thisisthetemporarysecretkey" # -- Password was masked in the source code submission for security practices.
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRATION_IN = 30 # --(in minutes)

# -- Function for Token Creation
def create_access_token(data: dict):
   to_encode = data.copy()
   expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRATION_IN)
   to_encode.update({"exp": expire})

   return jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)

# -- Token Verification Function
def get_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
   token = credentials.credentials

   try:
       payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
       return payload # -- contains user_id and username

   except JWTError:
       raise HTTPException(status_code = 401, detail = "Invalid or expired token")


