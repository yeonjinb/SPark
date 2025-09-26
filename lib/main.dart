import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'screens/voice_search_loading_screen.dart';
import 'screens/recommendation_results_screen.dart';
import 'screens/login_signup_screen.dart';
import 'services/api_service.dart';
import 'services/kakao_map_service.dart';
import 'services/kakao_auth_service.dart';
import 'services/vosk_service.dart';
import 'widgets/kakao_map_widget.dart';
import 'widgets/voice_recognition_widget.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:kakao_map_plugin/kakao_map_plugin.dart';
import 'package:kakao_flutter_sdk/kakao_flutter_sdk.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // 환경 변수 로드 (선택적)
  try {
    await dotenv.load(fileName: ".env");
    print('환경 변수 로드 성공');
  } catch (e) {
    print('환경 변수 파일이 없습니다. 기본 설정으로 진행합니다.');
    // 환경 변수 없이 진행
  }
  
  // 서비스 초기화
  await ApiService.initialize();
  await KakaoMapService.initialize();
  await KakaoNavigationService.initialize();
  await KakaoAuthService.initialize();
  await VoskService.initialize();
  
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'SPark',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        fontFamily: 'Inter',
      ),
      home: const LocationPermissionScreen(),
    );
  }
}

class LocationPermissionScreen extends StatelessWidget {
  const LocationPermissionScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.blue.shade50,
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            children: [
              const SizedBox(height: 60),
              Container(
                width: 160,
                height: 160,
                decoration: BoxDecoration(
                  color: Colors.blue.withOpacity(0.1),
                  shape: BoxShape.circle,
                ),
                child: Padding(
                  padding: const EdgeInsets.all(25),
                  child: Image.asset(
                    'assets/images/icon252.png',
                    fit: BoxFit.contain,
                  ),
                ),
              ),
              const SizedBox(height: 40),
              const Text(
                '위치 권한이 필요합니다',
                style: TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                  fontFamily: 'Inter',
                ),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 16),
              const Text(
                '주변 주차장을 찾고 추천하기 위해\n위치 정보가 필요합니다',
                style: TextStyle(
                  fontSize: 16,
                  color: Colors.grey,
                  fontFamily: 'Inter',
                ),
                textAlign: TextAlign.center,
              ),
              const Spacer(),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: () {
                    Navigator.of(context).pushReplacement(
                      MaterialPageRoute(builder: (context) => const MainScreen()),
                    );
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.blue,
                    padding: const EdgeInsets.symmetric(vertical: 16),
                  ),
                  child: const Text(
                    '위치 권한 허용',
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.w600,
                      color: Colors.white,
                      fontFamily: 'Inter',
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 12),
              SizedBox(
                width: double.infinity,
                child: OutlinedButton(
                  onPressed: () {
                    Navigator.of(context).pushReplacement(
                      MaterialPageRoute(builder: (context) => const MainScreen()),
                    );
                  },
                  child: const Text(
                    '나중에 설정',
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.w600,
                      color: Colors.blue,
                      fontFamily: 'Inter',
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 20),
            ],
          ),
        ),
      ),
    );
  }
}

class MainScreen extends StatelessWidget {
  const MainScreen({super.key});

  List<Map<String, dynamic>> _getSampleParkingLots() {
    return [
      {
        'name': '건대입구역 지하주차장',
        'address': '서울시 광진구 능동로 209',
        'lat': 37.5407,
        'lng': 127.0692,
        'price_per_hour': 1600,
        'available': 12,
      },
      {
        'name': '건대 로데오거리 노상주차장',
        'address': '서울시 광진구 아차산로29길 18',
        'lat': 37.5405,
        'lng': 127.0685,
        'price_per_hour': 1200,
        'available': 5,
      },
      {
        'name': '건국대학교 주변 공영주차장',
        'address': '서울시 광진구 능동로 120',
        'lat': 37.5410,
        'lng': 127.0695,
        'price_per_hour': 1000,
        'available': 18,
      },
    ];
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.blue.shade50,
      body: Stack(
        children: [
          // 지도 영역
          Container(
            width: double.infinity,
            height: double.infinity,
            child: KakaoMapWidget(
              showCurrentLocation: true,
              showParkingLots: true,
              parkingLots: _getSampleParkingLots(),
              onMapTapped: (lat, lng) {
                print('지도 탭: $lat, $lng');
              },
              onCameraMoved: (lat, lng) {
                print('카메라 이동: $lat, $lng');
              },
            ),
          ),
          // 상단 앱바
          Positioned(
            top: 0,
            left: 0,
            right: 0,
            child: Container(
              padding: EdgeInsets.only(
                top: MediaQuery.of(context).padding.top + 16,
                left: 20,
                right: 20,
                bottom: 16,
              ),
              decoration: const BoxDecoration(
                color: Colors.white,
                boxShadow: [
                  BoxShadow(
                    color: Colors.black12,
                    blurRadius: 10,
                    offset: Offset(0, 2),
                  ),
                ],
              ),
              child: Row(
                children: [
                  Container(
                    width: 48,
                    height: 48,
                    decoration: BoxDecoration(
                      color: Colors.blue.shade600,
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Padding(
                      padding: const EdgeInsets.all(10),
                      child: Image.asset(
                        'assets/images/icon64.png',
                        fit: BoxFit.none,
                      ),
                    ),
                  ),
                  const SizedBox(width: 12),
                  const Expanded(
                    child: Text(
                      'SPark - 스마트 주차장 검색',
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.w600,
                        fontFamily: 'Inter',
                      ),
                    ),
                  ),
                  const Icon(
                    Icons.notifications_outlined,
                    color: Colors.grey,
                  ),
                ],
              ),
            ),
          ),
          // 플로팅 패널 (이미지 참고)
          Positioned(
            bottom: 100,
            left: 16,
            right: 16,
            child: Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(20),
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withOpacity(0.1),
                    blurRadius: 20,
                    offset: const Offset(0, 4),
                  ),
                ],
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // 헤더: "주변 주차장" + "3개 발견" 배지
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Text(
                        '주변 주차장',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.w600,
                          fontFamily: 'Inter',
                        ),
                      ),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                        decoration: BoxDecoration(
                          color: Colors.blue.shade600,
                          borderRadius: BorderRadius.circular(16),
                        ),
                        child: const Text(
                          '3개 발견',
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 12,
                            fontWeight: FontWeight.w600,
                            fontFamily: 'Inter',
                          ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  // 주차장 리스트
                  _buildParkingItem(
                    '건대입구역 지하주차장',
                    '200m · 시간당 2,000원 · 여유 15대',
                    '보통',
                    Colors.blue.shade100,
                    Colors.blue.shade600,
                  ),
                  const SizedBox(height: 12),
                  _buildParkingItem(
                    '스타시티 주차장',
                    '350m · 시간당 1,500원 · 여유 8대',
                    '부족',
                    Colors.red.shade100,
                    Colors.red.shade600,
                  ),
                  const SizedBox(height: 20),
                  // "최적의 주차장 찾기" 버튼
                  SizedBox(
                    width: double.infinity,
                    child: ElevatedButton.icon(
                      onPressed: () {
                        // 음성 검색 화면으로 이동
                        Navigator.of(context).push(
                          MaterialPageRoute(
                            builder: (context) => VoiceRecognitionScreen(
                              onResult: (recognizedText) {
                                // 음성 인식 완료 후 결과 화면으로 이동
                                Navigator.of(context).pushReplacement(
                                  MaterialPageRoute(
                                    builder: (context) => RecommendationResultsScreen(
                                      searchQuery: recognizedText,
                                      onBack: () {
                                        Navigator.of(context).pop();
                                      },
                                      onSelectParking: (id) {
                                        Navigator.of(context).push(
                                          MaterialPageRoute(
                                            builder: (context) => _ParkingDetailsScreen(parkingId: id),
                                          ),
                                        );
                                      },
                                    ),
                                  ),
                                );
                              },
                              onError: (error) {
                                ScaffoldMessenger.of(context).showSnackBar(
                                  SnackBar(
                                    content: Text('음성 인식 오류: $error'),
                                    backgroundColor: Colors.red,
                                  ),
                                );
                              },
                            ),
                          ),
                        );
                      },
                      icon: const Icon(Icons.mic, size: 20),
                      label: const Text(
                        '최적의 주차장 찾기',
                        style: TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.w600,
                          fontFamily: 'Inter',
                        ),
                      ),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.blue.shade600,
                        foregroundColor: Colors.white,
                        padding: const EdgeInsets.symmetric(vertical: 16),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(12),
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: 0,
        type: BottomNavigationBarType.fixed,
        backgroundColor: Colors.white,
        selectedItemColor: Colors.blue.shade600,
        unselectedItemColor: Colors.grey.shade400,
        onTap: (index) {
          if (index == 1) {
            // 내 페이지로 이동
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('내 페이지는 준비 중입니다')),
            );
          } else if (index == 2) {
            // 로그인/회원가입 화면으로 이동
            Navigator.of(context).push(
              MaterialPageRoute(
                builder: (context) => LoginSignupScreen(
                  onLoginSuccess: () {
                    Navigator.of(context).pop();
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(
                        content: Text('로그인되었습니다!'),
                        backgroundColor: Colors.green,
                      ),
                    );
                  },
                  onBack: () {
                    Navigator.of(context).pop();
                  },
                ),
              ),
            );
          }
        },
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.home),
            label: '홈',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.favorite),
            label: '내페이지',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.person),
            label: '로그인',
          ),
        ],
      ),
    );
  }

  Widget _buildParkingItem(String name, String details, String status, Color statusBgColor, Color statusTextColor) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.grey.shade50,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.grey.shade200),
      ),
      child: Row(
        children: [
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  name,
                  style: const TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w600,
                    fontFamily: 'Inter',
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  details,
                  style: TextStyle(
                    fontSize: 14,
                    color: Colors.grey.shade600,
                    fontFamily: 'Inter',
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(width: 12),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
            decoration: BoxDecoration(
              color: statusBgColor,
              borderRadius: BorderRadius.circular(12),
            ),
            child: Text(
              status,
              style: TextStyle(
                color: statusTextColor,
                fontSize: 12,
                fontWeight: FontWeight.w600,
                fontFamily: 'Inter',
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class VoiceRecognitionScreen extends StatelessWidget {
  final Function(String) onResult;
  final Function(String)? onError;

  const VoiceRecognitionScreen({
    super.key,
    required this.onResult,
    this.onError,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.blue.shade50,
      appBar: AppBar(
        title: const Text(
          '음성 검색',
          style: TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.w600,
            fontFamily: 'Inter',
          ),
        ),
        backgroundColor: Colors.blue.shade600,
        foregroundColor: Colors.white,
        elevation: 0,
      ),
      body: SafeArea(
        child: Column(
          children: [
            const SizedBox(height: 40),
            // 안내 텍스트
            const Padding(
              padding: EdgeInsets.symmetric(horizontal: 24),
              child: Text(
                '원하는 주차장을 말씀해주세요',
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.w600,
                  fontFamily: 'Inter',
                ),
                textAlign: TextAlign.center,
              ),
            ),
            const SizedBox(height: 8),
            const Padding(
              padding: EdgeInsets.symmetric(horizontal: 24),
              child: Text(
                '예: "2시간 이용 가능한 주차장 찾아줘"',
                style: TextStyle(
                  fontSize: 14,
                  color: Colors.grey,
                  fontFamily: 'Inter',
                ),
                textAlign: TextAlign.center,
              ),
            ),
            const SizedBox(height: 40),
            // 음성 인식 위젯
            Expanded(
              child: VoiceRecognitionWidget(
                onResult: (text) {
                  if (text.isNotEmpty) {
                    onResult(text);
                  }
                },
                onError: onError,
              ),
            ),
            const SizedBox(height: 20),
          ],
        ),
      ),
    );
  }
}

class _ParkingDetailsScreen extends StatelessWidget {
  final int parkingId;

  const _ParkingDetailsScreen({required this.parkingId});

  @override
  Widget build(BuildContext context) {
    // 주차장 데이터 (실제로는 API에서 가져올 데이터)
    final parkingData = _getParkingData(parkingId);
    
    return Scaffold(
      appBar: AppBar(
        title: Text(parkingData['name']),
        backgroundColor: Colors.blue.shade600,
        foregroundColor: Colors.white,
        elevation: 0,
      ),
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // 지도 영역
            Container(
              height: 250,
              width: double.infinity,
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                  colors: [
                    Colors.blue.shade100,
                    Colors.grey.shade100,
                  ],
                ),
              ),
              child: Stack(
                children: [
                  const Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(
                          Icons.map,
                          size: 60,
                          color: Colors.blue,
                        ),
                        SizedBox(height: 8),
                        Text(
                          '카카오맵 연동 예정',
                          style: TextStyle(
                            fontSize: 16,
                            color: Colors.blue,
                            fontFamily: 'Inter',
                          ),
                        ),
                      ],
                    ),
                  ),
                  Positioned(
                    top: 16,
                    right: 16,
                    child: Container(
                      padding: const EdgeInsets.all(8),
                      decoration: BoxDecoration(
                        color: Colors.white,
                        borderRadius: BorderRadius.circular(8),
                        boxShadow: [
                          BoxShadow(
                            color: Colors.black.withOpacity(0.1),
                            blurRadius: 4,
                            offset: const Offset(0, 2),
                          ),
                        ],
                      ),
                      child: Icon(
                        Icons.navigation,
                        color: Colors.blue.shade600,
                        size: 20,
                      ),
                    ),
                  ),
                ],
              ),
            ),
            // 주차장 정보
            Padding(
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // 주차장 이름과 배지
                  Row(
                    children: [
                      Expanded(
                        child: Text(
                          parkingData['name'],
                          style: const TextStyle(
                            fontSize: 24,
                            fontWeight: FontWeight.bold,
                            fontFamily: 'Inter',
                          ),
                        ),
                      ),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                        decoration: BoxDecoration(
                          color: parkingData['badgeColor'],
                          borderRadius: BorderRadius.circular(20),
                        ),
                        child: Text(
                          parkingData['badge'],
                          style: const TextStyle(
                            color: Colors.white,
                            fontSize: 12,
                            fontWeight: FontWeight.w600,
                            fontFamily: 'Inter',
                          ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  // 주소
                  Row(
                    children: [
                      Icon(
                        Icons.location_on,
                        size: 16,
                        color: Colors.grey.shade600,
                      ),
                      const SizedBox(width: 4),
                      Expanded(
                        child: Text(
                          parkingData['address'],
                          style: TextStyle(
                            fontSize: 14,
                            color: Colors.grey.shade600,
                            fontFamily: 'Inter',
                          ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 20),
                  // 기본 정보
                  _buildInfoSection('기본 정보', [
                    _buildInfoRow('거리', parkingData['distance'], Icons.directions_walk),
                    _buildInfoRow('요금', parkingData['price'], Icons.attach_money),
                    _buildInfoRow('평점', '${parkingData['rating']} ⭐', Icons.star),
                    _buildInfoRow('주차 가능', '${parkingData['available']}대', Icons.local_parking),
                  ]),
                  const SizedBox(height: 20),
                  // 특징
                  _buildInfoSection('주차장 특징', [
                    ...parkingData['features'].map((feature) => 
                      Padding(
                        padding: const EdgeInsets.symmetric(vertical: 4),
                        child: Row(
                          children: [
                            Icon(
                              Icons.check_circle,
                              size: 16,
                              color: Colors.green.shade600,
                            ),
                            const SizedBox(width: 8),
                            Text(
                              feature,
                              style: const TextStyle(
                                fontSize: 14,
                                fontFamily: 'Inter',
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ]),
                  const SizedBox(height: 30),
                  // 액션 버튼들
                  Row(
                    children: [
                      Expanded(
                        child: ElevatedButton.icon(
                          onPressed: () async {
                            // 카카오맵 길찾기 실행
                            final url = KakaoNavigationService.getNavigationUrl(
                              startLng: 127.027619, // 현재 위치 (실제로는 사용자 위치)
                              startLat: 37.497951,
                              endLng: parkingData['lng'] ?? 127.027619,
                              endLat: parkingData['lat'] ?? 37.497951,
                              startName: '현재 위치',
                              endName: parkingData['name'],
                            );
                            
                            if (await canLaunchUrl(Uri.parse(url))) {
                              await launchUrl(Uri.parse(url));
                            } else {
                              ScaffoldMessenger.of(context).showSnackBar(
                                const SnackBar(
                                  content: Text('카카오맵을 실행할 수 없습니다'),
                                  backgroundColor: Colors.red,
                                ),
                              );
                            }
                          },
                          icon: const Icon(Icons.navigation),
                          label: const Text('길찾기'),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.blue.shade600,
                            foregroundColor: Colors.white,
                            padding: const EdgeInsets.symmetric(vertical: 16),
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(12),
                            ),
                          ),
                        ),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: OutlinedButton.icon(
                          onPressed: () {
                            ScaffoldMessenger.of(context).showSnackBar(
                              const SnackBar(
                                content: Text('즐겨찾기에 추가되었습니다'),
                                backgroundColor: Colors.orange,
                              ),
                            );
                          },
                          icon: const Icon(Icons.favorite_border),
                          label: const Text('즐겨찾기'),
                          style: OutlinedButton.styleFrom(
                            side: BorderSide(color: Colors.blue.shade600),
                            foregroundColor: Colors.blue.shade600,
                            padding: const EdgeInsets.symmetric(vertical: 16),
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(12),
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildInfoSection(String title, List<Widget> children) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          title,
          style: const TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.w600,
            fontFamily: 'Inter',
          ),
        ),
        const SizedBox(height: 12),
        ...children,
      ],
    );
  }

  Widget _buildInfoRow(String label, String value, IconData icon) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 6),
      child: Row(
        children: [
          Icon(
            icon,
            size: 16,
            color: Colors.grey.shade600,
          ),
          const SizedBox(width: 8),
          Text(
            '$label: ',
            style: TextStyle(
              fontSize: 14,
              color: Colors.grey.shade600,
              fontFamily: 'Inter',
            ),
          ),
          Text(
            value,
            style: const TextStyle(
              fontSize: 14,
              fontWeight: FontWeight.w500,
              fontFamily: 'Inter',
            ),
          ),
        ],
      ),
    );
  }

  Map<String, dynamic> _getParkingData(int id) {
    final parkingList = [
      {
        'name': '건대입구역 지하주차장',
        'address': '서울시 광진구 능동로 209',
        'distance': '네비 기준 2분 (150m)',
        'price': '2시간 3,200원',
        'badge': '최적',
        'badgeColor': Colors.blue,
        'rating': 4.3,
        'features': ['24시간 운영', '실내주차', '카드결제 가능', '엘리베이터 이용'],
        'available': 12,
        'lat': 37.5407,
        'lng': 127.0692,
      },
      {
        'name': '건대 로데오거리 노상주차장',
        'address': '서울시 광진구 아차산로29길 18',
        'distance': '네비 기준 1분 (80m)',
        'price': '2시간 2,400원',
        'badge': '최단거리',
        'badgeColor': Colors.green,
        'rating': 4.0,
        'features': ['노상주차', '단기주차', '맛집근처', '24시간 운영'],
        'available': 5,
        'lat': 37.5405,
        'lng': 127.0685,
      },
      {
        'name': '건국대학교 주변 공영주차장',
        'address': '서울시 광진구 능동로 120',
        'distance': '네비 기준 4분 (300m)',
        'price': '2시간 2,000원',
        'badge': '최저가격',
        'badgeColor': Colors.orange,
        'rating': 4.1,
        'features': ['공영주차', '저렴한 요금', '넓은 공간', '안전한 주차'],
        'available': 18,
        'lat': 37.5410,
        'lng': 127.0695,
      },
    ];
    
    return parkingList[id - 1] ?? parkingList[0];
  }
}