import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Enhanced CSS for "Glassmorphism" and high contrast
# --- CONFIG & STYLING ---
st.set_page_config(
    page_title="FinRisk Intelligence",
    page_icon="🛡️",
    layout="wide"
)

# Enhanced CSS: Dark Main Body + Solid White Sidebar
st.markdown("""
    <style>
    /* 1. Header & Decoration */
    header[data-testid="stHeader"] {
        background: rgba(0,0,0,0) !important;
    }
    div[data-testid="stDecoration"] {
        display: none !important;
    }
    footer {visibility: hidden;}

    /* 2. Main App Background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    }

    /* 3. FIX: Target specific Widget Labels & Slider Values */
    /* Targeting the 'st-at' class which Streamlit uses for input labels */
    .stMarkdown, p, span, label, h1, h2, h3, .stMetric div, 
    [data-testid="stWidgetLabel"] p,
    .st-at, .st-ae, .st-af, .st-ag,
    div[data-testid="stThumbValue"], 
    div[data-testid="stTickBarMin"], 
    div[data-testid="stTickBarMax"] {
        color: white !important;
    }

    /* 4. SIDEBAR - Forced White Background */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        opacity: 1 !important;
    }

    /* 5. SIDEBAR TEXT - Forced Dark for visibility */
    [data-testid="stSidebar"] .stMarkdown, 
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
    [data-testid="stSidebar"] .st-at {
        color: #1e1e1e !important;
    }

    /* 6. Input Fields - Ensuring text inside boxes is also visible */

    div[data-baseweb="input"] input {
        color: #1e1e1e !important;   /* dark text so it is visible on light field */
        background-color: #ffffff !important;
    }

    div[data-baseweb="input"] {
        background-color: #ffffff !important;
    }

    /* Fix placeholder visibility */
    div[data-baseweb="input"] input::placeholder {
        color: #666666 !important;
    }
    /* 7. Metric Cards */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.07);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* 8. Animated Button */
    .stButton>button {
        background: linear-gradient(45deg, #00dbde 0%, #fc00ff 100%);
        color: white !important;
        border: none;
        width: 100%;
        border-radius: 10px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    # Using a clean logo from URL or local asset
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135706.png", width=80)
    st.title("FinRisk AI")
    page = st.radio(
        "Navigation",
        ["📈 Overview", "🔍 Risk Prediction", "🎯 Model Performance", "🧠 Explainable AI"]
    )
    st.divider()
    st.info("System Status: Active")

# --------------------------------------------------
# OVERVIEW PAGE
# --------------------------------------------------
if "Overview" in page:
    st.title("📊 Financial Behaviour Overview")
    df = pd.read_csv("notebook/customer_features.csv")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Customers", f"{len(df):,}", delta="Live Data")
    with col2:
        st.metric("Default Rate", f"{df['default_flag'].mean()*100:.2f}%", delta="-0.5%", delta_color="inverse")
    with col3:
        st.metric("Average Income", f"₹{df['Income'].mean():,.0f}")

    st.markdown("### Market Distribution Analysis")
    col_a, col_b = st.columns(2)
    
    fig1 = px.histogram(df, x="loan_income_ratio", nbins=40, title="Loan-Income Ratio Distribution",
                       template="plotly_dark", color_discrete_sequence=['#00dbde'])
    
    fig2 = px.scatter(df, x="Income", y="total_loan_amount", color="default_flag", 
                     title="Income vs Loan Amount", template="plotly_dark", color_continuous_scale="RdYlGn_r")

    # Shared formatting for dark charts
    for f in [fig1, fig2]:
        f.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="white")
        )

    col_a.plotly_chart(fig1, use_container_width=True)
    col_b.plotly_chart(fig2, use_container_width=True)

# --------------------------------------------------
# RISK PREDICTION PAGE
# --------------------------------------------------
if "Risk Prediction" in page:
    st.title("🔍 Precision Risk Assessment")
    
    main_col1, main_col2 = st.columns([1.2, 1], gap="large")

    with main_col1:
        st.markdown("#### 📝 Financial Profile")
        with st.container():
            c1, c2 = st.columns(2)
            with c1:
                age = st.number_input("Age", 18, 80, 30)
                income = st.number_input("Annual Income (₹)", min_value=0, value=500000)
                credit_score = st.slider("Credit Score", 300, 850, 650)
            with c2:
                loan_amount = st.number_input("Total Loan Amount (₹)", min_value=0, value=100000)
                total_loans = st.number_input("Active Loans Count", 0, 20, 1)
                spending = st.number_input("Monthly Spending (₹)", min_value=0, value=20000)

            with st.expander("Additional Transactional Details"):
                cx, cy = st.columns(2)
                transactions = cx.number_input("Transaction Count", 0, 1000, 50)
                avg_txn = cy.number_input("Avg Transaction Value (₹)", 0, 100000, 2000)

            st.markdown("<br>", unsafe_allow_html=True)
            predict_btn = st.button("RUN AI RISK ANALYSIS")

    with main_col2:
        st.markdown("#### 🛡️ AI Risk Verdict")

        if predict_btn:
            payload = {
                "Age": age, "Income": income, "Credit_score": credit_score,
                "transaction_count": transactions, "avg_transaction_value": avg_txn,
                "total_loans": total_loans, "total_loan_amount": loan_amount, "total_spending": spending
            }

            try:
                response = requests.post("https://behavioural-analysis-and-financial-risk.onrender.com/predict", json=payload)
                if response.status_code == 200:
                    prob = response.json()["default_probability"]
                    
                    # Modern score display
                    if prob > 0.35:
                        color = "#ff4b4b"
                        status = "⚠️ HIGH RISK"
                    elif prob > 0.25:
                        color = "#ffa500"
                        status = "🟠 MEDIUM RISK"
                    else:
                        color = "#00ffcc"
                        status = "✅ LOW RISK"
                    
                    st.markdown(f"<h1 style='text-align: center; color: {color};'>{prob:.1%}</h1>", unsafe_allow_html=True)
                    st.write(f"**Verdict:** {status}")

                    # Gauge Chart
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=prob,
                        gauge={
                            'axis': {'range': [0, 1], 'tickcolor': "white"},
                            'bar': {'color': "white"},
                            'steps': [
                                {'range': [0, 0.25], 'color': "#00ffcc"},
                                {'range': [0.25, 0.45], 'color': "#ffa500"},
                                {'range': [0.45, 1], 'color': "#ff4b4b"}
                            ],
                        }
                    ))
                    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, height=280)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.error(f"API Error: {response.status_code}")
            except Exception as e:
                st.error("Connection failed. Check if API is awake.")
        else:
            st.info("Enter customer details and click 'Analyze Risk' to generate a report.")

# --------------------------------------------------
# MODEL PERFORMANCE PAGE
# --------------------------------------------------
if "Model Performance" in page:
    st.title("🎯 Model Intelligence Metrics")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("ROC AUC", "0.864", "+2.1%")
    m2.metric("Accuracy", "90%", "+1.2%")
    m3.metric("Recall", "91%", "-0.4%")

    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.image("assets/roc_curve.png", caption="ROC Curve Performance")
    with col2:
        st.image("assets/confusion_matrix.png", caption="Error Analysis (Confusion Matrix)")

# --------------------------------------------------
# EXPLAINABLE AI PAGE
# --------------------------------------------------
if "Explainable AI" in page:
    st.title("🧠 Feature Attribution (SHAP)")
    
    st.markdown("""
    ### Why did the model make this decision?
    The system utilizes **SHAP (SHapley Additive exPlanations)** to break down individual feature contributions.
    """)
    
    # Feature explanation cards
    st.image("assets/shap_summary.png", use_container_width=True)
    
    with st.expander("Detailed Feature Impact Guide"):
        st.write("""
        - **Loan-to-Income Ratio:** High ratios are the #1 predictor of default.
        - **Credit Score:** Lower scores show strong negative correlation with repayment.
        - **Spending Habits:** Anomalous spikes in spending relative to income signal risk.
        """)




