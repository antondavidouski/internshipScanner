#!/usr/bin/env python3
"""
deepseek_one_shot.py
Send ONE prompt to DeepSeek and exit.
"""

import os
import sys
import json
import requests
from dotenv import load_dotenv
import datetime

# Configuration
load_dotenv()                                   # loads .env from current dir
apiUrl = "https://api.deepseek.com/v1/chat/completions"
apiKey = os.getenv("API_KEY")                 
model = "deepseek-chat"                      
stream = False                                 # set False for non-streaming

if not apiKey:
    sys.exit("Error: API_KEY not set in .env")

def ask_deepseek(prompt):
    """Send *prompt* and return the assistant's full reply text."""
    headers = {
        "Authorization": f"Bearer {apiKey}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "stream": stream,
        "temperature": 0.1,
        "messages": [
            {"role": "system", "content": "Your response will be completely plain text, no markdown or code blocks. You will be provided todays date and a csv file containing data for different job descriptions. Your job is to look at the opening date column and find any opening dates which are today. Your response should be structured as follows: If there are no openings today, single return \"None\" and nothing else. If there are openings, return them nicely formatted in a list, in the following format: <Company Name> - <Position name>. You msut return ALL positions which have opened today, you must not miss a single position. Return nothing other than this list."},
            {"role": "user",   "content": prompt},
        ],
    }

    resp = requests.post(apiUrl, headers=headers, json=payload, stream=stream, timeout=60)
    resp.raise_for_status()

    answer = ""
    if stream:
        # Streaming mode: print tokens as they arrive
        for line in resp.iter_lines(decode_unicode=True):
            if not line or not line.startswith("data: "):
                continue
            chunk = line[len("data: "):].strip()
            if chunk == "[DONE]":
                break
            delta = json.loads(chunk)["choices"][0]["delta"].get("content", "")
            sys.stdout.write(delta)
            sys.stdout.flush()
            answer += delta
        print()      # newline when done
    else:
        # Non-streaming mode: one JSON blob
        answer = resp.json()["choices"][0]["message"]["content"]

    return answer


def promptBuilder(csvText):
    date = f"The date today is 19 august 2024"
    # date = f"The date today is {datetime.date.today()}"
    prompt = f"Todays date: {date}. The csv file is as follows:\n\n{csvText}"
    return prompt
