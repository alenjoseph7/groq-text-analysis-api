import json
import os
import urllib.request
import urllib.error
import ssl

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"

MAX_TEXT_LENGTH = 8000


def call_groq_llama(text: str) -> dict:
    if not GROQ_API_KEY:
        raise Exception("GROQ_API_KEY is missing")

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a backend API. "
                    "Respond with VALID JSON ONLY. "
                    "Do not include markdown, code blocks, or explanations."
                )
            },
            {
                "role": "user",
                "content": (
                    "Return JSON in exactly this format:\n"
                    "{\n"
                    '  "summary": "<one sentence>",\n'
                    '  "category": "<single word>",\n'
                    '  "sentiment": "<Positive|Neutral|Negative>",\n'
                    '  "risk_level": "<Low|Moderate|High>"\n'
                    "}\n\n"
                    f"Text:\n{text}"
                )
            }
        ],
        "temperature": 0.2,
        "max_tokens": 300
    }

    data = json.dumps(payload).encode("utf-8")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    req = urllib.request.Request(
        GROQ_URL, data=data, headers=headers, method="POST"
    )

    context = ssl.create_default_context()

    with urllib.request.urlopen(req, context=context) as response:
        raw = response.read().decode("utf-8")
        resp = json.loads(raw)

        content = resp["choices"][0]["message"]["content"]

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            raise Exception("LLM returned invalid JSON")


def lambda_handler(event, context):
    text = ""

    if "body" in event:
        try:
            body = json.loads(event["body"])
            text = body.get("text", "")
        except Exception:
            text = event["body"]
    else:
        text = event.get("text", "")

    if not text:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "No text provided"})
        }

    if len(text) > MAX_TEXT_LENGTH:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Text too long"})
        }

    try:
        result = call_groq_llama(text)
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(result)
    }
