'''
    database.py

    Author: Abraham Horta

    Purpose: This file manages the MySQL database connection for the Secure Transactional API system.
    It provides a centralized and reusable connection function that's used by all modules for secure access
    to user data, transaction records, audit logs, and role management.

    Source(s): The following code was inspired/influenced by the following
    -- source(s), but adapted and altered for the API project.

    1. YT Tutorial: https://www.youtube.com/watch?v=gbk6SsxZVG8

'''

import mysql.connector

# Database Connection
def get_db_connection():
   return mysql.connector.connect(
       host = "localhost",
       user = "root",
       password = "Your_DB_Password", # -- Password was masked in the source code submission for security practices.
       database = "secure_api_db"
   )
