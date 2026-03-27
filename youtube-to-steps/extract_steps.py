#!/usr/bin/env python3
"""
extract_steps.py <youtube_url> [N]

Calls Gemini API with a YouTube URL and returns steps as JSON.
If N is omitted, Gemini determines the appropriate step count automatically.
"""

import sys
import json
import re
import os
import time
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from google import genai
from google.genai import types
from google.genai.errors import ClientError

API_KEY = "AIzaSyA_AN5-LL9LCDQ9sCnaZVcSNW_53qiM_GI"
MODEL = "models/gemini-2.5-flash"
FIXED_PROMPT_PATH = "prompts/gemini_prompt.txt"
AUTO_PROMPT_PATH = "prompts/gemini_auto_prompt.txt"
MAX_RETRIES = 4


def clean_youtube_url(url: str) -> str:
    """Strip timestamp and playlist params — Gemini only accepts v= param."""
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)
    clean_qs = {k: v for k, v in qs.items() if k == "v"}
    clean = parsed._replace(query=urlencode(clean_qs, doseq=True))
    return urlunparse(clean)


def load_prompt(n=None) -> str:
    if n is not None:
        prompt_file = os.path.join(os.path.dirname(__file__), FIXED_PROMPT_PATH)
        with open(prompt_file) as f:
            return f.read().replace("{N}", str(n))
    else:
        prompt_file = os.path.join(os.path.dirname(__file__), AUTO_PROMPT_PATH)
        with open(prompt_file) as f:
            return f.read()


def extract_json(text: str) -> dict:
    # Strip markdown fences
    text = re.sub(r"```(?:json)?", "", text).strip().rstrip("`").strip()
    # Try object first (new format with summary), fall back to bare array (fixed-N prompt)
    obj_start = text.find("{")
    arr_start = text.find("[")
    if obj_start != -1 and (arr_start == -1 or obj_start < arr_start):
        end = text.rfind("}")
        parsed = json.loads(text[obj_start:end + 1])
        return {"summary": parsed.get("summary", ""), "steps": parsed["steps"]}
    else:
        end = text.rfind("]")
        steps = json.loads(text[arr_start:end + 1])
        return {"summary": "", "steps": steps}


def call_gemini(client, youtube_url: str, prompt: str) -> str:
    """Call Gemini with retry on 429 rate limit."""
    delay = 40
    for attempt in range(MAX_RETRIES):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=[
                    types.Part(file_data=types.FileData(file_uri=youtube_url)),
                    types.Part(text=prompt),
                ]
            )
            return response.text
        except ClientError as e:
            if "429" in str(e) and attempt < MAX_RETRIES - 1:
                print(f"Rate limited, retrying in {delay}s (attempt {attempt + 1})...", file=sys.stderr)
                time.sleep(delay)
                delay = min(delay * 2, 120)
            else:
                raise


def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: extract_steps.py <youtube_url> [N]", file=sys.stderr)
        sys.exit(1)

    youtube_url = sys.argv[1]
    n = None
    if len(sys.argv) == 3:
        try:
            n = int(sys.argv[2])
        except ValueError:
            print("N must be an integer", file=sys.stderr)
            sys.exit(1)

    youtube_url = clean_youtube_url(youtube_url)
    client = genai.Client(api_key=API_KEY)
    prompt = load_prompt(n)

    # Retry on JSON parse failure (Gemini occasionally returns malformed JSON)
    for attempt in range(2):
        raw = call_gemini(client, youtube_url, prompt)
        try:
            result = extract_json(raw)
            break
        except json.JSONDecodeError as e:
            if attempt == 0:
                print(f"JSON parse failed ({e}), retrying...", file=sys.stderr)
                time.sleep(5)
            else:
                print(f"JSON parse failed after retry: {e}", file=sys.stderr)
                print(f"Raw response:\n{raw[:500]}", file=sys.stderr)
                sys.exit(1)

    steps = result["steps"]
    if n is not None and len(steps) != n:
        print(f"Warning: Gemini returned {len(steps)} steps, expected {n}", file=sys.stderr)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
