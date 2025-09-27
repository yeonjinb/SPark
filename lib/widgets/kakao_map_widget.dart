import 'package:flutter/material.dart';
import 'package:geolocator/geolocator.dart';
import 'package:kakao_map_plugin/kakao_map_plugin.dart';

class KakaoMapWidget extends StatefulWidget {
  final double? initialLat;
  final double? initialLng;
  final double? initialZoom;
  final List<Map<String, dynamic>>? parkingLots;
  final Function(double lat, double lng)? onMapTapped;
  final Function(double lat, double lng)? onCameraMoved;
  final bool showCurrentLocation;
  final bool showParkingLots;

  const KakaoMapWidget({
    Key? key,
    this.initialLat,
    this.initialLng,
    this.initialZoom = 15,
    this.parkingLots,
    this.onMapTapped,
    this.onCameraMoved,
    this.showCurrentLocation = true,
    this.showParkingLots = true,
  }) : super(key: key);

  @override
  State<KakaoMapWidget> createState() => _KakaoMapWidgetState();
}

class _KakaoMapWidgetState extends State<KakaoMapWidget> {
  Position? _currentPosition;
  KakaoMapController? _mapController;
  List<Marker> _markers = [];

  @override
  void initState() {
    super.initState();
    _getCurrentLocation();
  }

  Future<void> _getCurrentLocation() async {
    try {
      final position = await Geolocator.getCurrentPosition(
        desiredAccuracy: LocationAccuracy.high,
      );
      setState(() {
        _currentPosition = position;
      });
      _updateMarkers();
    } catch (e) {
      print('위치 정보를 가져올 수 없습니다: $e');
      // 기본 위치 설정 (서울시청)
      setState(() {
        _currentPosition = Position(
          latitude: 37.5665,
          longitude: 126.9780,
          timestamp: DateTime.now(),
          accuracy: 0,
          altitude: 0,
          heading: 0,
          speed: 0,
          speedAccuracy: 0,
          altitudeAccuracy: 0,
          headingAccuracy: 0,
        );
      });
      _updateMarkers();
    }
  }

  void _updateMarkers() {
    if (_currentPosition == null) return;

    List<Marker> markers = [];

    // 현재 위치 마커
    if (widget.showCurrentLocation) {
      markers.add(
        Marker(
          markerId: 'current_location',
          latLng: LatLng(_currentPosition!.latitude, _currentPosition!.longitude),
          width: 30,
          height: 30,
        ),
      );
    }

    // 주차장 마커들
    if (widget.showParkingLots && widget.parkingLots != null) {
      for (int i = 0; i < widget.parkingLots!.length; i++) {
        final lot = widget.parkingLots![i];
        markers.add(
          Marker(
            markerId: 'parking_$i',
            latLng: LatLng(
              lot['lat'] ?? 37.5665 + (i * 0.01),
              lot['lng'] ?? 126.9780 + (i * 0.01),
            ),
            width: 25,
            height: 25,
          ),
        );
      }
    }

    setState(() {
      _markers = markers;
    });
  }

  @override
  Widget build(BuildContext context) {
    if (_currentPosition == null) {
      return Container(
        width: double.infinity,
        height: double.infinity,
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [
              Colors.blue.withOpacity(0.1),
              Colors.blue.shade50,
            ],
          ),
        ),
        child: const Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              CircularProgressIndicator(),
              SizedBox(height: 16),
              Text(
                '지도를 불러오는 중...',
                style: TextStyle(
                  fontSize: 16,
                  color: Colors.grey,
                  fontFamily: 'Inter',
                ),
              ),
            ],
          ),
        ),
      );
    }

    try {
      return KakaoMap(
        onMapCreated: (KakaoMapController controller) {
          _mapController = controller;
          _updateMarkers();
          print('카카오맵이 성공적으로 생성되었습니다.');
        },
        markers: _markers,
      );
    } catch (e) {
      print('카카오맵 생성 오류: $e');
      return Container(
        width: double.infinity,
        height: double.infinity,
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [
              Colors.red.withOpacity(0.1),
              Colors.red.shade50,
            ],
          ),
        ),
        child: const Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(Icons.error, size: 48, color: Colors.red),
              SizedBox(height: 16),
              Text(
                '지도 로드 실패',
                style: TextStyle(
                  fontSize: 16,
                  color: Colors.red,
                  fontFamily: 'Inter',
                ),
              ),
            ],
          ),
        ),
      );
    }
  }

  // 지도 중심 이동
  void moveToLocation(double lat, double lng, {double? zoom}) {
    print('지도 이동: $lat, $lng');
    widget.onCameraMoved?.call(lat, lng);
  }

  // 현재 위치로 이동
  void moveToCurrentLocation() {
    if (_currentPosition != null) {
      moveToLocation(
        _currentPosition!.latitude,
        _currentPosition!.longitude,
        zoom: 15,
      );
    }
  }

  // 주차장 추가
  void addParkingLot(Map<String, dynamic> parkingLot) {
    setState(() {
      widget.parkingLots?.add(parkingLot);
      _updateMarkers();
    });
  }

  // 주차장 제거
  void removeParkingLot(int index) {
    setState(() {
      widget.parkingLots?.removeAt(index);
      _updateMarkers();
    });
  }
}