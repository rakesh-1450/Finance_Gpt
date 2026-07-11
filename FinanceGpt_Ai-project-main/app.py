import streamlit as st
import pandas as pd
import numpy as np
import os
from utils.data_loader import load_csv
from utils.visualization import plot_expenses_pie, plot_stock_trend
from predict import make_prediction
from chatbot import ask_finance_bot
from utils.helpers import update_env_file, logger

# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="Finance GPT AI",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Sidebar ---
st.sidebar.title("💰 Finance GPT AI")
st.sidebar.markdown("Welcome to your personal AI financial assistant and dashboard.")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigate", [
    "Dashboard", 
    "Expense Tracker", 
    "Expense Suggestions",
    "Budget Planner",
    "Stock Predictor", 
    "Investment Basics",
    "Finance Education",
    "AI Assistant",
    "Settings"
])

st.sidebar.markdown("---")

# --- Page: Dashboard ---
if page == "Dashboard":
    st.title("📊 Financial Overview")
    st.markdown("A high-level view of your financial health.")
    
    # Load Finance Data
    df = load_csv("datasets/finance_data.csv")
    
    if df is not None:
        st.subheader("Monthly Income vs Savings")
        st.dataframe(df.style.format({"Income": "${:.2f}", "Savings": "${:.2f}"}), use_container_width=True)
        st.bar_chart(df.set_index("Month")[["Income", "Savings"]])
    else:
        st.warning("No finance data found. Please run `generate_data.py` to create the mock datasets.")

# --- Page: Expense Tracker ---
elif page == "Expense Tracker":
    st.title("💸 Expense Tracker")
    st.markdown("Analyze where your money is going.")
    
    df = load_csv("datasets/expenses.csv")
    
    if df is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Raw Data")
            st.dataframe(df, use_container_width=True)
            
        with col2:
            st.subheader("Expense Distribution")
            fig = plot_expenses_pie(df)
            if fig:
                st.pyplot(fig)
    else:
        st.warning("No expense data found. Please run `generate_data.py`.")

# --- Page: Expense Suggestions ---
elif page == "Expense Suggestions":
    st.title("💡 Expense Suggestions")
    st.markdown("Automated insights to help you save money.")
    
    df = load_csv("datasets/expenses.csv")
    if df is not None:
        category_totals = df.groupby('Category')['Amount'].sum().sort_values(ascending=False)
        st.subheader("Your Top Expenses")
        st.bar_chart(category_totals)
        
        st.subheader("Smart Insights")
        # Simple rule-based suggestions
        if "Subscriptions" in category_totals and category_totals["Subscriptions"] > 500:
            st.warning("⚠️ **High Subscription Costs:** You spent over $500 on subscriptions this year. Consider canceling unused streaming services or magazines.")
        
        if "Food" in category_totals and category_totals["Food"] > 5000:
            st.info("🍔 **Dining Out:** Your food expenses are high. Try meal prepping on weekends to cut costs by up to 30%.")
            
        st.success("✅ **Tip:** The AI Assistant can analyze these specific categories for you if you ask it!")
    else:
        st.warning("No expense data found.")

# --- Page: Budget Planner ---
elif page == "Budget Planner":
    st.title("📝 Budget Planner (50/30/20 Rule)")
    st.markdown("Calculate your ideal budget breakdown based on your monthly income.")
    
    income = st.number_input("Enter your Monthly After-Tax Income ($)", min_value=0.0, value=5000.0, step=100.0)
    
    if income > 0:
        needs = income * 0.50
        wants = income * 0.30
        savings = income * 0.20
        
        col1, col2, col3 = st.columns(3)
        col1.metric("🏠 Needs (50%)", f"${needs:,.2f}", "Rent, Groceries, Bills")
        col2.metric("🎉 Wants (30%)", f"${wants:,.2f}", "Dining, Entertainment")
        col3.metric("🏦 Savings/Debt (20%)", f"${savings:,.2f}", "Investments, Emergency")
        
        # Visualize it
        st.subheader("Budget Breakdown")
        budget_df = pd.DataFrame({
            "Category": ["Needs", "Wants", "Savings"],
            "Amount": [needs, wants, savings]
        }).set_index("Category")
        st.bar_chart(budget_df)

# --- Page: Stock Predictor ---
elif page == "Stock Predictor":
    st.title("📈 Stock Price Predictor")
    st.markdown("Use Machine Learning (Random Forest) to predict future closing prices based on today's metrics.")
    
    df = load_csv("datasets/stock_prices.csv")
    if df is not None:
        with st.expander("View Historical Stock Trend"):
            fig = plot_stock_trend(df)
            if fig:
                st.pyplot(fig)
                
    st.markdown("---")
    st.subheader("Predict Future Price")
    
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        with col1:
            open_p = st.number_input("Open Price ($)", min_value=0.0, value=150.0, step=0.5)
            high_p = st.number_input("High Price ($)", min_value=0.0, value=155.0, step=0.5)
        with col2:
            low_p = st.number_input("Low Price ($)", min_value=0.0, value=148.0, step=0.5)
            volume = st.number_input("Trading Volume", min_value=0, value=1000000, step=10000)
            
        submit_btn = st.form_submit_button("Predict Closing Price")
        
    if submit_btn:
        with st.spinner("AI is calculating..."):
            pred = make_prediction(open_p, high_p, low_p, volume)
            if pred:
                st.success(f"### Predicted Closing Price: ${pred:.2f}")
            else:
                st.error("Prediction failed. Ensure the model is trained (`train.py`).")

# --- Page: Investment Basics ---
elif page == "Investment Basics":
    st.title("🌱 Investment Basics: Compound Interest")
    st.markdown("See how your money grows over time with the power of compound interest.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        principal = st.number_input("Initial Investment ($)", min_value=0, value=1000, step=100)
    with col2:
        monthly_contribution = st.number_input("Monthly Contribution ($)", min_value=0, value=100, step=50)
    with col3:
        years = st.slider("Years to Grow", min_value=1, max_value=40, value=10)
        
    rate = st.slider("Estimated Annual Return (%)", min_value=1.0, max_value=15.0, value=7.0, step=0.5)
    
    # Calculate Compound Interest
    months = years * 12
    monthly_rate = (rate / 100) / 12
    
    balances = []
    current_balance = principal
    
    for i in range(months + 1):
        if i > 0:
            current_balance = (current_balance + monthly_contribution) * (1 + monthly_rate)
        if i % 12 == 0:
            balances.append(current_balance)
            
    st.subheader(f"Total after {years} years: ${balances[-1]:,.2f}")
    
    # Plot it
    growth_df = pd.DataFrame({
        "Year": range(years + 1),
        "Balance": balances
    }).set_index("Year")
    
    st.line_chart(growth_df)

# --- Page: Finance Education ---
elif page == "Finance Education":
    st.title("📚 Finance Education")
    st.markdown("Read through our AI-curated finance guides.")
    
    df = load_csv("datasets/finance_guides.csv")
    if df is not None:
        for index, row in df.iterrows():
            with st.expander(f"{row['Topic']} (Level: {row['Difficulty']})"):
                st.write(row['Content'])
    else:
        st.warning("No finance guides found. Please run `generate_data.py`.")

# --- Page: AI Assistant ---
elif page == "AI Assistant":
    st.title("🤖 Finance GPT AI Assistant")
    st.markdown("Ask our expert AI about budgeting, saving, and investing.")
    
    # Initialize chat history in session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Ask me about personal finance..."):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.spinner("Thinking..."):
            response = ask_finance_bot(prompt)
            
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# --- Page: Settings ---
elif page == "Settings":
    st.title("⚙️ Settings & API Keys")
    st.markdown("Manage your API keys here securely. This updates your `.env` file directly.")
    
    # Load current Gemini key for placeholder
    current_gemini = os.getenv("GEMINI_API_KEY", "")
    
    with st.form("api_key_form"):
        gemini_key = st.text_input("Gemini API Key", value=current_gemini, type="password")
        
        save_btn = st.form_submit_button("Save Key")
        
    if save_btn:
        with st.spinner("Saving to .env..."):
            try:
                update_env_file("GEMINI_API_KEY", gemini_key)
                st.success("Gemini API Key successfully saved! You can now use the AI Assistant.")
            except Exception as e:
                logger.error(f"Failed to update API key: {e}")
                st.error(f"Failed to save API key: {e}")
