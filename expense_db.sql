--   SMART EXPENSE MANAGER —

-- 1. Create & use database
CREATE DATABASE IF NOT EXISTS expense_db;
USE expense_db;

-- 2. CREATE TABLES
CREATE TABLE IF NOT EXISTS users (
    user_id  INT          PRIMARY KEY AUTO_INCREMENT,
    name     VARCHAR(50)  NOT NULL,
    email    VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS expenses (
    exp_id      INT           PRIMARY KEY AUTO_INCREMENT,
    user_id     INT           NOT NULL,
    amount      FLOAT         NOT NULL,
    category    VARCHAR(50)   NOT NULL,
    description VARCHAR(100),
    date        DATE          NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE
);

-- 4. VIEW
CREATE VIEW expenses_view AS SELECT exp_id, user_id, amount, category, description, date FROM expenses;

SELECT * FROM expenses_view;