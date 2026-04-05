from typing import Dict, Tuple
from models import Explanation


class ScoringEngine:
    def __init__(self):
        self.weights = {
            'screen_time': 0.30,
            'social_media': 0.25,
            'night_usage': 0.20,
            'unlock_frequency': 0.15,
            'session_duration': 0.10
        }
        
        # Normalization parameters (max values for normalization)
        self.max_values = {
            'screen_time': 480,  # 8 hours
            'social_media_ratio': 100,  # 100%
            'night_usage_ratio': 50,  # 50% of total usage
            'unlock_frequency': 20,  # 20 unlocks per hour
            'avg_session_duration': 120  # 2 hours
        }
    
    def calculate_addiction_score(self, features: Dict) -> Tuple[float, Explanation]:
        """
        Calculate addiction score based on weighted features.
        
        Args:
            features: Dictionary containing all computed features
            
        Returns:
            Tuple of (addiction_score, explanation)
        """
        # Normalize each feature to 0-100 scale
        normalized_scores = {}
        
        # Screen time normalization
        screen_time_score = min(100, (features['total_screen_time'] / self.max_values['screen_time']) * 100)
        normalized_scores['screen_time'] = screen_time_score
        
        # Social media ratio normalization
        social_media_score = min(100, (features['social_media_ratio'] / self.max_values['social_media_ratio']) * 100)
        normalized_scores['social_media'] = social_media_score
        
        # Night usage ratio normalization
        night_usage_ratio = (features['night_usage'] / max(features['total_screen_time'], 1)) * 100
        night_usage_score = min(100, (night_usage_ratio / self.max_values['night_usage_ratio']) * 100)
        normalized_scores['night_usage'] = night_usage_score
        
        # Unlock frequency normalization
        unlock_freq_score = min(100, (features['unlock_frequency'] / self.max_values['unlock_frequency']) * 100)
        normalized_scores['unlock_frequency'] = unlock_freq_score
        
        # Average session duration normalization
        session_duration_score = min(100, (features['avg_session_duration'] / self.max_values['avg_session_duration']) * 100)
        normalized_scores['session_duration'] = session_duration_score
        
        # Calculate weighted score
        addiction_score = (
            normalized_scores['screen_time'] * self.weights['screen_time'] +
            normalized_scores['social_media'] * self.weights['social_media'] +
            normalized_scores['night_usage'] * self.weights['night_usage'] +
            normalized_scores['unlock_frequency'] * self.weights['unlock_frequency'] +
            normalized_scores['session_duration'] * self.weights['session_duration']
        )
        
        # Create explanation with percentage contributions
        explanation = self._create_explanation(normalized_scores, addiction_score)
        
        return min(100, max(0, addiction_score)), explanation
    
    def get_risk_level(self, addiction_score: float) -> str:
        """Determine risk level based on addiction score."""
        if addiction_score < 40:
            return "Low"
        elif addiction_score <= 70:
            return "Moderate"
        else:
            return "High"
    
    def _create_explanation(self, normalized_scores: Dict, total_score: float) -> Explanation:
        """Create explanation showing percentage contribution of each factor."""
        if total_score == 0:
            return Explanation(
                screen_time=0.0,
                social_media=0.0,
                night_usage=0.0,
                unlock_behavior=0.0,
                session_behavior=0.0
            )
        
        # Calculate percentage contributions
        contributions = {}
        contributions['screen_time'] = (normalized_scores['screen_time'] * self.weights['screen_time'] / total_score) * 100
        contributions['social_media'] = (normalized_scores['social_media'] * self.weights['social_media'] / total_score) * 100
        contributions['night_usage'] = (normalized_scores['night_usage'] * self.weights['night_usage'] / total_score) * 100
        contributions['unlock_frequency'] = (normalized_scores['unlock_frequency'] * self.weights['unlock_frequency'] / total_score) * 100
        contributions['session_duration'] = (normalized_scores['session_duration'] * self.weights['session_duration'] / total_score) * 100
        
        # Normalize to ensure they sum to 100
        total_contribution = sum(contributions.values())
        if total_contribution > 0:
            for key in contributions:
                contributions[key] = (contributions[key] / total_contribution) * 100
        
        return Explanation(
            screen_time=round(contributions['screen_time'], 1),
            social_media=round(contributions['social_media'], 1),
            night_usage=round(contributions['night_usage'], 1),
            unlock_behavior=round(contributions['unlock_frequency'], 1),
            session_behavior=round(contributions['session_duration'], 1)
        )
    
    def detect_anomalies(self, features: Dict) -> list:
        """
        Detect anomalies in usage patterns.
        
        Args:
            features: Dictionary containing all computed features
            
        Returns:
            List of detected anomalies
        """
        anomalies = []
        
        # Extremely high screen time
        if features['total_screen_time'] > 600:  # > 10 hours
            anomalies.append("Extremely high screen time detected")
        
        # Very high unlock frequency
        if features['unlock_frequency'] > 30:  # > 30 unlocks per hour
            anomalies.append("Unusually high phone checking frequency")
        
        # Excessive night usage
        night_ratio = (features['night_usage'] / max(features['total_screen_time'], 1)) * 100
        if night_ratio > 60:  # > 60% of usage at night
            anomalies.append("Excessive night-time usage pattern")
        
        # Very long sessions
        if features['avg_session_duration'] > 180:  # > 3 hours average
            anomalies.append("Unusually long continuous usage sessions")
        
        # Social media dominance
        if features['social_media_ratio'] > 80:  # > 80% social media
            anomalies.append("Social media usage dominance")
        
        return anomalies
