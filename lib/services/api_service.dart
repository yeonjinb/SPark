import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter_dotenv/flutter_dotenv.dart';

class ApiService {
  static String? _baseUrl;
  static String? _accessToken;

  static Future<void> initialize() async {
    try {
      _baseUrl = dotenv.env['API_BASE_URL'] ?? 'http://localhost:8000';
    } catch (e) {
      print('환경 변수 로드 실패, 기본값 사용: $e');
      _baseUrl = 'http://localhost:8000';
    }
  }

  static Map<String, String> get _headers => {
    'Content-Type': 'application/json',
    if (_accessToken != null) 'Authorization': 'Bearer $_accessToken',
  };

  static void setAccessToken(String token) {
    _accessToken = token;
  }

  static void clearAccessToken() {
    _accessToken = null;
  }

  // 카카오 로그인 API
  static Future<Map<String, dynamic>> kakaoLogin({
    required String kakaoId,
    String? email,
    String? nickname,
    String? profileImage,
    required String accessToken,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$_baseUrl/auth/kakao'),
        headers: _headers,
        body: json.encode({
          'kakao_id': kakaoId,
          'email': email,
          'nickname': nickname,
          'profile_image': profileImage,
          'access_token': accessToken,
        }),
      );

      final data = json.decode(response.body);
      
      if (data['ok'] == true) {
        final authData = data['data'];
        setAccessToken(authData['access_token']);
        return authData;
      } else {
        throw Exception(data['error']['message']);
      }
    } catch (e) {
      throw Exception('카카오 로그인 실패: $e');
    }
  }

  // 인증 관련 API
  static Future<Map<String, dynamic>> signup({
    required String email,
    required String password,
    required String name,
    int? age,
    int? drivingYears,
    String? preferredPowertrain,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$_baseUrl/auth/signup'),
        headers: _headers,
        body: json.encode({
          'email': email,
          'password': password,
          'name': name,
          'age': age,
          'driving_years': drivingYears,
          'preferred_powertrain': preferredPowertrain,
        }),
      );

      final data = json.decode(response.body);
      
      if (data['ok'] == true) {
        final authData = data['data'];
        setAccessToken(authData['access_token']);
        return authData;
      } else {
        throw Exception(data['error']['message']);
      }
    } catch (e) {
      throw Exception('회원가입 실패: $e');
    }
  }

  static Future<Map<String, dynamic>> login({
    required String email,
    required String password,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$_baseUrl/auth/login'),
        headers: _headers,
        body: json.encode({
          'email': email,
          'password': password,
        }),
      );

      final data = json.decode(response.body);
      
      if (data['ok'] == true) {
        final authData = data['data'];
        setAccessToken(authData['access_token']);
        return authData;
      } else {
        throw Exception(data['error']['message']);
      }
    } catch (e) {
      throw Exception('로그인 실패: $e');
    }
  }

  static Future<Map<String, dynamic>> getCurrentUser() async {
    try {
      final response = await http.get(
        Uri.parse('$_baseUrl/auth/me'),
        headers: _headers,
      );

      final data = json.decode(response.body);
      
      if (data['ok'] == true) {
        return data['data'];
      } else {
        throw Exception(data['error']['message']);
      }
    } catch (e) {
      throw Exception('사용자 정보 조회 실패: $e');
    }
  }

  // 주차장 추천 API
  static Future<List<Map<String, dynamic>>> getParkingRecommendations({
    required double userLat,
    required double userLng,
    bool isEv = false,
    double? vehicleHeightM,
    int? maxPricePerHour,
    int limit = 5,
    String? authUserId,
    double searchRadiusKm = 5.0,
    bool includeDifficulty = true,
    String? preferredStructure,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$_baseUrl/recommend'),
        headers: _headers,
        body: json.encode({
          'user_lat': userLat,
          'user_lng': userLng,
          'is_ev': isEv,
          'vehicle_height_m': vehicleHeightM,
          'max_price_per_hour': maxPricePerHour,
          'limit': limit,
          'auth_user_id': authUserId,
          'search_radius_km': searchRadiusKm,
          'include_difficulty': includeDifficulty,
          'preferred_structure': preferredStructure,
        }),
      );

      final data = json.decode(response.body);
      
      if (data['ok'] == true) {
        return List<Map<String, dynamic>>.from(data['data']);
      } else {
        throw Exception(data['error']['message']);
      }
    } catch (e) {
      throw Exception('주차장 추천 실패: $e');
    }
  }

  // 즐겨찾기 관련 API
  static Future<List<Map<String, dynamic>>> getFavorites() async {
    try {
      final response = await http.get(
        Uri.parse('$_baseUrl/favorites'),
        headers: _headers,
      );

      final data = json.decode(response.body);
      
      if (data['ok'] == true) {
        return List<Map<String, dynamic>>.from(data['data']);
      } else {
        throw Exception(data['error']['message']);
      }
    } catch (e) {
      throw Exception('즐겨찾기 조회 실패: $e');
    }
  }

  static Future<void> addToFavorites(String parkingLotId) async {
    try {
      final response = await http.post(
        Uri.parse('$_baseUrl/favorites'),
        headers: _headers,
        body: json.encode({
          'parking_lot_id': parkingLotId,
        }),
      );

      final data = json.decode(response.body);
      
      if (data['ok'] != true) {
        throw Exception(data['error']['message']);
      }
    } catch (e) {
      throw Exception('즐겨찾기 추가 실패: $e');
    }
  }

  static Future<void> removeFromFavorites(String parkingLotId) async {
    try {
      final response = await http.delete(
        Uri.parse('$_baseUrl/favorites/$parkingLotId'),
        headers: _headers,
      );

      final data = json.decode(response.body);
      
      if (data['ok'] != true) {
        throw Exception(data['error']['message']);
      }
    } catch (e) {
      throw Exception('즐겨찾기 제거 실패: $e');
    }
  }

  // 검색 로그 API
  static Future<void> logSelection(String searchLogId, String selectedParkingLotId) async {
    try {
      final response = await http.post(
        Uri.parse('$_baseUrl/log_selection'),
        headers: _headers,
        body: json.encode({
          'search_log_id': searchLogId,
          'selected_parking_lot_id': selectedParkingLotId,
        }),
      );

      final data = json.decode(response.body);
      
      if (data['ok'] != true) {
        throw Exception(data['error']['message']);
      }
    } catch (e) {
      throw Exception('선택 로그 저장 실패: $e');
    }
  }
}
