from typing import List, Dict
from models import AppUsage


class RecommendationEngine:
    def __init__(self):
        self.recommendation_templates = {
            'screen_time_reduction': [
                "Set a daily screen time limit of {target} minutes",
                "Use app timers to limit usage to {target} minutes per day",
                "Enable digital wellbeing reminders after {target} minutes of usage",
                "Schedule screen-free periods during your day"
            ],
            'social_media_control': [
                "Limit social media apps to {target} minutes per day",
                "Disable notifications for social media apps",
                "Use grayscale mode to reduce social media engagement",
                "Schedule specific times for social media checking"
            ],
            'night_usage': [
                "Enable bedtime mode from 22:00 to 06:00",
                "Set up app blocking during night hours",
                "Use blue light filter after sunset",
                "Keep phone out of bedroom during sleep hours"
            ],
            'session_management': [
                "Take a 5-minute break every {target} minutes of usage",
                "Use Pomodoro technique for phone usage",
                "Set up automatic session reminders",
                "Practice the 20-20-20 rule during long sessions"
            ],
            'unlock_behavior': [
                "Disable unnecessary notifications to reduce unlocks",
                "Organize apps to minimize accidental opens",
                "Use app folders to reduce mindless scrolling",
                "Set up focus mode during work hours"
            ],
            'app_specific': [
                "Set daily limits for {app_name} ({target} minutes)",
                "Move {app_name} off your home screen",
                "Disable notifications for {app_name}",
                "Use alternative apps with better time management"
            ],
            'general_wellbeing': [
                "Schedule regular digital detox periods",
                "Engage in offline hobbies and activities",
                "Practice mindfulness before phone usage",
                "Set up phone-free zones in your home"
            ]
        }
    
    def generate_recommendations(self, features: Dict, patterns: List[str], 
                               app_usage: List[AppUsage]) -> List[str]:
        """
        Generate personalized recommendations based on features and patterns.
        
        Args:
            features: Dictionary containing computed features
            patterns: List of detected patterns
            app_usage: List of app usage data
            
        Returns:
            List of personalized recommendations
        """
        recommendations = []
        
        # Screen time recommendations
        if features['total_screen_time'] > 300:  # > 5 hours
            target = max(120, features['total_screen_time'] - 120)  # Reduce by 2 hours
            recommendations.append(
                self.recommendation_templates['screen_time_reduction'][0].format(target=target)
            )
        
        # Social media recommendations
        if features['social_media_ratio'] > 40:  # > 40% social media
            target = max(30, int(features['total_screen_time'] * 0.3))  # 30% of total time
            recommendations.append(
                self.recommendation_templates['social_media_control'][0].format(target=target)
            )
            recommendations.append(self.recommendation_templates['social_media_control'][1])
        
        # Night usage recommendations
        night_ratio = (features['night_usage'] / max(features['total_screen_time'], 1)) * 100
        if night_ratio > 20:  # > 20% night usage
            recommendations.append(self.recommendation_templates['night_usage'][0])
            recommendations.append(self.recommendation_templates['night_usage'][3])
        
        # Session management recommendations
        if features['avg_session_duration'] > 45:  # > 45 minutes average
            target = 30  # Break every 30 minutes
            recommendations.append(
                self.recommendation_templates['session_management'][0].format(target=target)
            )
        
        # Unlock behavior recommendations
        if features['unlock_frequency'] > 8:  # > 8 unlocks per hour
            recommendations.append(self.recommendation_templates['unlock_behavior'][0])
            recommendations.append(self.recommendation_templates['unlock_behavior'][2])
        
        # Pattern-specific recommendations
        pattern_recs = self._get_pattern_specific_recommendations(patterns)
        recommendations.extend(pattern_recs)
        
        # App-specific recommendations
        app_recs = self._get_app_specific_recommendations(app_usage, features)
        recommendations.extend(app_recs)
        
        # General wellbeing recommendations
        if features['total_screen_time'] > 240:  # > 4 hours
            recommendations.append(self.recommendation_templates['general_wellbeing'][0])
        
        # Limit to top 5 most relevant recommendations
        return recommendations[:5]
    
    def _get_pattern_specific_recommendations(self, patterns: List[str]) -> List[str]:
        """Get recommendations based on detected patterns."""
        recommendations = []
        
        for pattern in patterns:
            if "High night usage" in pattern:
                recommendations.append(self.recommendation_templates['night_usage'][1])
            elif "Long continuous sessions" in pattern:
                recommendations.append(self.recommendation_templates['session_management'][2])
            elif "Frequent phone checking" in pattern:
                recommendations.append(self.recommendation_templates['unlock_behavior'][3])
            elif "Social media dominance" in pattern:
                recommendations.append(self.recommendation_templates['social_media_control'][2])
            elif "Usage spikes" in pattern:
                recommendations.append(self.recommendation_templates['session_management'][3])
            elif "Binge usage" in pattern:
                recommendations.append(self.recommendation_templates['general_wellbeing'][1])
            elif "notification-driven" in pattern:
                recommendations.append(self.recommendation_templates['unlock_behavior'][1])
        
        return recommendations
    
    def _get_app_specific_recommendations(self, app_usage: List[AppUsage], 
                                       features: Dict) -> List[str]:
        """Get app-specific recommendations for most used apps."""
        recommendations = []
        
        if not app_usage:
            return recommendations
        
        # Sort apps by usage time
        sorted_apps = sorted(app_usage, key=lambda x: x.minutes, reverse=True)
        
        # Get top 2 most used apps
        for app in sorted_apps[:2]:
            if app.minutes > 60:  # Only if app usage > 1 hour
                target = max(15, app.minutes // 2)  # Reduce by half, minimum 15 minutes
                recommendations.append(
                    self.recommendation_templates['app_specific'][0].format(
                        app_name=app.app, target=target
                    )
                )
        
        return recommendations
    
    def get_recommendation_priority(self, recommendation: str, features: Dict) -> int:
        """
        Get priority score for a recommendation (higher = more important).
        
        Args:
            recommendation: The recommendation text
            features: Dictionary containing computed features
            
        Returns:
            Priority score (1-10)
        """
        priority = 5  # Base priority
        
        # Increase priority for severe issues
        if features['total_screen_time'] > 480:  # > 8 hours
            priority += 2
        
        if features['social_media_ratio'] > 70:  # > 70% social media
            priority += 2
        
        night_ratio = (features['night_usage'] / max(features['total_screen_time'], 1)) * 100
        if night_ratio > 40:  # > 40% night usage
            priority += 2
        
        if features['unlock_frequency'] > 15:  # > 15 unlocks per hour
            priority += 1
        
        return min(10, priority)
    
    def categorize_recommendations(self, recommendations: List[str]) -> Dict[str, List[str]]:
        """
        Categorize recommendations by type.
        
        Args:
            recommendations: List of recommendation strings
            
        Returns:
            Dictionary with categorized recommendations
        """
        categories = {
            'Time Management': [],
            'App Control': [],
            'Behavior Change': [],
            'Wellbeing': []
        }
        
        for rec in recommendations:
            rec_lower = rec.lower()
            if any(keyword in rec_lower for keyword in ['limit', 'timer', 'minutes', 'break']):
                categories['Time Management'].append(rec)
            elif any(keyword in rec_lower for keyword in ['app', 'notification', 'block']):
                categories['App Control'].append(rec)
            elif any(keyword in rec_lower for keyword in ['focus', 'mode', 'habit', 'organize']):
                categories['Behavior Change'].append(rec)
            else:
                categories['Wellbeing'].append(rec)
        
        return categories
