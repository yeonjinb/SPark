import 'package:flutter_riverpod/flutter_riverpod.dart';

// 앱 상태 열거형
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

// 오류 타입 열거형
enum ErrorType {
  network,
  voice,
  noResults,
  location,
}

// 주차장 타입 열거형
enum ParkingType {
  optimal,
  nearest,
  cheapest,
}

// 차량 타입 열거형
enum CarType {
  compact,
  small,
  medium,
  large,
}

// 선호도 타입 열거형
enum PreferenceType {
  cost,
  time,
  difficulty,
}

// 주차장 데이터 모델
class ParkingLot {
  final int id;
  final String name;
  final String address;
  final String distance;
  final String price;
  final double rating;
  final List<String> features;
  final int available;
  final ParkingType type;

  const ParkingLot({
    required this.id,
    required this.name,
    required this.address,
    required this.distance,
    required this.price,
    required this.rating,
    required this.features,
    required this.available,
    required this.type,
  });
}

// 사용자 프로필 모델
class UserProfile {
  final String name;
  final String email;
  final String drivingExperience;
  final CarType carType;
  final PreferenceType preference;
  final List<String> discountTypes;

  const UserProfile({
    required this.name,
    required this.email,
    required this.drivingExperience,
    required this.carType,
    required this.preference,
    required this.discountTypes,
  });
}

// 앱 상태 관리 Provider
class AppStateNotifier extends StateNotifier<AppState> {
  AppStateNotifier() : super(AppState.splash);

  void goToSplash() => state = AppState.splash;
  void goToLocation() => state = AppState.location;
  void goToMain() => state = AppState.main;
  void goToVoiceLoading() => state = AppState.voiceLoading;
  void goToRecommendations() => state = AppState.recommendations;
  void goToDetails() => state = AppState.details;
  void goToMyProfile() => state = AppState.myProfile;
  void goToMyPage() => state = AppState.myPage;
  void goToError() => state = AppState.error;
}

// Provider 정의
final appStateProvider = StateNotifierProvider<AppStateNotifier, AppState>((ref) {
  return AppStateNotifier();
});

// 로그인 상태 Provider
final isLoggedInProvider = StateProvider<bool>((ref) => false);

// 위치 권한 상태 Provider
final locationPermissionGrantedProvider = StateProvider<bool>((ref) => false);

// 선택된 주차장 ID Provider
final selectedParkingIdProvider = StateProvider<int?>((ref) => null);

// 검색 쿼리 Provider
final searchQueryProvider = StateProvider<String>((ref) => '');

// 오류 타입 Provider
final errorTypeProvider = StateProvider<ErrorType?>((ref) => null);

// 사용자 프로필 Provider
final userProfileProvider = StateProvider<UserProfile?>((ref) => null);

// 즐겨찾기 주차장 목록 Provider
final favoriteParkingsProvider = StateProvider<List<ParkingLot>>((ref) => []);

// 추천 주차장 목록 Provider
final recommendedParkingsProvider = StateProvider<List<ParkingLot>>((ref) => []);

// Mock 데이터
final mockParkingLotsProvider = Provider<List<ParkingLot>>((ref) {
  return [
    const ParkingLot(
      id: 1,
      name: "강남역 지하주차장",
      address: "서울특별시 강남구 강남대로 396",
      distance: "200m",
      price: "2,000원/시간",
      rating: 4.5,
      features: ["전기차 충전", "24시간 운영", "무인 결제"],
      available: 15,
      type: ParkingType.optimal,
    ),
    const ParkingLot(
      id: 2,
      name: "역삼동 공영주차장",
      address: "서울특별시 강남구 역삼동 123-45",
      distance: "150m",
      price: "1,500원/시간",
      rating: 4.2,
      features: ["무인 결제", "24시간 운영"],
      available: 8,
      type: ParkingType.nearest,
    ),
    const ParkingLot(
      id: 3,
      name: "테헤란로 주차타워",
      address: "서울특별시 강남구 테헤란로 123",
      distance: "300m",
      price: "1,000원/시간",
      rating: 4.0,
      features: ["무인 결제"],
      available: 25,
      type: ParkingType.cheapest,
    ),
  ];
});
