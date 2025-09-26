import 'package:flutter/material.dart';
import '../../providers/app_state_provider.dart';
import '../../theme/app_theme.dart';

class ParkingCard extends StatelessWidget {
  final ParkingLot parking;
  final VoidCallback? onTap;

  const ParkingCard({
    super.key,
    required this.parking,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        width: 280,
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(16),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.1),
              blurRadius: 10,
              offset: const Offset(0, 4),
            ),
          ],
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // 주차장 이미지 (가상)
            Container(
              height: 120,
              decoration: BoxDecoration(
                color: AppTheme.surfaceBlue,
                borderRadius: const BorderRadius.only(
                  topLeft: Radius.circular(16),
                  topRight: Radius.circular(16),
                ),
              ),
              child: Stack(
                children: [
                  Center(
                    child: Icon(
                      Icons.local_parking,
                      size: 40,
                      color: AppTheme.primaryBlue.withOpacity(0.3),
                    ),
                  ),
                  // 타입 배지
                  Positioned(
                    top: 12,
                    left: 12,
                    child: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                      decoration: BoxDecoration(
                        color: _getTypeColor(parking.type),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Text(
                        _getTypeText(parking.type),
                        style: AppTheme.koreanTextStyle(
                          fontSize: 12,
                          fontWeight: FontWeight.w600,
                          color: Colors.white,
                        ),
                      ),
                    ),
                  ),
                  // 별점
                  Positioned(
                    top: 12,
                    right: 12,
                    child: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 4),
                      decoration: BoxDecoration(
                        color: Colors.black.withOpacity(0.6),
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          const Icon(
                            Icons.star,
                            size: 14,
                            color: Colors.amber,
                          ),
                          const SizedBox(width: 2),
                          Text(
                            parking.rating.toString(),
                            style: AppTheme.koreanTextStyle(
                              fontSize: 12,
                              fontWeight: FontWeight.w600,
                              color: Colors.white,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            ),
            // 주차장 정보
            Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // 주차장 이름
                  Text(
                    parking.name,
                    style: AppTheme.koreanTextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.w600,
                      color: AppTheme.textPrimary,
                    ),
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                  ),
                  const SizedBox(height: 4),
                  // 주소
                  Text(
                    parking.address,
                    style: AppTheme.koreanTextStyle(
                      fontSize: 12,
                      color: AppTheme.textSecondary,
                    ),
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                  ),
                  const SizedBox(height: 12),
                  // 거리, 가격, 주차 가능
                  Row(
                    children: [
                      _buildInfoChip(
                        Icons.directions_walk,
                        parking.distance,
                        AppTheme.primaryBlue,
                      ),
                      const SizedBox(width: 8),
                      _buildInfoChip(
                        Icons.attach_money,
                        parking.price,
                        AppTheme.textSecondary,
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  // 주차 가능 대수
                  Row(
                    children: [
                      Icon(
                        Icons.local_parking,
                        size: 16,
                        color: parking.available > 0 ? Colors.green : Colors.red,
                      ),
                      const SizedBox(width: 4),
                      Text(
                        '${parking.available}대 주차 가능',
                        style: AppTheme.koreanTextStyle(
                          fontSize: 12,
                          color: parking.available > 0 ? Colors.green : Colors.red,
                          fontWeight: FontWeight.w500,
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
            style: AppTheme.koreanTextStyle(
              fontSize: 12,
              color: color,
              fontWeight: FontWeight.w500,
            ),
          ),
        ],
      ),
    );
  }

  Color _getTypeColor(ParkingType type) {
    switch (type) {
      case ParkingType.optimal:
        return AppTheme.primaryBlue;
      case ParkingType.nearest:
        return Colors.green;
      case ParkingType.cheapest:
        return Colors.orange;
    }
  }

  String _getTypeText(ParkingType type) {
    switch (type) {
      case ParkingType.optimal:
        return '최적';
      case ParkingType.nearest:
        return '최단거리';
      case ParkingType.cheapest:
        return '최저가격';
    }
  }
}
