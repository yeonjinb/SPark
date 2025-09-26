import 'dart:convert';
import 'dart:io' show Platform;

import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:geolocator/geolocator.dart';
import 'package:kakaomap_webview/kakaomap_webview.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import '../services/favorites.dart';
import 'favorites_page.dart';
import 'lot_detail_page.dart';
import '../services/vosk_service.dart';

class MapPage extends StatefulWidget {
  const MapPage({super.key});

  @override
  State<MapPage> createState() => _MapPageState();
}

class _MapPageState extends State<MapPage> {
  Position? _position;
  bool _loading = false;
  String? _error;
  List<Map<String, dynamic>> _recommendations = [];
  late final FavoritesService _fav;
  Set<String> _favIds = {};
  final _vosk = VoskService();
  bool _listening = false;
  String _partial = '';
  
  // Voice command state
  int? _voiceMaxPrice;
  int? _voiceHours;
  bool _voiceIsEv = false;

  String get _kakaoJsKey => dotenv.env['KAKAO_JS_KEY'] ?? '';
  late final Dio _dio;

  @override
  void initState() {
    super.initState();
    _dio = Dio(BaseOptions(baseUrl: _resolveBaseUrl()));
    _fav = FavoritesService(Supabase.instance.client);
    _ensureLocation().then((_) async {
      await _fetchFavorites();
      await _fetchRecommend();
    });
  }

  Future<void> _fetchFavorites() async {
    try {
      _favIds = await _fav.fetchFavoriteLotIds();
      setState(() {});
    } catch (_) {}
  }

  String _resolveBaseUrl() {
    final override = dotenv.env['BACKEND_BASE_URL'];
    if (override != null && override.isNotEmpty) return override;
    if (Platform.isAndroid) return 'http://10.0.2.2:8000';
    return 'http://127.0.0.1:8000';
  }

  Future<void> _ensureLocation() async {
    try {
      LocationPermission perm = await Geolocator.checkPermission();
      if (perm == LocationPermission.denied) {
        perm = await Geolocator.requestPermission();
      }
      if (perm == LocationPermission.deniedForever || perm == LocationPermission.denied) {
        setState(() => _error = '위치 권한이 필요합니다.');
        return;
      }
      final pos = await Geolocator.getCurrentPosition(desiredAccuracy: LocationAccuracy.high);
      setState(() => _position = pos);
    } catch (e) {
      setState(() => _error = '위치 확인 실패: $e');
    }
  }

  Future<void> _fetchRecommend() async {
    if (_position == null) return;
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final authUserId = Supabase.instance.client.auth.currentUser?.id;
      final resp = await _dio.post('/recommend', data: {
        'user_lat': _position!.latitude,
        'user_lng': _position!.longitude,
        'is_ev': _voiceIsEv,
        'vehicle_height_m': null,
        'max_price_per_hour': _voiceMaxPrice,
        'limit': 10,
        'auth_user_id': authUserId,
      });
      if (resp.data is Map && resp.data['ok'] == true) {
        final List items = resp.data['data'] as List;
        setState(() {
          _recommendations = items.cast<Map<String, dynamic>>();
        });
      } else {
        setState(() => _error = '추천 실패');
      }
    } catch (e) {
      setState(() => _error = '네트워크 오류: $e');
    } finally {
      setState(() => _loading = false);
    }
  }

  String _buildMarkerScript() {
    if (_position == null) return '';
    final buffers = <String>[];
    for (final item in _recommendations) {
      final lot = item['lot'] as Map<String, dynamic>?;
      if (lot == null) continue;
      final lat = lot['lat'];
      final lng = lot['lng'];
      final name = (lot['name'] ?? '').toString().replaceAll("'", "\'");
      buffers.add("""
        (function(){
          var markerPosition  = new kakao.maps.LatLng(${lat}, ${lng});
          var marker = new kakao.maps.Marker({ position: markerPosition });
          marker.setMap(map);
          var iwContent = '<div style="padding:5px;">${name}</div>';
          var infowindow = new kakao.maps.InfoWindow({content : iwContent});
          kakao.maps.event.addListener(marker, 'click', function() {infowindow.open(map, marker);});
        })();
      """);
    }
    return buffers.join("\n");
  }

  void _parseVoiceCommand(String text) {
    // 시간 파싱: "3시간", "3시간 동안", "3시간 주차"
    final hourReg = RegExp(r'(\d+)\s*시간');
    final hourMatch = hourReg.firstMatch(text);
    if (hourMatch != null) {
      _voiceHours = int.tryParse(hourMatch.group(1) ?? '');
    }

    // 가격 파싱: "3천원", "3000원", "3만원", "저렴한"
    final priceReg = RegExp(r'(\d+)(천|만|원)');
    final priceMatch = priceReg.firstMatch(text);
    if (priceMatch != null) {
      final num = int.tryParse(priceMatch.group(1) ?? '') ?? 0;
      final unit = priceMatch.group(2) ?? '';
      if (unit == '천') {
        _voiceMaxPrice = num * 1000;
      } else if (unit == '만') {
        _voiceMaxPrice = num * 10000;
      } else if (unit == '원') {
        _voiceMaxPrice = num;
      }
    } else if (text.contains('저렴') || text.contains('싼')) {
      _voiceMaxPrice = 3000; // 기본 저렴 기준
    }

    // EV 파싱: "전기차", "EV", "충전"
    if (text.contains('전기차') || text.contains('EV') || text.contains('충전')) {
      _voiceIsEv = true;
    }

    // 거리 키워드: "가까운", "근처" → 가격 상한만 적용하고 거리는 선호 가중치로 처리
    if (text.contains('가까운') || text.contains('근처')) {
      // 거리 선호는 user_settings에서 처리되므로 별도 파라미터 없음
    }
  }

  Future<void> _toggleVoice() async {
    if (_listening) {
      await _vosk.stop();
      setState(() { _listening = false; _partial = ''; });
      return;
    }
    setState(() { _listening = true; _partial = ''; });
    await _vosk.start(
      onPartial: (p) => setState(() { _partial = p; }),
      onFinal: (text) async {
        _parseVoiceCommand(text);
        await _fetchRecommend();
        setState(() { _listening = false; _partial = ''; });
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    final pos = _position;
    return Scaffold(
      appBar: AppBar(
        title: const Text('SPark 지도'),
        actions: [
          if (_partial.isNotEmpty)
            Padding(
              padding: const EdgeInsets.only(right: 12),
              child: Center(child: Text(_partial, maxLines: 1, overflow: TextOverflow.ellipsis)),
            ),
          IconButton(
            icon: const Icon(Icons.favorite),
            onPressed: () async {
              await Navigator.of(context).push(
                MaterialPageRoute(builder: (_) => const FavoritesPage()),
              );
              await _fetchFavorites();
            },
          ),
        ],
      ),
      body: Column(
        children: [
          if (_error != null)
            Container(
              color: Colors.red.withOpacity(0.1),
              padding: const EdgeInsets.all(8),
              child: Row(
                children: [
                  const Icon(Icons.error, color: Colors.red),
                  const SizedBox(width: 8),
                  Expanded(child: Text(_error!)),
                ],
              ),
            ),
          if (_voiceMaxPrice != null || _voiceHours != null || _voiceIsEv)
            Container(
              color: Colors.blue.withOpacity(0.1),
              padding: const EdgeInsets.all(8),
              child: Row(
                children: [
                  const Icon(Icons.voice_over_off, color: Colors.blue),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Text(
                      '음성 필터: ${_voiceMaxPrice != null ? '${_voiceMaxPrice}원 이하' : ''}${_voiceHours != null ? ' ${_voiceHours}시간' : ''}${_voiceIsEv ? ' 전기차' : ''}',
                      style: const TextStyle(fontSize: 12),
                    ),
                  ),
                  IconButton(
                    icon: const Icon(Icons.clear, size: 16),
                    onPressed: () {
                      setState(() {
                        _voiceMaxPrice = null;
                        _voiceHours = null;
                        _voiceIsEv = false;
                      });
                      _fetchRecommend();
                    },
                  ),
                ],
              ),
            ),
          Expanded(
            child: (pos == null || _kakaoJsKey.isEmpty)
                ? const Center(child: Text('위치 또는 Kakao 키를 준비 중...'))
                : KakaoMapView(
                    width: MediaQuery.of(context).size.width,
                    height: MediaQuery.of(context).size.height,
                    kakaoMapKey: _kakaoJsKey,
                    lat: pos.latitude,
                    lng: pos.longitude,
                    showMapTypeControl: true,
                    showZoomControl: true,
                    customScript: _buildMarkerScript(),
                  ),
          ),
          SizedBox(
            height: 180,
            child: _loading
                ? const Center(child: CircularProgressIndicator())
                : ListView.builder(
                    scrollDirection: Axis.horizontal,
                    itemCount: _recommendations.length,
                    itemBuilder: (context, index) {
                      final item = _recommendations[index];
                      final lot = item['lot'] as Map<String, dynamic>? ?? {};
                      final score = (item['score'] ?? 0.0) as num;
                      final lotId = (lot['id'] ?? '').toString();
                      final isFav = _favIds.contains(lotId);
                      return InkWell(
                        onTap: () {
                          Navigator.of(context).push(
                            MaterialPageRoute(builder: (_) => LotDetailPage(lot: lot)),
                          );
                        },
                        child: Card(
                          margin: const EdgeInsets.all(8),
                          child: Container(
                            width: 280,
                            padding: const EdgeInsets.all(12),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Row(
                                  children: [
                                    Expanded(
                                      child: Text(
                                        lot['name']?.toString() ?? '주차장',
                                        style: const TextStyle(fontWeight: FontWeight.bold),
                                        overflow: TextOverflow.ellipsis,
                                      ),
                                    ),
                                    IconButton(
                                      icon: Icon(isFav ? Icons.favorite : Icons.favorite_border, color: isFav ? Colors.red : null),
                                      onPressed: () async {
                                        try {
                                          await _fav.toggleFavorite(lotId);
                                          await _fetchFavorites();
                                        } catch (e) {
                                          setState(() { _error = '즐겨찾기 오류: $e'; });
                                        }
                                      },
                                    )
                                  ],
                                ),
                                const SizedBox(height: 6),
                                Text('요금: ${lot['price_per_hour']}원/시간'),
                                Text('EV: ${lot['ev_charging'] == true ? '가능' : '불가'}'),
                                Text('24시간: ${lot['open_24h'] == true ? '예' : '아니오'}'),
                                const Spacer(),
                                Text('점수: ${score.toStringAsFixed(2)}'),
                              ],
                            ),
                          ),
                        ),
                      );
                    },
                  ),
          ),
        ],
      ),
      floatingActionButton: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          FloatingActionButton.extended(
            onPressed: _toggleVoice,
            icon: Icon(_listening ? Icons.mic_off : Icons.mic),
            label: Text(_listening ? '음성 중지' : '음성 검색'),
          ),
          const SizedBox(height: 8),
          FloatingActionButton.extended(
            onPressed: () async {
              await _ensureLocation();
              await _fetchRecommend();
              await _fetchFavorites();
              setState(() {});
            },
            icon: const Icon(Icons.refresh),
            label: const Text('추천 새로고침'),
          ),
        ],
      ),
    );
  }
}
