'''
    transaction_routes.py

    Author: Abraham Horta

    Purpose: This file manages all financial transaction operations, including transaction creation
    and transaction status updates. It enforces business rules, uses stored procedures for secure
    database operations, and applies rollback protection when invalid transaction state changes are attempted.

    Sources: The following code was inspired/influenced by the following
    -- sources, but adapted and altered for the API project.

    1. https://www.youtube.com/watch?v=gbk6SsxZVG8
    2. https://www.youtube.com/watch?v=0A_GCXBCNUQ
    3. https://blogs.oracle.com/mysql/how-to-setup-fastapi-with-mysql-heatwave-and-post-the-data#:~:text=%5Bopc@api%20~%5D$%20cat%20my_fastapi,Output:
    4. https://medium.com/@parth.khajgiwale/building-a-crud-api-with-fastapi-mysql-and-postman-8e849e62d9fe
'''

from fastapi import APIRouter, Depends
from database import get_db_connection
from models import TransactionRequest, UpdateRequest
from auth import get_user

router = APIRouter()

# -- Endpoint To Create Transactions
@router.post("/create_transaction")
def create_transaction(
   request: TransactionRequest,
   user = Depends(get_user)
):
   conn = get_db_connection()
   cursor = conn.cursor()

   try:
       cursor.callproc("create_transaction", [
           user["user_id"], # Now from JWT
           request.amount,
           request.currency,
           request.description,
           "127.0.0.1"
       ])
       conn.commit()
       return {"Message": "Transaction has been created successfully"}

   except Exception as e:
       conn.rollback()
       return {"Error": str(e)}

   finally:
       cursor.close()
       conn.close()

# -- Endpoint To Update Transactions
@router.post("/update_transaction")
def update_transaction(
   request: UpdateRequest,
   user = Depends(get_user)
):
   conn = get_db_connection()
   cursor = conn.cursor()

   try:
       cursor.callproc("update_transaction_status", [
           user["user_id"], # Now from JWT
           request.transaction_id,
           request.new_status
       ])
       # check for returned result sets(error messages from db)
       for results in cursor.stored_results():
           error_message = results.fetchone()
           if error_message:
               conn.rollback()
               return {"Error": error_message[0]}

       conn.commit()
       return {"Message": "Transaction has been updated successfully"}

   except Exception as e:
       conn.rollback()
       return {"Error": str(e)}

   finally:
       cursor.close()
       conn.close()