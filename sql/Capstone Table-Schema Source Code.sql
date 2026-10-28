/*
Capstone Table-Schema Source Code.sql

Author: Abraham Horta

Purpose: This script file details the layout of the entire database schema/design.
It includes the table and column names, unique IDs, along with foreign keys and references.

Source: This code uses concepts and techniques that were learned and practiced in 
previous courses such as CSC-410- Database Management Systems, and were also influenced 
by the following source:
1. Silberschatz, A., Korth, H., & Sudarshan, S. Database System Concepts. https://www.mpgcamb.com/wp-content/uploads/2024/12/
Abraham-Silberschatz-Henry-F.-Korth-S.-Sudarshan-Database-System-Concepts-McGraw-Hill-Education-2019.pdf 

*/

use secure_api_db;

CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL UNIQUE,
    time_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    time_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE user_roles (
    user_id INT NOT NULL,
    role_id INT NOT NULL,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) 
        REFERENCES users(id)
        ON DELETE CASCADE,
    FOREIGN KEY (role_id) 
        REFERENCES roles(id)
        ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    amount DECIMAL(19,4) NOT NULL,
    currency CHAR(3) NOT NULL,
    transaction_status ENUM('Pending','Completed','Refunded','Failed') DEFAULT 'Pending',
    transaction_description TEXT,
    time_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    time_updated TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
    time_deleted TIMESTAMP NULL,
    FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE audit_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    action_type VARCHAR(100) NOT NULL,
    metadata JSON,
    ip_address VARCHAR(45),
    time_logged TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE RESTRICT
) ENGINE=InnoDB;

/*show tables;
SELECT 
    TABLE_NAME,
    CONSTRAINT_NAME,
    REFERENCED_TABLE_NAME
FROM information_schema.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = 'secure_api_db'
AND REFERENCED_TABLE_NAME IS NOT NULL;
*/

/*CREATE INDEX idx_user_roles_user ON user_roles(user_id);
CREATE INDEX idx_user_roles_role ON user_roles(role_id);
CREATE INDEX idx_transactions_user ON transactions(user_id);
CREATE INDEX idx_audit_log_user ON audit_log(user_id);
*/
# To reinsert the test user for password hashing
UPDATE users
SET password_hash = '$2b$12$IvHK0S9HlLQ9h2myAs6aeuL6ZKm8E.GLnSbfxVszCvSVhzM5gNlwW'
WHERE username = 'Dash';
