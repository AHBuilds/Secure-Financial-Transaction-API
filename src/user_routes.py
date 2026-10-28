'''
    user_routes.py

    Author: Abraham Horta

    Purpose: This file manages user registration and login functionality for the Secure Transactional
    API system. It handles duplicate user checks, secure password hashing, default role assignment,
    password verification, and JWT token generation after successful authentication.

    Sources: The following code was inspired/influenced by the following
    -- sources, but adapted and altered for the API project.

    1. https://www.youtube.com/watch?v=gbk6SsxZVG8
    2. https://www.youtube.com/watch?v=0A_GCXBCNUQ
    3. https://blogs.oracle.com/mysql/how-to-setup-fastapi-with-mysql-heatwave-and-post-the-data#:~:text=%5Bopc@api%20~%5D$%20cat%20my_fastapi,Output:
    4. https://medium.com/@parth.khajgiwale/building-a-crud-api-with-fastapi-mysql-and-postman-8e849e62d9fe

'''

from fastapi import APIRouter, HTTPException
from database import get_db_connection
from models import RegisterUserRequest, LoginRequest
from auth import (
    to_secure_password,
    to_validate_secure_password,
    create_access_token
)

router = APIRouter()

# -- Registration Endpoint
@router.post("/register")
def register_user(request: RegisterUserRequest):
   conn = get_db_connection()
   cursor = conn.cursor()

   try:
       # -- Check to see if username/email is already being used
       cursor.execute(
           "SELECT id FROM users WHERE username = %s or email = %s",
           (request.username, request.email)
       )
       already_exists = cursor.fetchone()
       if already_exists:
           raise HTTPException(status_code = 400, detail = "Registration Failed")

       # -- Password hash
       ciphertext = to_secure_password(request.password)

       # -- Add user to DB
       cursor.execute(
           "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
           (request.username, request.email, ciphertext)
       )
       user_id = cursor.lastrowid

       # -- Default role assigned is customer (role_id for customer in DB is 3)
       cursor.execute(
           "INSERT INTO user_roles (user_id, role_id) VALUES (%s, %s)",
           (user_id, 3)
       )
       conn.commit()
       return {"Message": "User has been registered successfully"}

   except Exception as e:
       conn.rollback()
       return {"Error": str(e)}

   finally:
       cursor.close()
       conn.close()

# -- Endpoint For Logging In
@router.post("/login")
def login(request: LoginRequest):
   conn = get_db_connection()
   cursor = conn.cursor(dictionary = True)

   try:
       cursor.execute(
           "SELECT id, username, password_hash FROM users WHERE username = %s",
           (request.username,)
       )
       user = cursor.fetchone()

       if not user:
           raise HTTPException(status_code = 401, detail = "Invalid username and/or password")

       # -- Simple comparison(temporary)
       if not to_validate_secure_password(request.password, user["password_hash"]):
           raise HTTPException(status_code = 401, detail = "Invalid username and/or password")

       token = create_access_token({
           "user_id": user["id"],
           "username": user["username"]
       })
       return {"access_token": token}

   finally:
       cursor.close()
       conn.close()
