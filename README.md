# Digital Wellbeing AI Engine

A production-ready FastAPI backend for analyzing digital usage patterns and providing personalized recommendations. The system is completely stateless - all computation happens in real-time based on incoming request data.

## 🚀 Features

- **Real-time Analysis**: Instant processing of usage data without persistence
- **Addiction Scoring**: Weighted algorithm (0-100 scale) with explainable results
- **Pattern Detection**: Identifies usage patterns like night usage, binge sessions, and social media dominance
- **Personalized Recommendations**: Dynamic suggestions based on computed features
- **Risk Classification**: Low/Moderate/High risk levels
- **Production Ready**: Comprehensive validation, error handling, and logging

## 📋 API Endpoint

### POST /analyze-usage

Analyzes digital usage patterns and returns comprehensive insights.

#### Request Body

```json
{
  "user_id": "string",
  "total_screen_time": "integer (minutes)",
  "unlock_count": "integer",
  "app_usage": [
    {
      "app": "string",
      "minutes": "integer"
    }
  ],
  "sessions": [
    {
      "start": "HH:MM",
      "end": "HH:MM"
    }
  ],
  "notifications": {
    "app_name": "integer (count)"
  }
}
```

#### Response Body

```json
{
  "addiction_score": "number (0-100)",
  "risk_level": "Low|Moderate|High",
  "patterns": ["string"],
  "recommendations": ["string"],
  "insights": {
    "most_used_app": "string",
    "peak_usage_period": "string",
    "usage_summary": "string"
  },
  "explanation": {
    "screen_time": "percentage",
    "social_media": "percentage",
    "night_usage": "percentage",
    "unlock_behavior": "percentage",
    "session_behavior": "percentage"
  }
}
```

## 🏗️ Architecture

```
├── main.py              # FastAPI application and endpoints
├── models.py            # Pydantic validation models
├── feature_engine.py    # Feature computation and metrics
├── scoring.py           # Addiction score calculation
├── patterns.py          # Usage pattern detection
├── recommendations.py   # Dynamic recommendation engine
├── requirements.txt     # Python dependencies
└── README.md           # This documentation
```

## 🧠 Scoring Algorithm

The addiction score uses a weighted model:

- **Screen Time** (30%): Total usage duration
- **Social Media Ratio** (25%): Percentage of social media usage
- **Night Usage** (20%): Usage between 22:00-06:00
- **Unlock Frequency** (15%): Phone checks per hour
- **Session Duration** (10%): Average session length

**Risk Levels**:
- Low: < 40
- Moderate: 40-70  
- High: > 70

## 🔍 Pattern Detection

The system detects various usage patterns:

- **High Night Usage**: >30% of usage during night hours
- **Long Sessions**: Average session >60 minutes
- **Frequent Checking**: >10 unlocks per hour
- **Social Media Dominance**: >50% social media usage
- **Usage Spikes**: Sessions >2x average duration
- **Binge Patterns**: Multiple long sessions
- **Notification-Driven**: High unlock-to-session ratio

## 💡 Recommendation Engine

Generates personalized suggestions based on:

- Screen time levels
- Social media usage patterns
- Night time usage
- Session management needs
- App-specific usage
- Detected patterns

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.11+
- pip

### Setup

1. **Clone and navigate**:
```bash
cd "DIGITAL WELL BACKEND"
```

2. **Create virtual environment**:
```bash
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Run the server**:
```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

## 📚 Usage Examples

### Example Request

```bash
curl -X POST "http://127.0.0.1:8000/analyze-usage" \
-H "Content-Type: application/json" \
-d '{
  "user_id": "user_123",
  "total_screen_time": 420,
  "unlock_count": 85,
  "app_usage": [
    {"app": "instagram", "minutes": 180},
    {"app": "youtube", "minutes": 120},
    {"app": "whatsapp", "minutes": 60},
    {"app": "chrome", "minutes": 60}
  ],
  "sessions": [
    {"start": "09:00", "end": "10:30"},
    {"start": "12:00", "end": "13:45"},
    {"start": "20:00", "end": "22:30"},
    {"start": "23:30", "end": "01:00"}
  ],
  "notifications": {
    "instagram": 45,
    "whatsapp": 30,
    "youtube": 15
  }
}'
```

### Example Response

```json
{
  "addiction_score": 72.2,
  "risk_level": "High",
  "patterns": [
    "Long continuous sessions (avg 108.8 minutes)",
    "Social media dominance (85.7% of usage)",
    "Potential notification-driven usage (high unlock-to-session ratio)"
  ],
  "recommendations": [
    "Set a daily screen time limit of 300 minutes",
    "Limit social media apps to 126 minutes per day",
    "Disable notifications for social media apps",
    "Enable bedtime mode from 22:00 to 06:00",
    "Keep phone out of bedroom during sleep hours"
  ],
  "insights": {
    "most_used_app": "instagram",
    "peak_usage_period": "Morning",
    "usage_summary": "420 minutes total screen time, 4 sessions, average 108.8 minutes per session, most used app: instagram"
  },
  "explanation": {
    "screen_time": 36.4,
    "social_media": 29.7,
    "night_usage": 15.8,
    "unlock_behavior": 5.5,
    "session_behavior": 12.6
  }
}
```

## 🔧 Development

### Running Tests

The API includes comprehensive validation and error handling. Test with the interactive docs:

- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

### Health Check

```bash
curl http://127.0.0.1:8000/health
```

## 🚨 Important Constraints

- **Stateless**: No data persistence or storage
- **Real-time**: All computation happens per request
- **Privacy**: No user data is retained
- **Deterministic**: Same input always produces same output

## 📊 Technical Specifications

- **Framework**: FastAPI 0.95.2
- **Validation**: Pydantic 1.10.12
- **Server**: Uvicorn 0.22.0
- **Python**: 3.11+
- **Architecture**: Modular, production-ready

## 🤝 Contributing

The system is designed to be modular and extensible. Key areas for enhancement:

- Additional pattern detection algorithms
- More sophisticated recommendation logic
- Enhanced scoring models
- Additional metrics and insights

## 📄 License

This project is provided as-is for educational and development purposes.
