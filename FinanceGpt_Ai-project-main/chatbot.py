import os
import time
from google import genai                # Official Gemini SDK (google-genai)
from dotenv import load_dotenv
from utils.helpers import logger

# Load environment variables (API Key) from the .env file
load_dotenv(override=True)

# ─────────────────────────────────────────────────────────────────────────────
# MODEL FALLBACK CHAIN
# If one model hits its quota limit, we automatically try the next one.
# Order: cheapest/fastest first → more capable models as fallback.
# ─────────────────────────────────────────────────────────────────────────────
GEMINI_MODELS = [
    "gemini-2.0-flash-lite",   # Fastest, lowest quota usage — try first
    "gemini-2.5-flash",        # Fallback #1 — has separate daily quota
    "gemini-2.0-flash",        # Fallback #2
    "gemini-flash-latest",     # Fallback #3 — alias to latest flash model
]

def get_system_prompt():
    """
    Reads our custom system prompt to give the AI its 'Finance Expert' personality.
    The prompt is stored in prompts/finance_prompts.txt for easy editing.
    """
    try:
        with open("prompts/finance_prompts.txt", "r") as f:
            return f.read()
    except FileNotFoundError:
        # Default fallback if the prompts file doesn't exist
        return "You are a helpful AI finance assistant. Provide clear, accurate, beginner-friendly financial advice."

def ask_finance_bot(user_message, chat_history=None):
    """
    Sends the user's message to Google Gemini AI and returns the response.
    Automatically falls back to the next model if quota is exceeded (429 error).

    Args:
        user_message (str): The question or message from the user.
        chat_history (list): Optional list of past messages for context.

    Returns:
        str: The AI's text response.
    """
    # Step 1: Load the system prompt to shape the AI's personality
    system_prompt = get_system_prompt()

    # Step 2: Read the Gemini API key from the .env file
    gemini_key = os.getenv("GEMINI_API_KEY")

    # Step 3: If no key is found, run in Mock Mode (so the app still loads)
    if not gemini_key:
        logger.warning("GEMINI_API_KEY not found in .env file. Running in Mock Mode.")
        return (
            "[Mock Mode] Please add your GEMINI_API_KEY to the .env file "
            "to enable real AI responses from Google Gemini!"
        )

    # Step 4: Create a Gemini client using the google-genai SDK
    client = genai.Client(api_key=gemini_key)

    # Step 5: Combine the system prompt + user question into a single prompt
    full_prompt = f"{system_prompt}\n\nUser: {user_message}\nAI:"

    # Step 6: Try each model in the fallback chain
    last_error = None
    for model_name in GEMINI_MODELS:
        try:
            logger.info(f"Trying Gemini model: {model_name}")
            response = client.models.generate_content(
                model=model_name,
                contents=full_prompt,
            )
            logger.info(f"Success! Got response from model: {model_name}")
            return response.text

        except Exception as e:
            error_str = str(e)

            # Check if this is a quota/rate-limit error (429)
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                logger.warning(f"Model '{model_name}' quota exhausted. Trying next model...")
                last_error = e

                # Extract retry delay from error if available and wait briefly
                retry_delay = 2  # default 2 seconds between model switches
                if "retryDelay" in error_str:
                    try:
                        import re
                        match = re.search(r"'retryDelay': '(\d+)s'", error_str)
                        if match:
                            # Only wait if the delay is short (don't block the UI)
                            suggested = int(match.group(1))
                            retry_delay = min(suggested, 3)
                    except Exception:
                        pass

                time.sleep(retry_delay)
                continue  # Try the next model

            else:
                # Non-quota error (e.g., invalid key, network issue) — stop immediately
                logger.error(f"Non-quota error with model '{model_name}': {e}")
                return (
                    f"[Error] Gemini API error: {e}\n\n"
                    "Please check your API key in the Settings page."
                )

    # Step 7: All models exhausted — return a helpful message
    logger.error(f"All Gemini models exhausted their quota. Last error: {last_error}")
    return (
        "[Quota Exhausted] All available Gemini models have hit their daily free-tier limit.\n\n"
        "Please try one of these solutions:\n"
        "1. Wait until tomorrow (quota resets daily at midnight Pacific Time)\n"
        "2. Generate a new API key at https://aistudio.google.com\n"
        "3. Enable billing on your Google Cloud project for higher limits"
    )


# ─────────────────────────────────────────────
# Quick test — run this file directly to verify
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("Testing Finance Chatbot with Gemini (model fallback chain)...\n")
    print(f"Will try these models in order: {GEMINI_MODELS}\n")
    question = "What is the 50/30/20 budgeting rule?"
    print(f"Question: {question}\n")
    answer = ask_finance_bot(question)
    print("AI Response:")
    print(answer)
