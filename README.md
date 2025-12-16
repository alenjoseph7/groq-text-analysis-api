# Groq Text Analysis API

A serverless text analysis API built using AWS Lambda, API Gateway, and Groq LLM.
The API accepts raw text and returns a structured JSON response containing a summary,
category, sentiment, and risk level.

## Tech Stack
- AWS Lambda (Python)
- AWS API Gateway (HTTP API)
- Groq LLM (llama-3.3-70b-versatile)

## Endpoint
POST /analyze

## Request
```json
{
  {
  "text": "Artificial intelligence is transforming healthcare, finance, and education by improving efficiency while raising ethical concerns."
}

}
   


   #output:{
  "summary": "Artificial intelligence is transforming industries while raising ethical concerns.",
  "category": "Technology",
  "sentiment": "Neutral",
  "risk_level": "Moderate"
}
