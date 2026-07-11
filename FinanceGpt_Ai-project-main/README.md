# Finance GPT AI

Welcome to **Finance GPT AI**! 🚀
This is a complete beginner-to-advanced project designed to help you learn Python, Machine Learning, and AI API integration (like Gemini or OpenAI) while building a real-world financial application.

## 🌟 Features
- **AI Finance Chatbot**: An intelligent assistant to answer your financial queries.
- **Expense Tracking & Data Analysis**: Analyze tabular financial data visually.
- **Stock Prediction Demo**: A machine learning model predicting stock prices.
- **Streamlit Dashboard**: A beautiful, interactive web interface for all features.

## 📂 Project Architecture
The project is built with modularity in mind.
- **`app.py`**: The main entry point (Streamlit Dashboard).
- **`utils/`**: Helper scripts for data loading, preprocessing, and visualization.
- **`models/`**: Saves the trained Machine Learning models (`.pkl` files).
- **`datasets/`**: Stores generated mock CSV datasets.
- **`prompts/`**: Contains System Prompts used for Prompt Engineering the AI.

## 🛠️ How to Run Locally

### 1. Create a Virtual Environment (Recommended)
```bash
python -m venv venv
```
Activate it:
- Windows: `venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Generate Datasets and Train Model
```bash
python generate_data.py
python train.py
```

### 4. Setup API Keys
Rename `.env.example` to `.env` and add your Gemini API Key (or OpenAI key):
```env
GEMINI_API_KEY=your_key_here
```

### 5. Run the Application
```bash
streamlit run app.py
```

## 🚀 Future Improvements (Homework for you!)
1. **User Authentication**: Add a login system to separate data per user.
2. **Database Integration**: Swap out CSVs for SQLite or PostgreSQL.
3. **Live API Integration**: Fetch real-time stock prices using Yahoo Finance (`yfinance` library).
4. **PDF Reports**: Use `fpdf` to export charts and tables into a monthly PDF report.

Happy Coding! 🎉
