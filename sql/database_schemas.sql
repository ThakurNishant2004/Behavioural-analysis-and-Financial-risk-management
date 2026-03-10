
CREATE DATABASE IF NOT EXISTS financial_risk_system;
USE financial_risk_system;


CREATE TABLE customers (
    Customer_id INT PRIMARY KEY,
    Age INT,
    Income FLOAT,
    Employment_type VARCHAR(50),
    City VARCHAR(50),
    Credit_score INT
);


CREATE TABLE transactions (
    Transaction_id INT PRIMARY KEY,
    Customer_id INT,
    Transaction_date DATE,
    Amount FLOAT,
    Category VARCHAR(50),
    Merchant VARCHAR(100),

    FOREIGN KEY (Customer_id)
    REFERENCES customers(Customer_id)
);


CREATE TABLE loans (
    Loan_id INT PRIMARY KEY,
    Customer_id INT,
    Loan_amount FLOAT,
    Interest_rate FLOAT,
    EMI FLOAT,
    Default_flag INT,

    FOREIGN KEY (Customer_id)
    REFERENCES customers(Customer_id)
);