import 'package:flutter/material.dart';
import 'package:geolocator/geolocator.dart';
import 'package:kakao_map_plugin/kakao_map_plugin.dart';
import 'package:permission_handler/permission_handler.dart';

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
    _initializeMap();
  }

  Future<void> _initializeMap() async {
    // 위치 권한 요청
    await _requestLocationPermission();
    // 현재 위치 가져오기
    await _getCurrentLocation();
  }

  Future<void> _requestLocationPermission() async {
    final status = await Permission.location.request();
    if (status != PermissionStatus.granted) {
      print('위치 권한이 거부되었습니다.');
    }
  }

  Future<void> _getCurrentLocation() async {
    try {
      // 위치 서비스가 활성화되어 있는지 확인
      bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
      if (!serviceEnabled) {
        print('위치 서비스가 비활성화되어 있습니다.');
        _setDefaultLocation();
        return;
      }

      // 위치 권한 확인
      LocationPermission permission = await Geolocator.checkPermission();
      if (permission == LocationPermission.denied) {
        permission = await Geolocator.requestPermission();
        if (permission == LocationPermission.denied) {
          print('위치 권한이 거부되었습니다.');
          _setDefaultLocation();
          return;
        }
      }

      if (permission == LocationPermission.deniedForever) {
        print('위치 권한이 영구적으로 거부되었습니다.');
        _setDefaultLocation();
        return;
      }

      final position = await Geolocator.getCurrentPosition(
        desiredAccuracy: LocationAccuracy.high,
        timeLimit: const Duration(seconds: 10),
      );
      
      setState(() {
        _currentPosition = position;
      });
      _updateMarkers();
    } catch (e) {
      print('위치 정보를 가져올 수 없습니다: $e');
      _setDefaultLocation();
    }
  }

  void _setDefaultLocation() {
    setState(() {
      _currentPosition = Position(
        latitude: widget.initialLat ?? 37.5665,
        longitude: widget.initialLng ?? 126.9780,
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

    return KakaoMap(
      onMapCreated: (KakaoMapController controller) {
        _mapController = controller;
        _updateMarkers();
        print('카카오맵이 성공적으로 생성되었습니다.');
        
        // 지도 중심을 현재 위치로 이동
        if (_currentPosition != null) {
          controller.setCenter(
            LatLng(_currentPosition!.latitude, _currentPosition!.longitude),
          );
          controller.setLevel((widget.initialZoom ?? 15).toInt());
        }
      },
      markers: _markers,
      center: _currentPosition != null 
          ? LatLng(_currentPosition!.latitude, _currentPosition!.longitude)
          : LatLng(widget.initialLat ?? 37.5665, widget.initialLng ?? 126.9780),
    );
  }

  // 지도 중심 이동
  void moveToLocation(double lat, double lng, {double? zoom}) {
    print('지도 이동: $lat, $lng');
    _mapController?.setCenter(LatLng(lat, lng));
    if (zoom != null) {
      _mapController?.setLevel(zoom.toInt());
    }
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