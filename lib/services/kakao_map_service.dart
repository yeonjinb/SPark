import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter_dotenv/flutter_dotenv.dart';

class KakaoMapService {
  static const String _baseUrl = 'https://dapi.kakao.com/v2';
  static String? _apiKey;

  static Future<void> initialize() async {
    try {
      _apiKey = dotenv.env['KAKAO_REST_API_KEY'];
    } catch (e) {
      print('환경 변수 로드 실패, 기본값 사용: $e');
    }
    
    if (_apiKey == null) {
      // 기본 API 키 사용 (개발용)
      _apiKey = 'fc9248fb37c47471e8ac96d2336946f2';
      print('기본 카카오 API 키를 사용합니다.');
    }
  }

  static Map<String, String> get _headers => {
    'Authorization': 'KakaoAK $_apiKey',
    'Content-Type': 'application/json',
  };

  /// 주소를 좌표로 변환 (Geocoding)
  static Future<Map<String, double>?> getCoordinatesFromAddress(String address) async {
    try {
      final encodedAddress = Uri.encodeComponent(address);
      final url = '$_baseUrl/local/geo/coord2address.json?x=127.027619&y=37.497951&input_coord=WGS84';
      
      final response = await http.get(
        Uri.parse('$_baseUrl/local/search/address.json?query=$encodedAddress'),
        headers: _headers,
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final documents = data['documents'] as List;
        
        if (documents.isNotEmpty) {
          final doc = documents.first;
          return {
            'lng': double.parse(doc['x']),
            'lat': double.parse(doc['y']),
          };
        }
      }
      return null;
    } catch (e) {
      print('Error getting coordinates: $e');
      return null;
    }
  }

  /// 좌표를 주소로 변환 (Reverse Geocoding)
  static Future<String?> getAddressFromCoordinates(double lng, double lat) async {
    try {
      final url = '$_baseUrl/local/geo/coord2address.json?x=$lng&y=$lat&input_coord=WGS84';
      
      final response = await http.get(
        Uri.parse(url),
        headers: _headers,
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final documents = data['documents'] as List;
        
        if (documents.isNotEmpty) {
          final doc = documents.first;
          return doc['address']['address_name'];
        }
      }
      return null;
    } catch (e) {
      print('Error getting address: $e');
      return null;
    }
  }

  /// 키워드로 장소 검색
  static Future<List<Map<String, dynamic>>> searchPlaces(String keyword, {int page = 1, int size = 15}) async {
    try {
      final encodedKeyword = Uri.encodeComponent(keyword);
      final url = '$_baseUrl/local/search/keyword.json?query=$encodedKeyword&page=$page&size=$size';
      
      final response = await http.get(
        Uri.parse(url),
        headers: _headers,
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final documents = data['documents'] as List;
        
        return documents.map((doc) => {
          'id': doc['id'],
          'name': doc['place_name'],
          'address': doc['address_name'],
          'road_address': doc['road_address_name'],
          'lng': double.parse(doc['x']),
          'lat': double.parse(doc['y']),
          'category': doc['category_name'],
          'phone': doc['phone'],
          'url': doc['place_url'],
        }).toList();
      }
      return [];
    } catch (e) {
      print('Error searching places: $e');
      return [];
    }
  }

  /// 카테고리로 장소 검색 (주차장 검색용)
  static Future<List<Map<String, dynamic>>> searchParkingLots(double lng, double lat, {int radius = 2000}) async {
    try {
      final url = '$_baseUrl/local/search/category.json?category_group_code=PK6&x=$lng&y=$lat&radius=$radius';
      
      final response = await http.get(
        Uri.parse(url),
        headers: _headers,
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final documents = data['documents'] as List;
        
        return documents.map((doc) => {
          'id': doc['id'],
          'name': doc['place_name'],
          'address': doc['address_name'],
          'road_address': doc['road_address_name'],
          'lng': double.parse(doc['x']),
          'lat': double.parse(doc['y']),
          'phone': doc['phone'],
          'url': doc['place_url'],
          'distance': doc['distance'],
        }).toList();
      }
      return [];
    } catch (e) {
      print('Error searching parking lots: $e');
      return [];
    }
  }
}

class KakaoNavigationService {
  static const String _baseUrl = 'https://dapi.kakao.com/v2';
  static String? _apiKey;

  static Future<void> initialize() async {
    try {
      _apiKey = dotenv.env['KAKAO_REST_API_KEY'];
    } catch (e) {
      print('환경 변수 로드 실패, 기본값 사용: $e');
    }
    
    if (_apiKey == null) {
      // 기본 API 키 사용 (개발용)
      _apiKey = 'fc9248fb37c47471e8ac96d2336946f2';
      print('기본 카카오 API 키를 사용합니다.');
    }
  }

  static Map<String, String> get _headers => {
    'Authorization': 'KakaoAK $_apiKey',
    'Content-Type': 'application/json',
  };

  /// 카카오맵 길찾기 URL 생성
  static String getNavigationUrl({
    required double startLng,
    required double startLat,
    required double endLng,
    required double endLat,
    String? startName,
    String? endName,
  }) {
    final startNameParam = startName != null ? '&sname=${Uri.encodeComponent(startName)}' : '';
    final endNameParam = endName != null ? '&ename=${Uri.encodeComponent(endName)}' : '';
    
    return 'https://map.kakao.com/link/route/$startLng,$startLat/$endLng,$endLat$startNameParam$endNameParam';
  }

  /// 카카오맵 앱으로 길찾기 실행
  static String getKakaoMapAppUrl({
    required double startLng,
    required double startLat,
    required double endLng,
    required double endLat,
    String? startName,
    String? endName,
  }) {
    final startNameParam = startName != null ? '&sname=${Uri.encodeComponent(startName)}' : '';
    final endNameParam = endName != null ? '&ename=${Uri.encodeComponent(endName)}' : '';
    
    return 'kakaomap://route?sp=$startLng,$startLat&ep=$endLng,$endLat&by=CAR$startNameParam$endNameParam';
  }

  /// 네이버맵 앱으로 길찾기 실행
  static String getNaverMapAppUrl({
    required double startLng,
    required double startLat,
    required double endLng,
    required double endLat,
    String? startName,
    String? endName,
  }) {
    final startNameParam = startName != null ? '&sname=${Uri.encodeComponent(startName)}' : '';
    final endNameParam = endName != null ? '&ename=${Uri.encodeComponent(endName)}' : '';
    
    return 'nmap://route/car?slat=$startLat&slng=$startLng&sname=$startNameParam&dlat=$endLat&dlng=$endLng&dname=$endNameParam';
  }

  /// 구글맵 앱으로 길찾기 실행
  static String getGoogleMapAppUrl({
    required double startLng,
    required double startLat,
    required double endLng,
    required double endLat,
    String? startName,
    String? endName,
  }) {
    final startNameParam = startName != null ? '&saddr=${Uri.encodeComponent(startName)}' : '';
    final endNameParam = endName != null ? '&daddr=${Uri.encodeComponent(endName)}' : '';
    
    return 'https://www.google.com/maps/dir/?api=1&origin=$startLat,$startLng&destination=$endLat,$endLng&travelmode=driving$startNameParam$endNameParam';
  }
}
