import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class SimpleMapPage extends StatelessWidget {
  const SimpleMapPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('SPark 지도'),
        backgroundColor: AppTheme.primaryBlue,
        foregroundColor: Colors.white,
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.map,
              size: 100,
              color: AppTheme.primaryBlue,
            ),
            const SizedBox(height: 20),
            Text(
              '지도 화면',
              style: AppTheme.koreanTextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 10),
            Text(
              '카카오맵이 여기에 표시됩니다',
              style: AppTheme.koreanTextStyle(
                fontSize: 16,
                color: AppTheme.textSecondary,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
