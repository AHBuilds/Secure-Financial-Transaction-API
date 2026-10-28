'''
   models.py

   Author: Abraham Horta

   Purpose: This file contains all Pydantic models used for request validation throughout the API.
   These models make sure that user input for registration, login, transaction creation, and
   transaction updates follow the correct structure before being processed by the system.

   Source(s): The following code was inspired/influenced by the following
    -- source(s), but adapted and altered for the API project.
   1. https://www.geeksforgeeks.org/python/authentication-and-authorization-with-fastapi/

'''

from pydantic import BaseModel

# -- Register User Request Model
class RegisterUserRequest(BaseModel):
   username: str
   email: str
   password: str

# -- User Login Request Model
class LoginRequest(BaseModel):
   username: str
   password: str

# -- Request Transaction Model
class TransactionRequest(BaseModel):
   #user_id: int
   amount: float
   currency: str
   description: str

# -- Update Request Model
class UpdateRequest(BaseModel):
   #user_id: int
   transaction_id: int
   new_status: str