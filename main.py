from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.requests import Request
from typing import Dict, Any
import logging

from models import UsageRequest, UsageResponse, Insights
from feature_engine import FeatureEngine
from scoring import ScoringEngine
from patterns import PatternDetector
from recommendations import RecommendationEngine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Digital Wellbeing AI Engine",
    description="Production-ready API for analyzing digital usage patterns and providing personalized recommendations",
    version="1.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize engines
feature_engine = FeatureEngine()
scoring_engine = ScoringEngine()
pattern_detector = PatternDetector()
recommendation_engine = RecommendationEngine()


@app.get("/")
async def root():
    """Root endpoint to check API health."""
    return {
        "message": "Digital Wellbeing AI Engine API",
        "status": "healthy",
        "version": "1.1.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/analyze-usage", response_model=UsageResponse, status_code=status.HTTP_200_OK)
async def analyze_usage(request: UsageRequest) -> UsageResponse:
    """
    Analyze digital usage patterns and provide personalized recommendations.
    
    This endpoint processes usage data in real-time and returns:
    - Addiction score (0-100)
    - Risk level classification
    - Detected patterns
    - Personalized recommendations
    - Usage insights
    - Score explanation
    """
    try:
        logger.info(f"Processing analysis request for user: {request.user_id}")
        
        # Step 1: Feature Engineering
        logger.info("Computing features...")
        features = compute_features(request)
        
        # Step 2: Pattern Detection
        logger.info("Detecting usage patterns...")
        patterns = pattern_detector.detect_patterns(
            features, request.sessions, request.app_usage
        )
        
        # Step 3: Scoring
        logger.info("Calculating addiction score...")
        addiction_score, explanation = scoring_engine.calculate_addiction_score(features)
        risk_level = scoring_engine.get_risk_level(addiction_score)
        
        # Step 4: Recommendations
        logger.info("Generating recommendations...")
        recommendations = recommendation_engine.generate_recommendations(
            features, patterns, request.app_usage
        )
        
        # Step 5: Insights
        logger.info("Generating insights...")
        insights = generate_insights(features, request)
        
        # Step 6: Anomaly Detection (bonus)
        anomalies = scoring_engine.detect_anomalies(features)
        if anomalies:
            logger.info(f"Detected anomalies: {anomalies}")
            # Add anomalies to patterns if any
            patterns.extend(anomalies)
        
        response = UsageResponse(
            addiction_score=round(addiction_score, 1),
            risk_level=risk_level,
            patterns=patterns,
            recommendations=recommendations,
            insights=insights,
            explanation=explanation
        )
        
        logger.info(f"Analysis completed for user: {request.user_id}")
        return response
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


def compute_features(request: UsageRequest) -> Dict[str, Any]:
    """Compute all features from the request data."""
    return {
        'total_screen_time': request.total_screen_time,
        'unlock_count': request.unlock_count,
        'session_count': len(request.sessions),
        'avg_session_duration': feature_engine.calculate_average_session_duration(request.sessions),
        'night_usage': feature_engine.calculate_night_usage(request.sessions),
        'social_media_ratio': feature_engine.calculate_social_media_ratio(request.app_usage),
        'unlock_frequency': feature_engine.calculate_unlock_frequency(request.unlock_count),
        'most_used_app': feature_engine.get_most_used_app(request.app_usage)
    }


def generate_insights(features: Dict[str, Any], request: UsageRequest) -> Insights:
    """Generate insights from computed features."""
    most_used_app = features['most_used_app']
    peak_usage_period = feature_engine.get_peak_usage_period(request.sessions)
    usage_summary = feature_engine.generate_usage_summary(
        features['total_screen_time'], 
        request.sessions, 
        request.app_usage
    )
    
    return Insights(
        most_used_app=most_used_app,
        peak_usage_period=peak_usage_period,
        usage_summary=usage_summary
    )


# Exception handlers
@app.exception_handler(ValueError)
async def value_error_handler(_request: Request, exc: ValueError):
    logger.error("Value error: %s", exc)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": f"Invalid input: {exc!s}"},
    )


@app.exception_handler(KeyError)
async def key_error_handler(_request: Request, exc: KeyError):
    logger.error("Key error: %s", exc)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Missing required field in request"},
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
