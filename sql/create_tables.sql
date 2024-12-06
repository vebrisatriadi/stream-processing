CREATE TABLE users (
    user_id UUID PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    age INT,
    income DECIMAL(10, 2),
    created_at TIMESTAMP
);

-- Create processed users table
CREATE TABLE processed_users (
    user_id UUID PRIMARY KEY,
    name VARCHAR(100),
    income_category VARCHAR(20)
);

-- Create index for performance
CREATE INDEX idx_users_income ON users(income);
CREATE INDEX idx_processed_users_category ON processed_users(income_category);