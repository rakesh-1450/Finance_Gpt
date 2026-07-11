import pandas as pd
import numpy as np
import os
from utils.helpers import ensure_directories, logger

def generate_mock_data():
    """
    As a trainer, I always tell my students: 'You can't do Data Science without Data!'
    This script generates realistic mock data for our Finance AI project.
    """
    ensure_directories()
    
    # 1. Generate Stock Prices Data
    logger.info("Generating stock prices data...")
    dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq='B') # Business days
    np.random.seed(42) # For reproducibility
    
    # Start with a base price and add random walk
    prices = 150 + np.cumsum(np.random.randn(len(dates)) * 2) 
    
    stock_df = pd.DataFrame({
        'Date': dates,
        'Open': prices + np.random.randn(len(dates)),
        'High': prices + np.random.rand(len(dates)) * 2,
        'Low': prices - np.random.rand(len(dates)) * 2,
        'Close': prices,
        'Volume': np.random.randint(1000000, 5000000, size=len(dates))
    })
    stock_df.to_csv("datasets/stock_prices.csv", index=False)
    logger.info("Saved datasets/stock_prices.csv")

    # 2. Generate Expenses Data
    logger.info("Generating expenses data...")
    expense_categories = ['Housing', 'Food', 'Transportation', 'Entertainment', 'Utilities', 'Subscriptions']
    expenses = []
    
    for month in range(1, 13):
        for category in expense_categories:
            amount = np.random.uniform(50, 1500)
            if category == 'Housing':
                amount = np.random.uniform(1000, 2500)
            elif category == 'Food':
                amount = np.random.uniform(300, 800)
            elif category == 'Subscriptions':
                amount = np.random.uniform(10, 100) # Good target for expense reduction suggestions
                
            expenses.append({
                'Date': f"2023-{month:02d}-01",
                'Category': category,
                'Amount': round(amount, 2)
            })
            
    expense_df = pd.DataFrame(expenses)
    expense_df.to_csv("datasets/expenses.csv", index=False)
    logger.info("Saved datasets/expenses.csv")
    
    # 3. Generate General Finance Data
    logger.info("Generating general finance data...")
    finance_df = pd.DataFrame({
        'Month': [f"2023-{m:02d}" for m in range(1, 13)],
        'Income': np.random.uniform(4000, 6000, size=12).round(2),
        'Savings': np.random.uniform(500, 1500, size=12).round(2)
    })
    finance_df.to_csv("datasets/finance_data.csv", index=False)
    logger.info("Saved datasets/finance_data.csv")
    
    # 4. Generate Finance Guides Data
    logger.info("Generating finance guides data...")
    guides_df = pd.DataFrame([
        {"Topic": "Emergency Funds", "Difficulty": "Beginner", "Content": "An emergency fund is a bank account with money set aside to pay for large, unexpected expenses. Rule of thumb: save 3-6 months of expenses."},
        {"Topic": "The 50/30/20 Rule", "Difficulty": "Beginner", "Content": "A simple budgeting framework: 50% for Needs, 30% for Wants, and 20% for Savings/Debt reduction."},
        {"Topic": "Compound Interest", "Difficulty": "Intermediate", "Content": "Compound interest is the interest on savings calculated on both the initial principal and the accumulated interest from previous periods."},
        {"Topic": "ETFs vs Mutual Funds", "Difficulty": "Advanced", "Content": "ETFs trade like stocks on an exchange and typically have lower fees. Mutual funds are bought at the end of the trading day and may be actively managed."},
        {"Topic": "Debt Snowball vs Avalanche", "Difficulty": "Intermediate", "Content": "Snowball: pay off smallest debts first for psychological wins. Avalanche: pay off highest interest rate debts first to save money mathematically."}
    ])
    guides_df.to_csv("datasets/finance_guides.csv", index=False)
    logger.info("Saved datasets/finance_guides.csv")
    
    print("All mock datasets generated successfully!")

if __name__ == "__main__":
    generate_mock_data()
