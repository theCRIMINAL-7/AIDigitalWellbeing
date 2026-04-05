from typing import List, Dict, Tuple
from datetime import datetime, time as dt_time
from models import AppUsage, Session


class FeatureEngine:
    def __init__(self):
        self.social_media_apps = {
            'instagram', 'facebook', 'twitter', 'tiktok', 'snapchat', 
            'youtube', 'whatsapp', 'telegram', 'linkedin', 'reddit',
            'pinterest', 'tumblr', 'wechat', 'weibo', 'line'
        }
    
    def calculate_average_session_duration(self, sessions: List[Session]) -> float:
        """Calculate average session duration in minutes."""
        if not sessions:
            return 0.0
        
        total_duration = 0
        for session in sessions:
            duration = self._calculate_session_duration(session.start, session.end)
            total_duration += duration
        
        return total_duration / len(sessions)
    
    def calculate_session_count(self, sessions: List[Session]) -> int:
        """Return number of sessions."""
        return len(sessions)
    
    def calculate_night_usage(self, sessions: List[Session]) -> int:
        """Calculate total usage during night hours (22:00-06:00)."""
        night_minutes = 0
        
        for session in sessions:
            night_minutes += self._calculate_night_session_duration(session.start, session.end)
        
        return night_minutes
    
    def get_most_used_app(self, app_usage: List[AppUsage]) -> str:
        """Find the most used application."""
        if not app_usage:
            return ""
        
        return max(app_usage, key=lambda x: x.minutes).app
    
    def calculate_social_media_ratio(self, app_usage: List[AppUsage]) -> float:
        """Calculate ratio of social media usage to total usage."""
        total_usage = sum(app.minutes for app in app_usage)
        if total_usage == 0:
            return 0.0
        
        social_media_usage = sum(
            app.minutes for app in app_usage 
            if app.app.lower() in self.social_media_apps
        )
        
        return (social_media_usage / total_usage) * 100
    
    def calculate_unlock_frequency(self, unlock_count: int) -> float:
        """Calculate unlock frequency per hour (assuming 16 waking hours)."""
        if unlock_count == 0:
            return 0.0
        
        return unlock_count / 16.0
    
    def get_peak_usage_period(self, sessions: List[Session]) -> str:
        """Determine peak usage period based on session distribution."""
        if not sessions:
            return "No data"
        
        hour_counts = {}
        for session in sessions:
            start_hour = int(session.start.split(':')[0])
            end_hour = int(session.end.split(':')[0])
            
            # Handle sessions crossing midnight
            if end_hour < start_hour:
                hours = list(range(start_hour, 24)) + list(range(0, end_hour + 1))
            else:
                hours = list(range(start_hour, end_hour + 1))
            
            for hour in hours:
                hour_counts[hour] = hour_counts.get(hour, 0) + 1
        
        if not hour_counts:
            return "No data"
        
        peak_hour = max(hour_counts, key=hour_counts.get)
        
        if 6 <= peak_hour < 12:
            return "Morning"
        elif 12 <= peak_hour < 18:
            return "Afternoon"
        elif 18 <= peak_hour < 22:
            return "Evening"
        else:
            return "Night"
    
    def _calculate_session_duration(self, start: str, end: str) -> float:
        """Calculate session duration in minutes."""
        start_hour, start_min = map(int, start.split(':'))
        end_hour, end_min = map(int, end.split(':'))
        
        start_total = start_hour * 60 + start_min
        end_total = end_hour * 60 + end_min
        
        # Handle sessions crossing midnight
        if end_total < start_total:
            end_total += 24 * 60
        
        return end_total - start_total
    
    def _calculate_night_session_duration(self, start: str, end: str) -> int:
        """Calculate night usage duration for a session (22:00-06:00)."""
        start_hour, start_min = map(int, start.split(':'))
        end_hour, end_min = map(int, end.split(':'))
        
        start_total = start_hour * 60 + start_min
        end_total = end_hour * 60 + end_min
        
        night_duration = 0
        
        # Handle sessions crossing midnight
        if end_total < start_total:
            # Part before midnight (22:00-24:00)
            if start_total < 22 * 60:
                night_duration += max(0, 24 * 60 - max(start_total, 22 * 60))
            else:
                night_duration += 24 * 60 - start_total
            
            # Part after midnight (00:00-06:00)
            night_duration += min(end_total, 6 * 60)
        else:
            # Same day session
            if start_total < 6 * 60:
                night_duration += min(end_total, 6 * 60) - start_total
            elif start_total >= 22 * 60:
                night_duration += end_total - start_total
            elif end_total > 22 * 60:
                night_duration += end_total - 22 * 60
        
        return max(0, night_duration)
    
    def generate_usage_summary(self, total_screen_time: int, sessions: List[Session], 
                             app_usage: List[AppUsage]) -> str:
        """Generate a human-readable usage summary."""
        session_count = len(sessions)
        avg_session = self.calculate_average_session_duration(sessions)
        most_used = self.get_most_used_app(app_usage)
        
        summary_parts = []
        summary_parts.append(f"{total_screen_time} minutes total screen time")
        summary_parts.append(f"{session_count} sessions")
        summary_parts.append(f"average {avg_session:.1f} minutes per session")
        
        if most_used:
            summary_parts.append(f"most used app: {most_used}")
        
        return ", ".join(summary_parts)
