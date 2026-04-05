# AI Digital Wellbeing App

A comprehensive Android application that tracks user digital habits and provides AI-powered insights for better digital wellness.

## 🚀 Features

### Core Functionality
- **Screen Time Tracking**: Monitor total screen time over the last 24 hours
- **Unlock Count**: Track how many times the device was unlocked
- **App Usage Statistics**: Detailed usage data for each installed application
- **Notification Monitoring**: Count and track notifications from all apps
- **Usage Sessions**: Identify usage patterns and session durations

### Technical Implementation
- **Modern Material 3 UI**: Sleek, responsive interface with Material Design components
- **API Integration**: Retrofit 2 with Gson for server communication
- **Permission Management**: Comprehensive handling of sensitive permissions
- **Background Services**: Notification listener service for real-time tracking
- **Error Handling**: Robust error handling with user-friendly messages

## 📱 Screenshots

The app features:
- **Dashboard**: Overview cards showing screen time, unlocks, and notifications
- **App Usage List**: Detailed breakdown of app usage with icons and time spent
- **Permission Flow**: Guided permission request process
- **Loading States**: Smooth loading animations and progress indicators
- **Error States**: Clear error messages and recovery options

## 🏗️ Architecture

### Data Layer
- **UsageData**: Main data model containing all usage statistics
- **AppUsage**: Individual app usage information
- **Session**: Usage session tracking with start/end times

### API Layer
- **ApiService**: Retrofit interface for server communication
- **ApiClient**: Singleton for API client management
- **POST /analyze-usage**: Endpoint for sending usage data to AI backend

### Service Layer
- **NotificationListenerService**: Background service for notification tracking
- **UsageStatsManagerUtil**: Utility for extracting usage statistics

### UI Layer
- **MainActivity**: Main dashboard with Material 3 components
- **AppUsageAdapter**: RecyclerView adapter for app usage list
- **Material Components**: Cards, buttons, dialogs, and snackbars

## 🔧 Setup Instructions

### 1. Dependencies
The app uses the following key dependencies:
```gradle
// Material 3
implementation 'com.google.android.material:material:1.12.0'

// Retrofit & Gson
implementation 'com.squareup.retrofit2:retrofit:2.9.0'
implementation 'com.squareup.retrofit2:converter-gson:2.9.0'

// RecyclerView & SwipeRefreshLayout
implementation 'androidx.recyclerview:recyclerview:1.3.2'
implementation 'androidx.swiperefreshlayout:swiperefreshlayout:1.1.0'

// Lottie Animations (Optional)
implementation 'com.airbnb.android:lottie:6.1.0'
```

### 2. Permissions
The app requires these sensitive permissions:

#### Usage Stats Permission
```xml
<uses-permission android:name="android.permission.PACKAGE_USAGE_STATS"
    tools:ignore="ProtectedPermissions" />
```

#### Notification Listener Permission
```xml
<uses-permission android:name="android.permission.BIND_NOTIFICATION_LISTENER_SERVICE" />
```

### 3. API Configuration
Update the `BASE_URL` in `ApiClient.java`:
```java
private static final String BASE_URL = "https://your-api-base-url.com/api/";
```

## 📊 Data Flow

### 1. Data Collection
- **Usage Events**: Query `UsageEvents` for foreground/background transitions
- **Screen Time**: Calculate total time in foreground across all apps
- **Unlock Count**: Count `KEYGUARD_DISMISSED` events
- **Notifications**: Track via `NotificationListenerService`

### 2. Data Processing
- **Session Detection**: Identify usage sessions with gaps > 1 minute
- **App Ranking**: Sort apps by usage time (descending)
- **User ID**: Use `Settings.Secure.ANDROID_ID` as unique identifier

### 3. API Communication
```json
{
  "user_id": "android_id_string",
  "total_screen_time": 3600,
  "unlock_count": 45,
  "app_usage": [
    {
      "package_name": "com.example.app",
      "app_name": "Example App",
      "usage_time": 1800000,
      "last_used": 1640995200000
    }
  ],
  "sessions": [
    {
      "start_time": 1640995200000,
      "end_time": 1640995800000,
      "duration": 600000
    }
  ],
  "notifications": {
    "com.example.app": 5,
    "com.another.app": 3
  }
}
```

## 🎯 Key Features Explained

### Permission Handling
- **Automatic Detection**: Checks for required permissions on startup
- **Guided Flow**: Directs users to appropriate settings screens
- **Real-time Updates**: Rechecks permissions after user returns from settings

### Modern UI Components
- **MaterialCardView**: For stats and app usage cards
- **SwipeRefreshLayout**: For manual data refresh
- **RecyclerView**: Efficient list display with Material 3 styling
- **ProgressBar**: Loading state with smooth animations
- **Snackbar**: Non-intrusive error and success messages

### Error Handling
- **Network Errors**: Graceful handling of API failures
- **Permission Errors**: Clear messaging and recovery options
- **Data Errors**: Fallback states and user guidance
- **Background Errors**: Thread-safe error reporting

## 🔒 Privacy & Security

### Data Protection
- **Local Processing**: Usage data processed locally before API transmission
- **Secure ID**: Uses Android ID instead of device identifiers
- **Minimal Data**: Only collects necessary usage statistics
- **User Control**: Full permission control and revocation

### Best Practices
- **Background Execution**: Proper background service management
- **Memory Management**: Efficient data structures and cleanup
- **Battery Optimization**: Minimal impact on battery life
- **User Privacy**: No sensitive personal data collected

## 🚀 Getting Started

### 1. Clone & Build
```bash
git clone <repository-url>
cd AiDigitalWellbeing
./gradlew build
```

### 2. Install & Run
```bash
./gradlew installDebug
```

### 3. Grant Permissions
- Open the app
- Follow the permission request flow
- Grant Usage Stats access in Settings
- Enable Notification Listener service

### 4. Configure API
- Update `BASE_URL` in `ApiClient.java`
- Ensure your API endpoint is accessible
- Test the `/analyze-usage` endpoint

## 🐛 Troubleshooting

### Common Issues

#### Permission Not Granted
- Ensure Usage Stats permission is enabled in Settings > Apps > Special Access
- Check Notification Listener is enabled in Settings > Notifications

#### API Connection Failed
- Verify `BASE_URL` is correct and accessible
- Check network connectivity
- Review API endpoint implementation

#### Data Not Loading
- Ensure all permissions are granted
- Check if Usage Stats service is enabled
- Verify app has background processing permissions

#### UI Issues
- Ensure Material 3 theme is properly applied
- Check layout constraints and dimensions
- Verify RecyclerView adapter setup

## 📈 Performance Considerations

### Optimization
- **Background Threading**: All data processing on background threads
- **Memory Efficiency**: Minimal object creation and proper cleanup
- **UI Responsiveness**: Main thread only for UI updates
- **Battery Life**: Efficient usage stats queries

### Best Practices
- **Lazy Loading**: Load data only when needed
- **Caching**: Cache results to avoid repeated queries
- **Batching**: Group API calls when possible
- **Cleanup**: Proper service and listener management

## 🔄 Future Enhancements

### Planned Features
- **Weekly/Monthly Views**: Extended time range analysis
- **Goal Setting**: Digital wellness goals and tracking
- **Trends Analysis**: Usage pattern recognition
- **Export Data**: CSV/PDF export functionality
- **Widgets**: Home screen widgets for quick stats

### Technical Improvements
- **WorkManager**: Replace custom threading with WorkManager
- **Room Database**: Local data persistence
- **Coroutines**: Modern async programming
- **Dependency Injection**: Hilt or Dagger integration
- **MVVM Architecture**: ViewModel and LiveData implementation

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For issues and questions:
- Create an issue in the repository
- Check existing issues for solutions
- Review documentation and troubleshooting section

---

**Built with ❤️ using Java, Material 3, and modern Android development practices**
