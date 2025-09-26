import 'package:flutter/material.dart';

class RecommendationResultsScreen extends StatefulWidget {
  final String searchQuery;
  final VoidCallback? onBack;
  final Function(int)? onSelectParking;

  const RecommendationResultsScreen({
    super.key,
    required this.searchQuery,
    this.onBack,
    this.onSelectParking,
  });

  @override
  State<RecommendationResultsScreen> createState() => _RecommendationResultsScreenState();
}

class _RecommendationResultsScreenState extends State<RecommendationResultsScreen> {
  int _selectedIndex = 0;

  final List<ParkingRecommendation> _recommendations = [
    ParkingRecommendation(
      id: 1,
      name: '건대입구역 지하주차장',
      address: '서울시 광진구 능동로 209',
      distance: '네비 기준 2분 (150m)',
      price: '2시간 3,200원',
      type: 'optimal',
      badge: '최적',
      badgeColor: Colors.blue,
      rating: 4.3,
      features: ['24시간', '실내주차', '카드결제'],
      available: 12,
    ),
    ParkingRecommendation(
      id: 2,
      name: '건대 로데오거리 노상주차장',
      address: '서울시 광진구 아차산로29길 18',
      distance: '네비 기준 1분 (80m)',
      price: '2시간 2,400원',
      type: 'nearest',
      badge: '최단거리',
      badgeColor: Colors.green,
      rating: 4.0,
      features: ['노상주차', '단기주차', '맛집근처'],
      available: 5,
    ),
    ParkingRecommendation(
      id: 3,
      name: '건국대학교 주변 공영주차장',
      address: '서울시 광진구 능동로 120',
      distance: '네비 기준 4분 (300m)',
      price: '2시간 2,000원',
      type: 'cheapest',
      badge: '최저가격',
      badgeColor: Colors.orange,
      rating: 4.1,
      features: ['공영주차', '저렴', '넓음'],
      available: 18,
    ),
  ];

  void _handleSelect(int id, int index) {
    setState(() {
      _selectedIndex = index;
    });
    Future.delayed(const Duration(milliseconds: 300), () {
      widget.onSelectParking?.call(id);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey.shade50,
      body: Column(
        children: [
          // Header
          _buildHeader(),
          // Map Preview
          _buildMapPreview(),
          // Results List
          Expanded(
            child: _buildResultsList(),
          ),
        ],
      ),
    );
  }

  Widget _buildHeader() {
    return Container(
      color: Colors.white,
      padding: const EdgeInsets.all(16),
      child: Row(
        children: [
          IconButton(
            onPressed: widget.onBack,
            icon: const Icon(Icons.arrow_back),
            style: IconButton.styleFrom(
              backgroundColor: Colors.grey.shade100,
            ),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  '추천 주차장',
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.w600,
                    fontFamily: 'Inter',
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  '"${widget.searchQuery}" 검색 결과',
                  style: TextStyle(
                    fontSize: 14,
                    color: Colors.grey.shade600,
                    fontFamily: 'Inter',
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildMapPreview() {
    return Container(
      height: 200,
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
          // 지도 배경
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
                  '지도 미리보기',
                  style: TextStyle(
                    fontSize: 16,
                    color: Colors.blue,
                    fontFamily: 'Inter',
                  ),
                ),
              ],
            ),
          ),
          // 마커들
          ...List.generate(3, (index) {
            return Positioned(
              left: 50 + (index * 80).toDouble(),
              top: 80 + (index % 2) * 40.0,
              child: Container(
                width: 16,
                height: 16,
                decoration: BoxDecoration(
                  color: _recommendations[index].badgeColor,
                  shape: BoxShape.circle,
                  border: Border.all(color: Colors.white, width: 2),
                ),
              ),
            );
          }),
        ],
      ),
    );
  }

  Widget _buildResultsList() {
    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: _recommendations.length,
      itemBuilder: (context, index) {
        final recommendation = _recommendations[index];
        final isSelected = _selectedIndex == index;
        
        return Padding(
          padding: const EdgeInsets.only(bottom: 16),
          child: GestureDetector(
            onTap: () => _handleSelect(recommendation.id, index),
            child: AnimatedContainer(
              duration: const Duration(milliseconds: 200),
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(12),
                border: Border.all(
                  color: isSelected ? recommendation.badgeColor : Colors.grey.shade200,
                  width: isSelected ? 2 : 1,
                ),
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withOpacity(0.05),
                    blurRadius: 8,
                    offset: const Offset(0, 2),
                  ),
                ],
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Header with badge
                  Row(
                    children: [
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                        decoration: BoxDecoration(
                          color: recommendation.badgeColor,
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: Text(
                          recommendation.badge,
                          style: const TextStyle(
                            color: Colors.white,
                            fontSize: 12,
                            fontWeight: FontWeight.w600,
                            fontFamily: 'Inter',
                          ),
                        ),
                      ),
                      const Spacer(),
                      Row(
                        children: [
                          const Icon(
                            Icons.star,
                            size: 16,
                            color: Colors.amber,
                          ),
                          const SizedBox(width: 4),
                          Text(
                            recommendation.rating.toString(),
                            style: const TextStyle(
                              fontSize: 14,
                              fontWeight: FontWeight.w600,
                              fontFamily: 'Inter',
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),
                  // Name
                  Text(
                    recommendation.name,
                    style: const TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.w600,
                      fontFamily: 'Inter',
                    ),
                  ),
                  const SizedBox(height: 4),
                  // Address
                  Text(
                    recommendation.address,
                    style: TextStyle(
                      fontSize: 14,
                      color: Colors.grey.shade600,
                      fontFamily: 'Inter',
                    ),
                  ),
                  const SizedBox(height: 12),
                  // Info row
                  Wrap(
                    spacing: 8,
                    runSpacing: 4,
                    children: [
                      _buildInfoChip(
                        Icons.directions_walk,
                        recommendation.distance,
                        Colors.blue,
                      ),
                      _buildInfoChip(
                        Icons.attach_money,
                        recommendation.price,
                        Colors.green,
                      ),
                      _buildInfoChip(
                        Icons.local_parking,
                        '${recommendation.available}대 가능',
                        recommendation.available > 10 ? Colors.green : Colors.orange,
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),
                  // Features
                  Wrap(
                    spacing: 8,
                    runSpacing: 4,
                    children: recommendation.features.map((feature) {
                      return Container(
                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                        decoration: BoxDecoration(
                          color: Colors.grey.shade100,
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: Text(
                          feature,
                          style: TextStyle(
                            fontSize: 12,
                            color: Colors.grey.shade700,
                            fontFamily: 'Inter',
                          ),
                        ),
                      );
                    }).toList(),
                  ),
                ],
              ),
            ),
          ),
        );
      },
    );
  }

  Widget _buildInfoChip(IconData icon, String text, Color color) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 14, color: color),
          const SizedBox(width: 4),
          Text(
            text,
            style: TextStyle(
              fontSize: 12,
              color: color,
              fontWeight: FontWeight.w500,
              fontFamily: 'Inter',
            ),
          ),
        ],
      ),
    );
  }
}

class ParkingRecommendation {
  final int id;
  final String name;
  final String address;
  final String distance;
  final String price;
  final String type;
  final String badge;
  final Color badgeColor;
  final double rating;
  final List<String> features;
  final int available;

  const ParkingRecommendation({
    required this.id,
    required this.name,
    required this.address,
    required this.distance,
    required this.price,
    required this.type,
    required this.badge,
    required this.badgeColor,
    required this.rating,
    required this.features,
    required this.available,
  });
}
