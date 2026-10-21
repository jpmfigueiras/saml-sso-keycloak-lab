-- Create database
CREATE DATABASE IF NOT EXISTS gid;
USE gid;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    email VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    app_name VARCHAR(255) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    role VARCHAR(50) NOT NULL DEFAULT 'user',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (username, app_name),
    INDEX idx_email (email),
    INDEX idx_role (role)
);
