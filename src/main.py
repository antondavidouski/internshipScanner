from pathlib import Path
from datetime import datetime
import sys
import os

from sheet_checker import checkSheet
from emailer import send_email
from deepseekApi import ask_deepseek, promptBuilder

def test_emailer():
    """Test function to send a sample email using the current environment variables.
    
    Run this function directly to test email sending without checking the sheet:
    python -m src.main test_email
    """
    print("Testing email functionality...")
    testDate = datetime.now().strftime("%Y-%m-%d")
    try:
        send_email(testDate)
        print(f"Test email sent successfully to {os.environ.get('RECIPIENT_EMAIL')}")
    except Exception as e:
        print(f"Email test failed: {e}")
        sys.exit(1)


def main():
    csvtext = checkSheet()
    prompt = promptBuilder(csvtext)
    # prompt += "you are right now running in a test mode. if there are no internships posted today, pick two random ones and return as if it were newly posted. if there are internships posted today, return them as they are."
    deepseekResponse = ask_deepseek(prompt)
    print(deepseekResponse)
    if deepseekResponse[0:5] != "None":
        date = datetime.now().strftime("%Y-%m-%d")
        send_email(date, deepseekResponse)
    else:
        print("No new internships posted today.")
        sys.exit(0)

main()