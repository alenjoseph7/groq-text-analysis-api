# ⚡ Groq Text Analysis API

A serverless, multi-mode text analysis API built on **AWS Lambda** and powered by **Groq's LLM inference engine** (Llama 3.3 70B). Designed for low-latency, structured, machine-readable outputs that integrate seamlessly into downstream systems.

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-orange?logo=amazonaws)
![Groq](https://img.shields.io/badge/Groq-LLM-purple)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Architecture

```
┌────────────┐      ┌─────────────────┐      ┌──────────────┐      ┌─────────────┐
│   Client   │─────▶│  API Gateway    │─────▶│  AWS Lambda   │─────▶│  Groq API   │
│ Dashboard  │◀─────│  (HTTP API)     │◀─────│  (Python)     │◀─────│  Llama 3.3  │
└────────────┘      └─────────────────┘      └──────┬───────┘      └─────────────┘
                                                     │
                                              ┌──────▼───────┐
                                              │   History     │
                                              │   Store       │
                                              └──────────────┘
```

---

## Features

| Feature | Description |
|---------|-------------|
| **Multi-Mode Analysis** | Quick, Detailed, Entity Extraction, Sentiment Deep Dive |
| **Batch Processing** | Analyze up to 10 texts in a single request |
| **Structured JSON Output** | Machine-readable responses for system integration |
| **Analysis History** | Track past analyses with metadata |
| **Analytics Dashboard** | Sentiment distribution, category trends, usage stats |
| **Input Sanitization** | Null byte removal, whitespace normalization, length validation |
| **CORS Enabled** | Ready for frontend integration |
| **Health Check** | `/health` endpoint for monitoring |
| **Low Latency** | Powered by Groq's LPU inference engine |

---

## API Endpoints

### `POST /analyze` — Single Text Analysis

Analyze a single text with the specified mode.

**Request:**
```json
{
  "text": "Tesla reported record Q4 earnings, beating analyst expectations by 15%.",
  "mode": "detailed"
}
```

**Available Modes:**
| Mode | Description | Output Fields |
|------|-------------|---------------|
| `quick` | Fast summary + sentiment | summary, category, sentiment, confidence, risk_level |
| `detailed` | Comprehensive analysis | All quick fields + entities, key_phrases, tone, emotion, actionable_insights, language |
| `entities` | Named Entity Recognition | entities (name, type, context), entity_count |
| `sentiment` | Deep sentiment analysis | overall_sentiment, confidence, emotion_breakdown, tone, subjectivity, key_sentiment_drivers |

**Response:**
```json
{
  "success": true,
  "analysis_id": "a1b2c3d4-...",
  "mode": "detailed",
  "result": {
    "summary": "Tesla exceeded Q4 earnings expectations with record performance.",
    "category": "Finance",
    "subcategory": "Earnings",
    "sentiment": "Positive",
    "sentiment_confidence": 0.92,
    "emotion": "Optimism",
    "tone": "formal",
    "risk_level": "Low",
    "key_phrases": ["record Q4 earnings", "beating analyst expectations"],
    "entities": [
      {"name": "Tesla", "type": "ORG"},
      {"name": "Q4", "type": "DATE"}
    ],
    "actionable_insights": ["Strong buy signal based on earnings beat"],
    "language": "English"
  },
  "metadata": {
    "model": "llama-3.3-70b-versatile",
    "processing_time_ms": 823.45,
    "tokens_used": 245,
    "text_length": 71,
    "timestamp": "2025-02-09T12:00:00Z"
  }
}
```

---

### `POST /batch` — Batch Analysis

Analyze multiple texts in a single request.

**Request:**
```json
{
  "texts": [
    "Great product, fast shipping!",
    "Terrible customer service, waited 3 hours.",
    "The package arrived on time."
  ],
  "mode": "quick"
}
```

**Response:**
```json
{
  "success": true,
  "batch_summary": {
    "total": 3,
    "successful": 3,
    "failed": 0,
    "total_processing_time_ms": 2450.32
  },
  "results": [
    {"index": 0, "success": true, "result": {"sentiment": "Positive", ...}},
    {"index": 1, "success": true, "result": {"sentiment": "Negative", ...}},
    {"index": 2, "success": true, "result": {"sentiment": "Neutral", ...}}
  ]
}
```

---

### `GET /history` — Analysis History

Retrieve past analysis results.

**Query Parameters:** `?limit=20` (default: 20, max: 100)

---

### `GET /analytics` — Usage Analytics

Get aggregated statistics from analysis history.

**Response:**
```json
{
  "success": true,
  "analytics": {
    "total_analyses": 47,
    "sentiment_distribution": {"Positive": 22, "Neutral": 15, "Negative": 10},
    "category_distribution": {"Technology": 18, "Finance": 12, ...},
    "avg_processing_time_ms": 756.3,
    "total_tokens_used": 12450
  }
}
```

---

### `GET /health` — Health Check

Returns API status, available modes, and configuration.

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| **Runtime** | AWS Lambda (Python 3.9+) |
| **API Layer** | AWS API Gateway (HTTP API) |
| **LLM Provider** | Groq (Llama 3.3 70B Versatile) |
| **Frontend** | Vanilla HTML/CSS/JS Dashboard |
| **Testing** | pytest with unittest.mock |

---

## Setup & Deployment

### Prerequisites
- AWS Account with Lambda and API Gateway access
- [Groq API Key](https://console.groq.com/keys) (free tier available)

### 1. Clone the Repository
```bash
git clone https://github.com/alenjoseph7/groq-text-analysis-api.git
cd groq-text-analysis-api
```

### 2. Set Environment Variables (in AWS Lambda)
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GROQ_API_KEY` | Yes | — | Your Groq API key |
| `GROQ_MODEL` | No | `llama-3.3-70b-versatile` | Groq model to use |
| `MAX_TEXT_LENGTH` | No | `8000` | Max input text length |
| `MAX_BATCH_SIZE` | No | `10` | Max texts per batch |
| `ENABLE_HISTORY` | No | `true` | Enable analysis history |
| `LOG_LEVEL` | No | `INFO` | Logging level |

### 3. Deploy to AWS Lambda
```bash
# Zip the function
zip lambda_function.zip lambda_function.py

# Deploy via AWS CLI
aws lambda update-function-code \
  --function-name groq-text-analysis \
  --zip-file fileb://lambda_function.zip
```

### 4. Configure API Gateway
Create routes in API Gateway pointing to your Lambda:
- `POST /analyze` → `lambda_function.lambda_handler`
- `POST /batch` → `lambda_function.lambda_handler`
- `GET /history` → `lambda_function.lambda_handler`
- `GET /analytics` → `lambda_function.lambda_handler`
- `GET /health` → `lambda_function.lambda_handler`

### 5. Launch Dashboard
Open `dashboard.html` and replace `YOUR_API_GATEWAY_URL_HERE` with your API Gateway endpoint URL.

---

## Running Tests

```bash
pip install pytest
python -m pytest tests/test_lambda.py -v
```

---

## Project Structure

```
groq-text-analysis-api/
├── lambda_function.py      # Main Lambda handler (all endpoints)
├── dashboard.html           # Frontend dashboard
├── tests/
│   └── test_lambda.py       # Unit tests
├── README.md
├── .gitignore
└── LICENSE
```

---

## Future Improvements

- [ ] DynamoDB integration for persistent history storage
- [ ] Authentication with API keys
- [ ] Rate limiting per client
- [ ] Webhook support for async batch processing
- [ ] Multi-language support
- [ ] PDF and document upload for analysis
- [ ] Comparison mode (analyze two texts side by side)

---

## License

MIT License — see [LICENSE](LICENSE) for details.