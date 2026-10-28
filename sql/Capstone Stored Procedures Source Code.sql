/*
Capstone Stored Procedures Source Code.sql

Author: Abraham Horta
  
Purpose: This file deals with the stored procedures and all of the actions
that go in the database. It also includes test data/insert data that was used to test
the DB functions.

Source: This code uses concepts and techniques that were learned and practiced in 
previous courses such as CSC-410- Database Management Systems, and were also influenced 
by the following source:
1. Silberschatz, A., Korth, H., & Sudarshan, S. Database System Concepts. https://www.mpgcamb.com/wp-content/uploads/2024/12/
Abraham-Silberschatz-Henry-F.-Korth-S.-Sudarshan-Database-System-Concepts-McGraw-Hill-Education-2019.pdf 

*/
use secure_api_db;
DELIMITER $$

CREATE PROCEDURE create_transaction (
    IN p_user_id INT,
    IN p_amount DECIMAL(19,4),
    IN p_currency CHAR(3),
    IN p_description TEXT,
    IN p_ip VARCHAR(45)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT "The transaction failed and was rolled back." AS error_message;

    END;

    START TRANSACTION;

    # -- Insert transaction as PENDING
    INSERT INTO transactions (
        user_id,
        amount,
        currency,
        transaction_status,
        transaction_description,
        time_created
    )
    VALUES (
        p_user_id,
        p_amount,
        p_currency,
        'Pending',
        p_description,
        NOW()
    );

    # -- Log the action
    INSERT INTO audit_log (
        user_id,
        action_type,
        metadata,
        ip_address,
        time_logged
    )
    VALUES (
        p_user_id,
        'CREATE_TRANSACTION',
        JSON_OBJECT(
            'amount', p_amount,
            'currency', p_currency,
            'status', 'Pending'
        ),
        p_ip,
        NOW()
    );

    COMMIT;
END $$

DELIMITER ;
/*# To test Procedure:
INSERT INTO users (username, email, password_hash)
VALUES ('Dash', 'dash@testrun.com', 'testhash');
select * from users;
# CALL create_transaction( 2, 250.00, 'USD', 'Test payment', '127.0.0.1' );
CALL create_transaction(1, 250.00, 'USD', 'Test payment', '127.0.0.1'); 
select * from transactions;
select * from audit_log;
*/

INSERT INTO roles (role_name)
VALUES 
('Admin'),
('Support'),
('Customer');

INSERT INTO user_roles (user_id, role_id)
VALUES (1, 1);

DELIMITER $$

CREATE PROCEDURE update_transaction_status (
    IN p_user_id INT,
    IN p_transaction_id INT,
    IN p_new_status VARCHAR(20)
)
BEGIN
    DECLARE v_role_count INT DEFAULT 0;
    DECLARE v_current_status VARCHAR(20);
    DECLARE v_exists INT DEFAULT 0;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 'Error occurred: The transaction has failed and was rolled back.' AS message;
    END;

    START TRANSACTION;

    # -- Check if transaction exists
    SELECT COUNT(*)
    INTO v_exists
    FROM transactions
    WHERE id = p_transaction_id;

    IF v_exists = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'The transaction does not exist';
    END IF;

    # --  Get current transaction status
    SELECT transaction_status
    INTO v_current_status
    FROM transactions
    WHERE id = p_transaction_id;

    # -- Validate new transaction status
    IF p_new_status NOT IN ('Pending','Completed','Refunded','Failed') THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid status value';
    END IF;

    # -- RBAC check (Admin or Support only)
    SELECT COUNT(*)
    INTO v_role_count
    FROM user_roles ur
    JOIN roles r ON ur.role_id = r.id
    WHERE ur.user_id = p_user_id
    AND r.role_name IN ('Admin', 'Support');

    IF v_role_count = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'You are not authorized to proceed with this action.';
    END IF;

    # -- To enforce valid transitions
    IF NOT (
        (v_current_status = 'Pending' AND p_new_status IN ('Completed','Failed')) OR
        (v_current_status = 'Completed' AND p_new_status = 'Refunded')
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid status transition';
    END IF;

    # -- Update transactions
    UPDATE transactions
    SET transaction_status = p_new_status,
        time_updated = NOW()
    WHERE id = p_transaction_id;

    # -- Log actions
    INSERT INTO audit_log (
        user_id,
        action_type,
        metadata,
        ip_address,
        time_logged
    )
    VALUES (
        p_user_id,
        'Update_Transaction_Status',
        JSON_OBJECT(
            'transaction_id', p_transaction_id,
            'old_status', v_current_status,
            'new_status', p_new_status
        ),
        'SYSTEM',
        NOW()
    );

    COMMIT;
END $$

DELIMITER ;

/*# Pending to Completed
CALL update_transaction_status(1, 2, 'Completed');
# Completed to Refunded
CALL update_transaction_status(1, 2, 'Refunded');
# Invalid status
CALL update_transaction_status(1, 2, 'RandomValue');
# Invalid transition
CALL update_transaction_status(1, 2, 'Pending');
# Customer trying to update
CALL update_transaction_status(3, 2, 'Completed');
*/




