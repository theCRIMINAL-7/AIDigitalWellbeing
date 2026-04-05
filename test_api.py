#!/usr/bin/env python3
"""
Test script for Digital Wellbeing AI Engine API
"""

import requests
import json
import time

API_BASE_URL = "http://127.0.0.1:8000"

def test_health_check():
    """Test the health check endpoint."""
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        print(f"Health Check Status: {response.status_code}")
        print(f"Health Check Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_usage_analysis():
    """Test the main usage analysis endpoint with sample data."""
    
    # Test case 1: High usage user
    high_usage_data = {
        "user_id": "test_user_high",
        "total_screen_time": 480,  # 8 hours
        "unlock_count": 120,
        "app_usage": [
            {"app": "instagram", "minutes": 200},
            {"app": "tiktok", "minutes": 150},
            {"app": "youtube", "minutes": 80},
            {"app": "whatsapp", "minutes": 50}
        ],
        "sessions": [
            {"start": "08:00", "end": "10:30"},
            {"start": "12:00", "end": "14:00"},
            {"start": "16:00", "end": "18:30"},
            {"start": "20:00", "end": "23:00"},
            {"start": "00:00", "end": "02:00"}
        ],
        "notifications": {
            "instagram": 60,
            "tiktok": 45,
            "whatsapp": 25
        }
    }
    
    # Test case 2: Moderate usage user
    moderate_usage_data = {
        "user_id": "test_user_moderate",
        "total_screen_time": 240,  # 4 hours
        "unlock_count": 60,
        "app_usage": [
            {"app": "chrome", "minutes": 80},
            {"app": "whatsapp", "minutes": 60},
            {"app": "youtube", "minutes": 50},
            {"app": "gmail", "minutes": 30},
            {"app": "instagram", "minutes": 20}
        ],
        "sessions": [
            {"start": "09:00", "end": "10:30"},
            {"start": "14:00", "end": "15:30"},
            {"start": "19:00", "end": "21:00"}
        ],
        "notifications": {
            "whatsapp": 20,
            "gmail": 15,
            "instagram": 10
        }
    }
    
    # Test case 3: Low usage user
    low_usage_data = {
        "user_id": "test_user_low",
        "total_screen_time": 120,  # 2 hours
        "unlock_count": 25,
        "app_usage": [
            {"app": "chrome", "minutes": 40},
            {"app": "whatsapp", "minutes": 30},
            {"app": "gmail", "minutes": 25},
            {"app": "maps", "minutes": 15},
            {"app": "calculator", "minutes": 10}
        ],
        "sessions": [
            {"start": "08:00", "end": "08:45"},
            {"start": "12:00", "end": "12:30"},
            {"start": "18:00", "end": "19:15"}
        ],
        "notifications": {
            "whatsapp": 8,
            "gmail": 12
        }
    }
    
    test_cases = [
        ("High Usage User", high_usage_data),
        ("Moderate Usage User", moderate_usage_data),
        ("Low Usage User", low_usage_data)
    ]
    
    results = []
    
    for case_name, test_data in test_cases:
        print(f"\n{'='*50}")
        print(f"Testing: {case_name}")
        print(f"{'='*50}")
        
        try:
            response = requests.post(
                f"{API_BASE_URL}/analyze-usage",
                json=test_data,
                headers={"Content-Type": "application/json"}
            )
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"Addiction Score: {result['addiction_score']}")
                print(f"Risk Level: {result['risk_level']}")
                print(f"Patterns Detected: {len(result['patterns'])}")
                for pattern in result['patterns']:
                    print(f"  - {pattern}")
                print(f"Recommendations: {len(result['recommendations'])}")
                for rec in result['recommendations'][:3]:  # Show first 3
                    print(f"  - {rec}")
                print(f"Most Used App: {result['insights']['most_used_app']}")
                print(f"Peak Usage: {result['insights']['peak_usage_period']}")
                
                results.append({
                    "case": case_name,
                    "score": result['addiction_score'],
                    "risk": result['risk_level'],
                    "status": "success"
                })
            else:
                print(f"Error: {response.status_code} - {response.text}")
                results.append({
                    "case": case_name,
                    "status": "failed",
                    "error": response.text
                })
                
        except Exception as e:
            print(f"Request failed: {e}")
            results.append({
                "case": case_name,
                "status": "error",
                "error": str(e)
            })
    
    return results

def test_invalid_data():
    """Test API with invalid data to ensure proper error handling."""
    
    print(f"\n{'='*50}")
    print("Testing Invalid Data Handling")
    print(f"{'='*50}")
    
    # Test case 1: Missing required fields
    invalid_data_1 = {
        "user_id": "test_invalid",
        "total_screen_time": 100
        # Missing other required fields
    }
    
    # Test case 2: Invalid time format
    invalid_data_2 = {
        "user_id": "test_invalid",
        "total_screen_time": 100,
        "unlock_count": 10,
        "app_usage": [{"app": "test", "minutes": 50}],
        "sessions": [{"start": "25:00", "end": "26:00"}],  # Invalid time
        "notifications": {"test": 5}
    }
    
    # Test case 3: Negative values
    invalid_data_3 = {
        "user_id": "test_invalid",
        "total_screen_time": -100,  # Negative
        "unlock_count": 10,
        "app_usage": [{"app": "test", "minutes": 50}],
        "sessions": [{"start": "09:00", "end": "10:00"}],
        "notifications": {"test": 5}
    }
    
    invalid_cases = [
        ("Missing Fields", invalid_data_1),
        ("Invalid Time Format", invalid_data_2),
        ("Negative Values", invalid_data_3)
    ]
    
    for case_name, test_data in invalid_cases:
        print(f"\nTesting: {case_name}")
        try:
            response = requests.post(
                f"{API_BASE_URL}/analyze-usage",
                json=test_data,
                headers={"Content-Type": "application/json"}
            )
            print(f"Status Code: {response.status_code}")
            if response.status_code != 200:
                print(f"✅ Properly rejected: {response.status_code}")
            else:
                print(f"❌ Should have been rejected but was accepted")
        except Exception as e:
            print(f"Request failed: {e}")

def main():
    """Run all tests."""
    print("🧪 Digital Wellbeing AI Engine API Tests")
    print("=" * 60)
    
    # Test health check first
    if not test_health_check():
        print("❌ API is not running. Please start the server first:")
        print("   uvicorn main:app --reload")
        return
    
    print("✅ API is running")
    
    # Test main functionality
    results = test_usage_analysis()
    
    # Test error handling
    test_invalid_data()
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 Test Summary")
    print(f"{'='*60}")
    
    successful_tests = sum(1 for r in results if r.get('status') == 'success')
    total_tests = len(results)
    
    print(f"Successful Tests: {successful_tests}/{total_tests}")
    
    for result in results:
        if result.get('status') == 'success':
            print(f"✅ {result['case']}: Score {result['score']} ({result['risk']})")
        else:
            print(f"❌ {result['case']}: {result.get('error', 'Unknown error')}")
    
    print(f"\n🎉 Testing completed!")
    print(f"📖 API Documentation: {API_BASE_URL}/docs")
    print(f"🔍 Interactive UI: {API_BASE_URL}/redoc")

if __name__ == "__main__":
    main()
