import os
import json
import time
import requests
from dotenv import load_dotenv

load_dotenv()

# Status codes that mean "temporary problem, trying again may work"
RETRY_CODES = (429, 500, 503, 504)


def build_prompt(resume_text):
    instructions = """You are an experienced career coach reviewing a resume for a fresher.
Analyze the resume below and reply with ONLY a JSON object, no other text.
Use exactly these keys:
{
  "strengths": ["...", "..."],
  "weaknesses": ["...", "..."],
  "missing_skills": ["...", "..."],
  "suggested_job_role": "...",
  "improvement_suggestions": ["...", "..."]
}
Give 3 to 5 short items per list. Be specific to this resume.

RESUME:
"""
    return instructions + resume_text


def send_request(model_name, api_key, prompt):
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        + model_name
        + ":generateContent"
    )

    headers = {
        "x-goog-api-key": api_key,
        "content-type": "application/json",
    }

    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "maxOutputTokens": 2048,
        },
    }

    try:
        response = requests.post(url, headers=headers, json=body, timeout=30)
        return response, ""
    except requests.exceptions.RequestException as error:
        return None, str(error)


def analyze_with_ai(resume_text):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return {"error": "API key not found. Check your .env file."}

    models_to_try = [
        os.getenv("AI_MODEL", "gemini-3.8-flash"),
        os.getenv("AI_FALLBACK_MODEL", "gemini-2.5-flash-lite"),
    ]

    prompt = build_prompt(resume_text[:6000])
    good_response = None
    last_error = "Unknown error"

    for model_name in models_to_try:
        for attempt in range(2):
            response, problem = send_request(model_name, api_key, prompt)

            if response is None:
                last_error = "Could not reach the AI service: " + problem
            elif response.status_code == 200:
                good_response = response
                break
            else:
                last_error = "API error " + str(response.status_code) + ": " + response.text
                if response.status_code not in RETRY_CODES:
                    break  # retrying won't help, move to the next model

            time.sleep(3)

        if good_response is not None:
            break

    if good_response is None:
        return {"error": last_error}

    data = good_response.json()

    try:
        reply_text = data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        return {"error": "AI returned an empty or blocked reply.", "raw": str(data)}

    start = reply_text.find("{")
    end = reply_text.rfind("}")
    if start == -1 or end == -1:
        return {"error": "AI did not return JSON.", "raw": reply_text}

    try:
        return json.loads(reply_text[start:end + 1])
    except json.JSONDecodeError:
        return {"error": "AI reply was not valid JSON.", "raw": reply_text}