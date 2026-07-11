import os
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

from utils.helpers import logger, ensure_directories
from utils.data_loader import load_csv
from utils.preprocessing import prepare_stock_features

def train_model():
    """
    Trains a Machine Learning model to predict stock closing prices.
    This demonstrates the power of Scikit-Learn!
    """
    ensure_directories()
    
    logger.info("Starting model training process...")
    
    # Load stock data
    df = load_csv("datasets/stock_prices.csv")
    if df is None:
        logger.error("Could not load stock data. Run generate_data.py first!")
        return
        
    # Prepare features and target
    X, y = prepare_stock_features(df)
    if X is None or y is None:
        return
        
    # Split the data into training and testing sets
    # We use 80% of data for training, 20% for testing
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Initialize the model (Random Forest is a great beginner model!)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    
    # Train the model
    logger.info("Training Random Forest model...")
    model.fit(X_train, y_train)
    
    # Evaluate the model
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    logger.info(f"Model trained successfully! Mean Squared Error: {mse:.2f}")
    
    # Save the model so we don't have to retrain it every time
    model_path = "models/finance_model.pkl"
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
        
    logger.info(f"Model saved to {model_path}")
    print(f"Training Complete. Model saved at {model_path}. MSE: {mse:.2f}")

if __name__ == "__main__":
    train_model()
