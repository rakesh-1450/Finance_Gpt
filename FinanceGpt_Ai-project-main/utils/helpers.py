import logging
import os

def setup_logger(name="FinanceGPT", log_file="outputs/logs/app.log"):
    """
    Sets up a custom logger to record application events and errors.
    Like a trainer recording a student's progress!
    """
    # Create logs directory if it doesn't exist
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Only add handlers if they don't exist to prevent duplicate logs
    if not logger.handlers:
        # Create handlers (Console and File)
        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler(log_file)
        
        # Create formatters
        format_str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        c_format = logging.Formatter(format_str)
        f_format = logging.Formatter(format_str)
        
        c_handler.setFormatter(c_format)
        f_handler.setFormatter(f_format)
        
        # Add handlers to the logger
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)
        
    return logger

# Initialize a global logger for the project
logger = setup_logger()

def ensure_directories():
    """
    Utility function to ensure all required output directories exist.
    """
    dirs = ['datasets', 'models', 'outputs/charts', 'outputs/logs']
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        logger.info(f"Ensured directory exists: {d}")

def update_env_file(key, value):
    """
    Safely updates the .env file with a new key-value pair.
    Creates the file if it doesn't exist.
    """
    env_path = ".env"
    lines = []
    
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            lines = f.readlines()
            
    key_exists = False
    for i, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[i] = f"{key}={value}\n"
            key_exists = True
            break
            
    if not key_exists:
        lines.append(f"{key}={value}\n")
        
    with open(env_path, "w") as f:
        f.writelines(lines)
        
    # Also update the os environment immediately for the current session
    os.environ[key] = value
    logger.info(f"Updated {key} in .env file.")
