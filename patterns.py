from typing import List, Dict
from models import Session, AppUsage


class PatternDetector:
    def __init__(self):
        self.thresholds = {
            'night_usage_ratio': 30,  # % of total usage
            'long_session_duration': 60,  # minutes
            'high_unlock_frequency': 10,  # per hour
            'social_media_dominance': 50,  # % of total usage
            'usage_spike_ratio': 2.0  # times average
        }
    
    def detect_patterns(self, features: Dict, sessions: List[Session], 
                       app_usage: List[AppUsage]) -> List[str]:
        """
        Detect usage patterns based on computed features.
        
        Args:
            features: Dictionary containing computed features
            sessions: List of usage sessions
            app_usage: List of app usage data
            
        Returns:
            List of detected patterns
        """
        patterns = []
        
        # Check for high night usage
        night_ratio = (features['night_usage'] / max(features['total_screen_time'], 1)) * 100
        if night_ratio > self.thresholds['night_usage_ratio']:
            patterns.append(f"High night usage ({night_ratio:.1f}% of total usage)")
        
        # Check for long continuous sessions
        if features['avg_session_duration'] > self.thresholds['long_session_duration']:
            patterns.append(f"Long continuous sessions (avg {features['avg_session_duration']:.1f} minutes)")
        
        # Check for frequent phone checking
        if features['unlock_frequency'] > self.thresholds['high_unlock_frequency']:
            patterns.append(f"Frequent phone checking ({features['unlock_frequency']:.1f} unlocks/hour)")
        
        # Check for social media dominance
        if features['social_media_ratio'] > self.thresholds['social_media_dominance']:
            patterns.append(f"Social media dominance ({features['social_media_ratio']:.1f}% of usage)")
        
        # Check for usage spikes
        spike_pattern = self._detect_usage_spikes(sessions)
        if spike_pattern:
            patterns.append(spike_pattern)
        
        # Check for binge patterns
        binge_pattern = self._detect_binge_patterns(sessions)
        if binge_pattern:
            patterns.append(binge_pattern)
        
        # Check for notification-driven usage
        notification_pattern = self._detect_notification_driven_usage(features)
        if notification_pattern:
            patterns.append(notification_pattern)
        
        # Check for weekend vs weekday pattern (if data suggests)
        time_pattern = self._detect_time_based_patterns(sessions)
        if time_pattern:
            patterns.append(time_pattern)
        
        return patterns
    
    def _detect_usage_spikes(self, sessions: List[Session]) -> str:
        """Detect unusual usage spikes in sessions."""
        if len(sessions) < 3:
            return ""
        
        # Calculate session durations
        durations = []
        for session in sessions:
            start_hour, start_min = map(int, session.start.split(':'))
            end_hour, end_min = map(int, session.end.split(':'))
            
            start_total = start_hour * 60 + start_min
            end_total = end_hour * 60 + end_min
            
            if end_total < start_total:
                end_total += 24 * 60
            
            duration = end_total - start_total
            durations.append(duration)
        
        if not durations:
            return ""
        
        avg_duration = sum(durations) / len(durations)
        max_duration = max(durations)
        
        if max_duration > avg_duration * self.thresholds['usage_spike_ratio']:
            return f"Usage spikes detected (max {max_duration} minutes vs avg {avg_duration:.1f} minutes)"
        
        return ""
    
    def _detect_binge_patterns(self, sessions: List[Session]) -> str:
        """Detect binge usage patterns (multiple long sessions)."""
        long_sessions = 0
        
        for session in sessions:
            start_hour, start_min = map(int, session.start.split(':'))
            end_hour, end_min = map(int, session.end.split(':'))
            
            start_total = start_hour * 60 + start_min
            end_total = end_hour * 60 + end_min
            
            if end_total < start_total:
                end_total += 24 * 60
            
            duration = end_total - start_total
            if duration > 90:  # Sessions longer than 90 minutes
                long_sessions += 1
        
        if long_sessions >= 3:
            return f"Binge usage pattern ({long_sessions} long sessions)"
        
        return ""
    
    def _detect_notification_driven_usage(self, features: Dict) -> str:
        """Detect if usage might be driven by notifications."""
        # This is a heuristic based on unlock frequency vs session count
        if features['session_count'] > 0:
            unlocks_per_session = features['unlock_count'] / features['session_count']
            if unlocks_per_session > 3:
                return "Potential notification-driven usage (high unlock-to-session ratio)"
        
        return ""
    
    def _detect_time_based_patterns(self, sessions: List[Session]) -> str:
        """Detect time-based usage patterns."""
        if not sessions:
            return ""
        
        # Count sessions by time period
        morning_count = afternoon_count = evening_count = night_count = 0
        
        for session in sessions:
            start_hour = int(session.start.split(':')[0])
            
            if 6 <= start_hour < 12:
                morning_count += 1
            elif 12 <= start_hour < 18:
                afternoon_count += 1
            elif 18 <= start_hour < 22:
                evening_count += 1
            else:
                night_count += 1
        
        total_sessions = len(sessions)
        if total_sessions == 0:
            return ""
        
        # Find dominant period
        period_counts = {
            'Morning': morning_count,
            'Afternoon': afternoon_count,
            'Evening': evening_count,
            'Night': night_count
        }
        
        dominant_period = max(period_counts, key=period_counts.get)
        dominant_percentage = (period_counts[dominant_period] / total_sessions) * 100
        
        if dominant_percentage > 50:
            return f"Peak usage during {dominant_period} ({dominant_percentage:.1f}% of sessions)"
        
        return ""
    
    def get_pattern_severity(self, patterns: List[str]) -> str:
        """Assess overall pattern severity."""
        severity_score = 0
        
        for pattern in patterns:
            if "High night usage" in pattern:
                severity_score += 3
            elif "Long continuous sessions" in pattern:
                severity_score += 2
            elif "Frequent phone checking" in pattern:
                severity_score += 2
            elif "Social media dominance" in pattern:
                severity_score += 2
            elif "Usage spikes" in pattern:
                severity_score += 1
            elif "Binge usage" in pattern:
                severity_score += 2
            elif "notification-driven" in pattern:
                severity_score += 1
        
        if severity_score >= 6:
            return "High"
        elif severity_score >= 3:
            return "Moderate"
        else:
            return "Low"
