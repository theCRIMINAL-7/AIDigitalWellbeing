from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List, Dict


class AppUsage(BaseModel):
    app: str = Field(..., description="Application name")
    minutes: int = Field(..., ge=0, description="Usage time in minutes")


class Session(BaseModel):
    start: str = Field(..., description="Session start time in HH:MM format")
    end: str = Field(..., description="Session end time in HH:MM format")

    @field_validator("start", "end")
    @classmethod
    def validate_time_format(cls, v: str) -> str:
        try:
            hour, minute = map(int, v.split(":"))
            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                raise ValueError("Invalid time format")
            return v
        except Exception:
            raise ValueError("Time must be in HH:MM format")


class UsageRequest(BaseModel):
    user_id: str = Field(..., description="Unique user identifier")
    total_screen_time: int = Field(..., ge=0, description="Total screen time in minutes")
    unlock_count: int = Field(..., ge=0, description="Number of phone unlocks")
    app_usage: List[AppUsage] = Field(
        ..., min_length=1, description="List of app usage data"
    )
    sessions: List[Session] = Field(
        ..., min_length=1, description="List of usage sessions"
    )
    notifications: Dict[str, int] = Field(
        ..., description="Notification count per app"
    )

    @model_validator(mode="after")
    def validate_total_screen_time_vs_app_usage(self):
        app_total = sum(app.minutes for app in self.app_usage)
        if self.total_screen_time < app_total:
            raise ValueError("Total screen time must be >= sum of app usage times")
        return self


class Explanation(BaseModel):
    screen_time: float = Field(
        ..., ge=0, le=100, description="Percentage contribution from screen time"
    )
    social_media: float = Field(
        ..., ge=0, le=100, description="Percentage contribution from social media"
    )
    night_usage: float = Field(
        ..., ge=0, le=100, description="Percentage contribution from night usage"
    )
    unlock_behavior: float = Field(
        ..., ge=0, le=100, description="Percentage contribution from unlock behavior"
    )
    session_behavior: float = Field(
        ..., ge=0, le=100, description="Percentage contribution from session behavior"
    )


class Insights(BaseModel):
    most_used_app: str = Field(..., description="Most used application")
    peak_usage_period: str = Field(..., description="Peak usage time period")
    usage_summary: str = Field(..., description="Summary of usage patterns")


class UsageResponse(BaseModel):
    addiction_score: float = Field(..., ge=0, le=100, description="Addiction score (0-100)")
    risk_level: str = Field(..., description="Risk level: Low, Moderate, or High")
    patterns: List[str] = Field(..., description="Detected usage patterns")
    recommendations: List[str] = Field(..., description="Personalized recommendations")
    insights: Insights = Field(..., description="Usage insights")
    explanation: Explanation = Field(..., description="Score breakdown explanation")
