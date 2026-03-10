USE financial_risk_system ;

-- total spending per customer 
-- Customer who spend more than their income may show financial stress 
SELECT
Customer_id,SUM(Amount) as total_spending
FROM transactions GROUP BY Customer_id 
ORDER BY total_spending DESC ;

-- Avearge Transaction Size 
SELECT 
customer_id,
AVG(Amount) AS avg_transaction
FROM transactions
group by Customer_id
order by avg_transaction DESC ;

-- Transaction frequency 
Select customer_id,
COUNT(*) AS transaction_count 
FROM transactions 
GROUP BY customer_id 
order by transaction_count DESC ;

-- Monthly Spending Trend
SELECT
customer_id,
DATE_FORMAT(Transaction_date,'%Y-%m') AS month,
SUM(Amount) as monthly_spending
FROM transactions
GROUP BY customer_id, month
ORDER BY customer_id;

-- Spending by category
SELECT 
Category,
SUM(Amount) as total_spent
FROM transactions 
group by Category
order by total_spent DESC ;

-- Default rate analysis 
Select 
count(*) as total_loans,
sum(Default_flag) as total_defaults,
(sum(Default_flag)/count(*))*100 as default_rate
From loans ;

-- Average credit score of defaulters 
select
avg(c.Credit_score) as Avg_credi_score
from customers c 
join loans l
on c.Customer_id = l.Customer_id
where l.Default_flag=1;

-- Debt to income ratio --> High debt compared to income is a strong indicator of financial risk.
Select c.Customer_id ,
sum(l.Loan_amount) / c.Income as debt_income_ratio
from customers c
join loans l 
on c.Customer_id = l.Customer_id
Group BY c.Customer_id;

-- Default label (Target Variable)
Select Customer_id,
MAX(Default_flag) as default_flag 
from loans
group by Customer_id ;

-- Default count 
Select Customer_id,
SUM(Default_flag) as default_flag 
from loans
group by Customer_id
order by Default_flag DESC;

-- customer-level feature table
CREATE TABLE Customer_features AS
SELECT 
    c.Customer_id,
    c.Age,
    c.Income,
    c.Credit_score,

    COUNT(DISTINCT t.Transaction_id) AS transaction_count,

    COALESCE(SUM(t.Amount),0) AS total_spending,
    COALESCE(AVG(t.Amount),0) AS avg_transaction_value,

    COALESCE(COUNT(DISTINCT l.Loan_id),0) AS total_loans,
    COALESCE(SUM(l.Default_flag),0) AS total_defaults,
    COALESCE(SUM(l.Loan_amount),0) AS total_loan_amount,

    COALESCE(SUM(l.default_flag) / NULLIF(COUNT(DISTINCT l.loan_id),0),0) AS default_rate,

    COALESCE(MAX(l.Default_flag),0) AS default_flag

FROM customers c

LEFT JOIN transactions t 
ON c.Customer_id = t.Customer_id

LEFT JOIN loans l
ON c.Customer_id = l.Customer_id

GROUP BY 
c.Customer_id,
c.Age,
c.Income,
c.Credit_score;
