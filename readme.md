# Consumer Financial Behavior & Risk Intelligence System

An end-to-end data science pipeline that analyzes customer financial behavior, predicts loan default risk using machine learning, and explains model decisions using SHAP interpretability.

The system integrates **SQL-based feature engineering**, **machine learning modeling**, and **explainable AI** to build a transparent financial risk prediction framework.

---

## 📌 Project Overview
Financial institutions must assess whether a customer is likely to default on a loan before issuing credit. Incorrect predictions can result in:
* **Financial losses** if risky customers receive loans.
* **Lost business opportunities** if safe customers are rejected.

**This project builds a financial risk intelligence system that:**
1.  Analyzes customer financial behavior.
2.  Predicts default probability using machine learning.
3.  Provides interpretable explanations for model decisions.

---

## 🖥️ Interactive Dashboard

An interactive dashboard was built using **Streamlit** to make the model accessible as a real-time risk assessment tool.

The dashboard allows users to:
- Explore financial behavior patterns
- Input customer financial details
- Predict default probability
- Visualize model performance
- Interpret predictions using SHAP explanations

Run the dashboard locally:

```bash
streamlit run streamlit_app.py
```
---

## ⚠️ Dataset Note
This project uses a **synthetic financial dataset** created to simulate customer behavior and credit risk patterns.

While the dataset enables demonstration of the complete ML pipeline (SQL feature engineering, model training, explainable AI, API deployment, and dashboard), real financial systems typically include additional behavioral variables such as payment history, credit utilization, and delinquency records.

Therefore, this project should be interpreted as a **demonstration of an end-to-end financial risk intelligence system architecture**, rather than a production-ready credit scoring model.

---

## ⚙️ System Architecture
The project follows a realistic data science pipeline similar to those used in financial institutions.

1.  **Raw Financial Data**
2.  **MySQL Database** (customers, transactions, loans)
3.  **SQL Feature Engineering**
4.  **Python Data Pipeline**
5.  **Machine Learning Models**
    * Logistic Regression
    * Random Forest
6.  **Class Imbalance Handling**
7.  **Hyperparameter Tuning** (GridSearchCV)
8.  **Threshold Optimization**
9.  **Model Evaluation** (ROC-AUC ≈ 0.864)
10. **Explainable AI** (SHAP)

> This workflow demonstrates a complete ML lifecycle from data storage to explainable predictions.

---

## 📊 Dataset & Feature Engineering
Customer financial data was stored in a **MySQL relational database** containing three primary tables:
* `customers`
* `transactions`
* `loans`

**SQL queries** were used to engineer behavioral features such as:
* Total transaction spending
* Average transaction value
* Number of loans
* Default history
* Loan-to-income ratio

These were aggregated into a customer-level feature table where each row represents one customer.

---

## 🤖 Machine Learning Models
Two models were implemented and compared:

### 1. Logistic Regression
* Baseline linear classifier.
* Balanced class weights to handle dataset imbalance.

### 2. Random Forest
* Non-linear ensemble model.
* Tuned using **GridSearchCV**.
* **Hyperparameter tuning** included optimization of:
    * Number of trees
    * Maximum tree depth
    * Minimum samples per split
    * Minimum samples per leaf

---

## ⚖️ Class Imbalance Handling
The dataset contains fewer default cases than non-default cases, which can bias models. To address this:
* **Balanced class weights** were used.
* Evaluation focused on **recall** and **ROC-AUC**.
* **Decision threshold tuning** was applied to control risk sensitivity.

---

## 📈 Model Performance
The tuned Random Forest model achieved:
> **ROC-AUC ≈ 0.864**

This means the model can correctly rank risky customers about 86% of the time, demonstrating strong discrimination capability for credit risk prediction.

**Evaluation methods included:**
* Confusion Matrix
* Classification Report
* ROC Curve
* Threshold Analysis

---

## 🔍 Model Interpretability (SHAP)
To ensure transparency, **SHAP (SHapley Additive Explanations)** was used to explain model predictions. SHAP analysis revealed the most important financial risk drivers.

### Key Risk Insights
The model identified several meaningful financial behavior patterns:
* **Loan-to-Income Ratio:** The strongest indicator of default risk.
* **Total Loan Amounts:** Customers with high total loan amounts have higher default probability.
* **Concurrent Loans:** Multiple active loans increase financial pressure.
* **Spending Habits:** High spending relative to income signals financial instability.
* **Stability Factors:** Higher income and credit score reduce default risk.

*These results indicate the model is learning real financial behavior patterns rather than random correlations.*

---

## 📁 Project Structure
```bash
financial-risk-intelligence/
│
├── data/               # Raw and processed data
├── notebooks/          # Jupyter Notebooks
│   └── Customer_features.ipynb
│   └── Full_production_pipeline_of_modelling.ipynb
│   └── Synthetic_dataset_generation.ipynb
├── sql/                # Database scripts
│   ├── database_schemas.sql
│   └── feature_engineering.sql
├── models/             # Saved model binaries
├── README.md           # Project documentation
└── requirements.txt    # Dependencies
```

🛠️ Technologies Used
Language: Python

ML Libraries: Scikit-learn, SHAP

Data Analysis: Pandas, NumPy

Visualization: Matplotlib, Seaborn

Database: MySQL

