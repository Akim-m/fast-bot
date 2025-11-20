import json
import re
import requests
import logging
from datetime import datetime, UTC
from ollama import chat as ollama_chat
from pydantic import BaseModel

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("agent.log"), logging.StreamHandler()]
)

class WeatherResponse(BaseModel):
    city: str
    temperature: str
    description: str

SYSTEM_PROMPT = """
You are an intelligent assistant with access to three tools.
only use these tools and dont use any other external resources.

======================
TOOL 1: get_weather
===================

Purpose:
Retrieve weather information for a city.

Usage:
{
"action": "get_weather",
"city": "<city name>"
}

======================
TOOL 2: fetch_url
=================

Purpose:
Fetch any HTTP/HTTPS URL (GET, POST, PUT, DELETE).

Usage:
{
"action": "fetch_url",
"url": "<full URL>",
"method": "<GET|POST|PUT|DELETE>",
"data": { ... }  # optional for POST/PUT
}

======================
TOOL 3: manage_users
====================

Purpose:
Perform CRUD operations on /users endpoints.

Usage:
{
"action": "manage_users",
"method": "<GET|POST|PUT|DELETE>",
"user_id": <optional>,
"data": { "user_name": "<name>" }  # for POST/PUT
}

RULES:

* Always output JSON for tool calls
* Use get_weather anytime user asks about weather
* Only use other tools when needed
* Otherwise respond normally
"""


def extract_json(text: str):
    try:
        match = re.search(r"{.*}", text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
    except Exception as e:
        logging.error(f"JSON extraction failed: {e}")
    return None

def fetch_url_content(url: str, method: str = "GET", headers: dict = None, data: dict = None) -> str:
    method = method.upper()
    headers = headers or {}
    logging.info(f"Fetching URL: {url} | Method: {method} | Data: {data}")
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=15)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data, timeout=15)
        elif method == "PUT":
            response = requests.put(url, headers=headers, json=data, timeout=15)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, timeout=15)
        else:
            return f"Unsupported HTTP method: {method}"

        try:
            result = json.dumps(response.json(), indent=2)
        except:
            result = response.text[:5000]

        logging.info(f"Response received from {url}")
        return result
    except Exception as e:
        logging.error(f"Fetch error: {e}")
        return f"FETCH_ERROR: {e}"

def call_weather(city: str) -> str:
    url = f"http://127.0.0.1:8000/weather/city/{city}"
    logging.info(f"Fetching weather for city: {city}")
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        weather = WeatherResponse(**response.json())
        temperature = weather.temperature.replace("°C°C", "°C").replace("°C °C", "°C")
        result = f"{weather.city}: {weather.description}, {temperature}"
        logging.info(f"Weather result: {result}")
        return result
    except Exception as e:
        logging.error(f"Error fetching weather: {e}")
        return f"Error fetching weather: {e}"

def call_user_api(method: str, user_id: int = None, data: dict = None) -> str:
    base_url = "http://127.0.0.1:8000/users"
    url = f"{base_url}/{user_id}" if user_id else base_url
    logging.info(f"Calling user API | URL: {url} | Method: {method} | Data: {data}")
    return fetch_url_content(url, method=method, data=data)

def summarize_response(text: str) -> str:
    logging.info("Summarizing API response")
    prompt = f"Summarize the following API response clearly:\n{text}"
    try:
        reply = ollama_chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])
        result = reply["message"]["content"]
        logging.info("Summarization completed")
        return result
    except Exception as e:
        logging.error(f"Error summarizing response: {e}")
        return f"Error summarizing response: {e}"


def chat(user_msg: str) -> str:
    logging.info(f"User message: {user_msg}")
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_msg}
    ]

    try:
        llm_response = ollama_chat(model="llama3.2", messages=messages)
    except Exception as e:
        logging.error(f"LLM connection error: {e}")
        return f"LLM connection error: {e}"

    content = llm_response["message"]["content"]
    logging.info(f"LLM response: {content}")
    decision = extract_json(content)

    if isinstance(decision, dict) and "action" in decision:
        action = decision["action"]

        if action == "get_weather":
            city = decision.get("city")
            return call_weather(city)

        elif action == "fetch_url":
            url = decision.get("url")
            if not url or not url.startswith("http"):
                logging.warning(f"Invalid URL: {url}")
                return f"Invalid URL: {url}"
            method = decision.get("method", "GET")
            data = decision.get("data")
            raw = fetch_url_content(url, method=method, data=data)
            return summarize_response(raw)

        elif action == "manage_users":
            method = decision.get("method", "GET")
            user_id = decision.get("user_id")
            data = decision.get("data")
            raw = call_user_api(method=method, user_id=user_id, data=data)
            return summarize_response(raw)

    return content


def main():
    logging.info("Agent started")
    print("Agent active. Type 'exit' to quit.")
    while True:
        msg = input("You: ")
        if msg.lower() in ("exit", "quit"):
            logging.info("Agent shutting down")
            break
        response = chat(msg)
        print("Assistant:", response, "\n")

if __name__ == "__main__":
    main()