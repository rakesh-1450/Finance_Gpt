import matplotlib.pyplot as plt
import pandas as pd
import os
from utils.helpers import logger

def plot_expenses_pie(df, save_path="outputs/charts/expenses_pie.png"):
    """
    Creates a pie chart from expense data.
    
    Args:
        df (pd.DataFrame): Expense dataframe (requires 'Category' and 'Amount' columns).
        save_path (str): Where to save the generated image.
        
    Returns:
        matplotlib.figure.Figure: The created figure.
    """
    if df is None or 'Category' not in df.columns or 'Amount' not in df.columns:
        logger.error("Invalid dataframe for expense pie chart.")
        return None
        
    # Group by category in case there are multiple entries per category
    category_totals = df.groupby('Category')['Amount'].sum()
    
    fig, ax = plt.subplots(figsize=(8, 8))
    # We use a beautiful color map
    colors = plt.cm.Paired(range(len(category_totals)))
    
    ax.pie(category_totals, labels=category_totals.index, autopct='%1.1f%%', startangle=140, colors=colors)
    ax.set_title("Expenses by Category")
    
    plt.tight_layout()
    # Save the chart
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path)
    logger.info(f"Saved pie chart to {save_path}")
    
    return fig

def plot_stock_trend(df, save_path="outputs/charts/stock_trend.png"):
    """
    Plots the closing price trend over time.
    
    Args:
        df (pd.DataFrame): Stock dataframe.
        save_path (str): Where to save the generated image.
    
    Returns:
        matplotlib.figure.Figure: The created figure.
    """
    if df is None or 'Date' not in df.columns or 'Close' not in df.columns:
        logger.error("Invalid dataframe for stock trend chart.")
        return None
        
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Plotting Date vs Close price
    ax.plot(pd.to_datetime(df['Date']), df['Close'], marker='o', linestyle='-', color='b')
    
    ax.set_title("Stock Closing Price Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price ($)")
    ax.grid(True)
    
    # Rotate dates for better readability
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    plt.savefig(save_path)
    logger.info(f"Saved stock trend chart to {save_path}")
    
    return fig
