import 'package:kakao_flutter_sdk/kakao_flutter_sdk.dart';
import 'package:flutter/services.dart';
import 'api_service.dart';

class KakaoAuthService {
  static bool _isInitialized = false;

  static Future<void> initialize() async {
    if (_isInitialized) return;
    
    // 카카오 SDK 초기화
    KakaoSdk.init(
      nativeAppKey: 'fc9248fb37c47471e8ac96d2336946f2',
    );
    _isInitialized = true;
  }

  /// 카카오 로그인
  static Future<Map<String, dynamic>?> loginWithKakao() async {
    try {
      // 네트워크 연결 확인
      print('카카오 로그인 시도 중...');
      
      // 카카오톡이 설치되어 있는지 확인
      if (await isKakaoTalkInstalled()) {
        try {
          // 카카오톡으로 로그인
          OAuthToken token = await UserApi.instance.loginWithKakaoTalk();
          return await _handleKakaoLoginSuccess(token);
        } catch (error) {
          print('카카오톡 로그인 실패: $error');
          // 카카오톡 로그인 실패 시 웹으로 로그인
          if (error is PlatformException && error.code == 'CANCELLED') {
            return null; // 사용자가 취소한 경우
          }
          try {
            OAuthToken token = await UserApi.instance.loginWithKakaoAccount();
            return await _handleKakaoLoginSuccess(token);
          } catch (webError) {
            print('카카오 웹 로그인 실패: $webError');
            return null;
          }
        }
      } else {
        // 카카오톡이 설치되지 않은 경우 웹으로 로그인
        try {
          OAuthToken token = await UserApi.instance.loginWithKakaoAccount();
          return await _handleKakaoLoginSuccess(token);
        } catch (error) {
          print('카카오 웹 로그인 실패: $error');
          return null;
        }
      }
    } catch (error) {
      print('카카오 로그인 실패: $error');
      return null;
    }
  }

  /// 카카오 로그인 성공 처리
  static Future<Map<String, dynamic>?> _handleKakaoLoginSuccess(OAuthToken token) async {
    try {
      // 사용자 정보 가져오기
      User user = await UserApi.instance.me();
      
      // 백엔드에 카카오 로그인 정보 전송
      return await _sendKakaoLoginToBackend(user, token);
    } catch (error) {
      print('사용자 정보 가져오기 실패: $error');
      return null;
    }
  }

  /// 백엔드에 카카오 로그인 정보 전송
  static Future<Map<String, dynamic>?> _sendKakaoLoginToBackend(User user, OAuthToken token) async {
    try {
      final response = await ApiService.kakaoLogin(
        kakaoId: user.id.toString(),
        email: user.kakaoAccount?.email,
        nickname: user.kakaoAccount?.profile?.nickname ?? user.kakaoAccount?.name,
        profileImage: user.kakaoAccount?.profile?.profileImageUrl,
        accessToken: token.accessToken,
      );
      return response;
    } catch (error) {
      print('백엔드 카카오 로그인 실패: $error');
      return null;
    }
  }

  /// 로그아웃
  static Future<void> logout() async {
    try {
      await UserApi.instance.logout();
      ApiService.clearAccessToken();
    } catch (error) {
      print('카카오 로그아웃 실패: $error');
    }
  }

  /// 현재 로그인 상태 확인
  static Future<bool> isLoggedIn() async {
    try {
      return await AuthApi.instance.hasToken();
    } catch (error) {
      return false;
    }
  }

  /// 현재 사용자 정보 가져오기
  static Future<User?> getCurrentUser() async {
    try {
      if (await isLoggedIn()) {
        return await UserApi.instance.me();
      }
      return null;
    } catch (error) {
      print('사용자 정보 가져오기 실패: $error');
      return null;
    }
  }
}
