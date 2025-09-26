import 'package:flutter/material.dart';
import 'theme/app_theme.dart';
import 'splash_screen.dart';
import 'location_permission_screen.dart';
import 'main_screen.dart';
import 'voice_search_loading_screen.dart';

enum AppState {
  splash,
  location,
  main,
  voiceLoading,
  recommendations,
  details,
  myProfile,
  myPage,
  error,
}

class SimpleApp extends StatefulWidget {
  const SimpleApp({super.key});

  @override
  State<SimpleApp> createState() => _SimpleAppState();
}

class _SimpleAppState extends State<SimpleApp> {
  AppState _currentState = AppState.splash;

  void _goToSplash() => setState(() => _currentState = AppState.splash);
  void _goToLocation() => setState(() => _currentState = AppState.location);
  void _goToMain() => setState(() => _currentState = AppState.main);
  void _goToVoiceLoading() => setState(() => _currentState = AppState.voiceLoading);
  void _goToRecommendations() => setState(() => _currentState = AppState.recommendations);
  void _goToDetails() => setState(() => _currentState = AppState.details);
  void _goToMyProfile() => setState(() => _currentState = AppState.myProfile);
  void _goToMyPage() => setState(() => _currentState = AppState.myPage);
  void _goToError() => setState(() => _currentState = AppState.error);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'SPark',
      theme: AppTheme.lightTheme,
      home: _buildCurrentScreen(),
    );
  }

  Widget _buildCurrentScreen() {
    switch (_currentState) {
      case AppState.splash:
        return SplashScreen(onComplete: _goToLocation);
      case AppState.location:
        return LocationPermissionScreen(
          onAllow: _goToMain,
          onDeny: _goToMain,
        );
      case AppState.main:
        return MainScreen(
          onFindOptimalParking: _goToVoiceLoading,
          onMyInfo: _goToMyProfile,
          onMyPage: _goToMyPage,
          isLoggedIn: false,
          onLogin: _goToMain,
          locationPermissionGranted: true,
        );
      case AppState.voiceLoading:
        return VoiceSearchLoadingScreen(
          onComplete: _goToRecommendations,
          onError: _goToError,
        );
      case AppState.recommendations:
        return Scaffold(
          appBar: AppBar(title: const Text('추천 결과')),
          body: const Center(child: Text('추천 결과 화면')),
        );
      case AppState.details:
        return Scaffold(
          appBar: AppBar(title: const Text('주차장 상세')),
          body: const Center(child: Text('주차장 상세 화면')),
        );
      case AppState.myProfile:
        return Scaffold(
          appBar: AppBar(title: const Text('내 정보')),
          body: const Center(child: Text('내 정보 화면')),
        );
      case AppState.myPage:
        return Scaffold(
          appBar: AppBar(title: const Text('내 페이지')),
          body: const Center(child: Text('내 페이지 화면')),
        );
      case AppState.error:
        return Scaffold(
          appBar: AppBar(title: const Text('오류')),
          body: const Center(child: Text('오류 화면')),
        );
    }
  }
}
