import pickle
import pandas as pd
import os
from utils.helpers import logger

def make_prediction(open_price, high, low, volume):
    """
    Loads our trained model and makes a prediction based on user input.
    
    Args:
        open_price (float): Opening price.
        high (float): High price.
        low (float): Low price.
        volume (int): Trading volume.
        
    Returns:
        float: The predicted closing price.
    """
    model_path = "models/finance_model.pkl"
    
    if not os.path.exists(model_path):
        logger.error("Model file not found. Please run train.py first.")
        return None
        
    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
            
        # Create a dataframe for the input because the model expects feature names
        input_data = pd.DataFrame({
            'Open': [open_price],
            'High': [high],
            'Low': [low],
            'Volume': [volume]
        })
        
        # Predict the closing price
        prediction = model.predict(input_data)[0]
        logger.info(f"Made prediction: {prediction:.2f}")
        
        # Save output for logging purposes
        os.makedirs("outputs", exist_ok=True)
        with open("outputs/predictions.txt", "a") as out_f:
            out_f.write(f"Input: {open_price},{high},{low},{volume} -> Predicted Close: {prediction:.2f}\n")
            
        return prediction
        
    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        return None

if __name__ == "__main__":
    # Test the prediction logic
    print("Testing Prediction...")
    pred = make_prediction(150.0, 155.0, 149.0, 1200000)
    if pred:
        print(f"Predicted Closing Price: ${pred:.2f}")
