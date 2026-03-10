from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI()

model = joblib.load("risk_model.pkl")

feature_order = [
"Age",
"Income",
"Credit_score",
"transaction_count",
"total_spending",
"avg_transaction_value",
"total_loans",
"total_loan_amount",
"spending_income_ratio",
"loan_income_ratio",
"transaction_income_ratio"
]

@app.post("/predict")
def predict(data: dict):

    age = data["Age"]
    income = data["Income"]
    credit_score = data["Credit_score"]
    loan_amount = data["total_loan_amount"]
    total_loans = data["total_loans"]
    spending = data["total_spending"]

    transaction_count = data.get("transaction_count",0)
    avg_transaction_value = data.get("avg_transaction_value",0)

    # Derived features
    spending_income_ratio = spending / income
    loan_income_ratio = loan_amount / income
    transaction_income_ratio = transaction_count / income

    df = pd.DataFrame([{
        "Age": age,
        "Income": income,
        "Credit_score": credit_score,
        "transaction_count": transaction_count,
        "total_spending": spending,
        "avg_transaction_value": avg_transaction_value,
        "total_loans": total_loans,
        "total_loan_amount": loan_amount,
        "spending_income_ratio": spending_income_ratio,
        "loan_income_ratio": loan_income_ratio,
        "transaction_income_ratio": transaction_income_ratio
    }])

    df = df[feature_order]

    prob = model.predict_proba(df)[0][1]

    return {
        "default_probability": float(prob),
        "risk_level": "High Risk" if prob > 0.35 else "Medium Risk" if prob > 0.25 else "Low Risk"
    }