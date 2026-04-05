#!/bin/bash

# Digital Wellbeing AI Engine - Test Commands
# ===========================================

API_BASE="http://127.0.0.1:8000"

echo "🧪 Digital Wellbeing AI Engine - API Test Commands"
echo "=================================================="

# Health Check
echo ""
echo "1. Health Check:"
echo "curl $API_BASE/health"
curl $API_BASE/health
echo ""

# Root endpoint
echo ""
echo "2. Root Endpoint:"
echo "curl $API_BASE/"
curl $API_BASE/
echo ""

# Test Case 1: High Usage User (Social Media Addict)
echo ""
echo "3. High Usage User Test:"
echo "curl -X POST \"$API_BASE/analyze-usage\" \\"
echo "  -H \"Content-Type: application/json\" \\"
echo "  -d '{"
echo "    \"user_id\": \"heavy_user_001\","
echo "    \"total_screen_time\": 480,"
echo "    \"unlock_count\": 150,"
echo "    \"app_usage\": ["
echo "      {\"app\": \"instagram\", \"minutes\": 200},"
echo "      {\"app\": \"tiktok\", \"minutes\": 180},"
echo "      {\"app\": \"youtube\", \"minutes\": 60},"
echo "      {\"app\": \"whatsapp\", \"minutes\": 40}"
echo "    ],"
echo "    \"sessions\": ["
echo "      {\"start\": \"08:00\", \"end\": \"11:00\"},"
echo "      {\"start\": \"13:00\", \"end\": \"15:30\"},"
echo "      {\"start\": \"18:00\", \"end\": \"22:00\"},"
echo "      {\"start\": \"23:00\", \"end\": \"02:00\"}"
echo "    ],"
echo "    \"notifications\": {"
echo "      \"instagram\": 80,"
echo "      \"tiktok\": 60,"
echo "      \"whatsapp\": 30"
echo "    }"
echo "  }'"
echo ""

curl -X POST "$API_BASE/analyze-usage" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "heavy_user_001",
    "total_screen_time": 480,
    "unlock_count": 150,
    "app_usage": [
      {"app": "instagram", "minutes": 200},
      {"app": "tiktok", "minutes": 180},
      {"app": "youtube", "minutes": 60},
      {"app": "whatsapp", "minutes": 40}
    ],
    "sessions": [
      {"start": "08:00", "end": "11:00"},
      {"start": "13:00", "end": "15:30"},
      {"start": "18:00", "end": "22:00"},
      {"start": "23:00", "end": "02:00"}
    ],
    "notifications": {
      "instagram": 80,
      "tiktok": 60,
      "whatsapp": 30
    }
  }'
echo ""

# Test Case 2: Moderate Usage User (Professional)
echo ""
echo "4. Moderate Usage User Test:"
echo "curl -X POST \"$API_BASE/analyze-usage\" \\"
echo "  -H \"Content-Type: application/json\" \\"
echo "  -d '{"
echo "    \"user_id\": \"professional_user\","
echo "    \"total_screen_time\": 300,"
echo "    \"unlock_count\": 75,"
echo "    \"app_usage\": ["
echo "      {\"app\": \"chrome\", \"minutes\": 120},"
echo "      {\"app\": \"slack\", \"minutes\": 60},"
echo "      {\"app\": \"gmail\", \"minutes\": 45},"
echo "      {\"app\": \"whatsapp\", \"minutes\": 40},"
echo "      {\"app\": \"youtube\", \"minutes\": 35}"
echo "    ],"
echo "    \"sessions\": ["
echo "      {\"start\": \"09:00\", \"end\": \"11:00\"},"
echo "      {\"start\": \"14:00\", \"end\": \"16:30\"},"
echo "      {\"start\": \"19:00\", \"end\": \"21:00\"}"
echo "    ],"
echo "    \"notifications\": {"
echo "      \"slack\": 25,"
echo "      \"gmail\": 20,"
echo "      \"whatsapp\": 15"
echo "    }"
echo "  }'"
echo ""

curl -X POST "$API_BASE/analyze-usage" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "professional_user",
    "total_screen_time": 300,
    "unlock_count": 75,
    "app_usage": [
      {"app": "chrome", "minutes": 120},
      {"app": "slack", "minutes": 60},
      {"app": "gmail", "minutes": 45},
      {"app": "whatsapp", "minutes": 40},
      {"app": "youtube", "minutes": 35}
    ],
    "sessions": [
      {"start": "09:00", "end": "11:00"},
      {"start": "14:00", "end": "16:30"},
      {"start": "19:00", "end": "21:00"}
    ],
    "notifications": {
      "slack": 25,
      "gmail": 20,
      "whatsapp": 15
    }
  }'
echo ""

# Test Case 3: Low Usage User (Minimal User)
echo ""
echo "5. Low Usage User Test:"
echo "curl -X POST \"$API_BASE/analyze-usage\" \\"
echo "  -H \"Content-Type: application/json\" \\"
echo "  -d '{"
echo "    \"user_id\": \"minimal_user\","
echo "    \"total_screen_time\": 90,"
echo "    \"unlock_count\": 20,"
echo "    \"app_usage\": ["
echo "      {\"app\": \"chrome\", \"minutes\": 30},"
echo "      {\"app\": \"whatsapp\", \"minutes\": 25},"
echo "      {\"app\": \"gmail\", \"minutes\": 20},"
echo "      {\"app\": \"maps\", \"minutes\": 15}"
echo "    ],"
echo "    \"sessions\": ["
echo "      {\"start\": \"08:00\", \"end\": \"08:30\"},"
echo "      {\"start\": \"12:00\", \"end\": \"12:15\"},"
echo "      {\"start\": \"18:00\", \"end\": \"18:45\"}"
echo "    ],"
echo "    \"notifications\": {"
echo "      \"whatsapp\": 8,"
echo "      \"gmail\": 5"
echo "    }"
echo "  }'"
echo ""

curl -X POST "$API_BASE/analyze-usage" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "minimal_user",
    "total_screen_time": 90,
    "unlock_count": 20,
    "app_usage": [
      {"app": "chrome", "minutes": 30},
      {"app": "whatsapp", "minutes": 25},
      {"app": "gmail", "minutes": 20},
      {"app": "maps", "minutes": 15}
    ],
    "sessions": [
      {"start": "08:00", "end": "08:30"},
      {"start": "12:00", "end": "12:15"},
      {"start": "18:00", "end": "18:45"}
    ],
    "notifications": {
      "whatsapp": 8,
      "gmail": 5
    }
  }'
echo ""

# Test Case 4: Gaming User
echo ""
echo "6. Gaming User Test:"
echo "curl -X POST \"$API_BASE/analyze-usage\" \\"
echo "  -H \"Content-Type: application/json\" \\"
echo "  -d '{"
echo "    \"user_id\": \"gamer_user\","
echo "    \"total_screen_time\": 420,"
echo "    \"unlock_count\": 45,"
echo "    \"app_usage\": ["
echo "      {\"app\": \"pubg_mobile\", \"minutes\": 180},"
echo "      {\"app\": \"among_us\", \"minutes\": 120},"
echo "      {\"app\": \"discord\", \"minutes\": 60},"
echo "      {\"app\": \"youtube\", \"minutes\": 60}"
echo "    ],"
echo "    \"sessions\": ["
echo "      {\"start\": \"15:00\", \"end\": \"19:00\"},"
echo "      {\"start\": \"20:00\", \"end\": \"23:30\"},"
echo "      {\"start\": \"00:00\", \"end\": \"03:00\"}"
echo "    ],"
echo "    \"notifications\": {"
echo "      \"discord\": 40,"
echo "      \"pubg_mobile\": 20"
echo "    }"
echo "  }'"
echo ""

curl -X POST "$API_BASE/analyze-usage" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "gamer_user",
    "total_screen_time": 420,
    "unlock_count": 45,
    "app_usage": [
      {"app": "pubg_mobile", "minutes": 180},
      {"app": "among_us", "minutes": 120},
      {"app": "discord", "minutes": 60},
      {"app": "youtube", "minutes": 60}
    ],
    "sessions": [
      {"start": "15:00", "end": "19:00"},
      {"start": "20:00", "end": "23:30"},
      {"start": "00:00", "end": "03:00"}
    ],
    "notifications": {
      "discord": 40,
      "pubg_mobile": 20
    }
  }'
echo ""

# Error Test Cases
echo ""
echo "7. Error Handling Tests:"
echo ""

# Missing required fields
echo "7a. Missing Required Fields:"
echo "curl -X POST \"$API_BASE/analyze-usage\" \\"
echo "  -H \"Content-Type: application/json\" \\"
echo "  -d '{\"user_id\": \"test\", \"total_screen_time\": 100}'"
echo ""

curl -X POST "$API_BASE/analyze-usage" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test", "total_screen_time": 100}'
echo ""

# Invalid time format
echo "7b. Invalid Time Format:"
echo "curl -X POST \"$API_BASE/analyze-usage\" \\"
echo "  -H \"Content-Type: application/json\" \\"
echo "  -d '{"
echo "    \"user_id\": \"test\","
echo "    \"total_screen_time\": 100,"
echo "    \"unlock_count\": 10,"
echo "    \"app_usage\": [{\"app\": \"test\", \"minutes\": 50}],"
echo "    \"sessions\": [{\"start\": \"25:00\", \"end\": \"26:00\"}],"
echo "    \"notifications\": {\"test\": 5}"
echo "  }'"
echo ""

curl -X POST "$API_BASE/analyze-usage" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test",
    "total_screen_time": 100,
    "unlock_count": 10,
    "app_usage": [{"app": "test", "minutes": 50}],
    "sessions": [{"start": "25:00", "end": "26:00"}],
    "notifications": {"test": 5}
  }'
echo ""

# Negative values
echo "7c. Negative Values:"
echo "curl -X POST \"$API_BASE/analyze-usage\" \\"
echo "  -H \"Content-Type: application/json\" \\"
echo "  -d '{"
echo "    \"user_id\": \"test\","
echo "    \"total_screen_time\": -100,"
echo "    \"unlock_count\": 10,"
echo "    \"app_usage\": [{\"app\": \"test\", \"minutes\": 50}],"
echo "    \"sessions\": [{\"start\": \"09:00\", \"end\": \"10:00\"}],"
echo "    \"notifications\": {\"test\": 5}"
echo "  }'"
echo ""

curl -X POST "$API_BASE/analyze-usage" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test",
    "total_screen_time": -100,
    "unlock_count": 10,
    "app_usage": [{"app": "test", "minutes": 50}],
    "sessions": [{"start": "09:00", "end": "10:00"}],
    "notifications": {"test": 5}
  }'
echo ""

echo ""
echo "=================================================="
echo "🎉 All curl commands completed!"
echo ""
echo "📖 API Documentation: $API_BASE/docs"
echo "🔍 ReDoc Documentation: $API_BASE/redoc"
echo "💡 Use these commands to test different user scenarios!"
