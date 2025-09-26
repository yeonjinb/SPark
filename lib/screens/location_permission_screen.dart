import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:permission_handler/permission_handler.dart';
import '../providers/app_state_provider.dart';
import '../theme/app_theme.dart';

class LocationPermissionScreen extends ConsumerStatefulWidget {
  const LocationPermissionScreen({super.key});

  @override
  ConsumerState<LocationPermissionScreen> createState() => _LocationPermissionScreenState();
}

class _LocationPermissionScreenState extends ConsumerState<LocationPermissionScreen> {
  bool _isRequesting = false;

  Future<void> _requestLocationPermission() async {
    setState(() {
      _isRequesting = true;
    });

    try {
      final status = await Permission.location.request();
      
      if (status.isGranted) {
        ref.read(locationPermissionGrantedProvider.notifier).state = true;
        ref.read(appStateProvider.notifier).goToMain();
      } else {
        // 권한이 거부된 경우
        _showPermissionDeniedDialog();
      }
    } catch (e) {
      // 오류 발생 시
      ref.read(errorTypeProvider.notifier).state = ErrorType.location;
      ref.read(appStateProvider.notifier).goToError();
    } finally {
      setState(() {
        _isRequesting = false;
      });
    }
  }

  void _showPermissionDeniedDialog() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text(
          '위치 권한 필요',
          style: AppTheme.koreanTextStyle(
            fontSize: 18,
            fontWeight: FontWeight.w600,
          ),
        ),
        content: Text(
          '주차장 추천을 위해 위치 정보가 필요합니다.\n설정에서 위치 권한을 허용해주세요.',
          style: AppTheme.koreanTextStyle(fontSize: 14),
        ),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.of(context).pop();
              ref.read(appStateProvider.notifier).goToMain();
            },
            child: Text(
              '나중에',
              style: AppTheme.koreanTextStyle(
                fontSize: 14,
                color: AppTheme.textSecondary,
              ),
            ),
          ),
          ElevatedButton(
            onPressed: () {
              Navigator.of(context).pop();
              openAppSettings();
            },
            child: Text(
              '설정으로 이동',
              style: AppTheme.koreanTextStyle(
                fontSize: 14,
                color: Colors.white,
              ),
            ),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.backgroundBlue,
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            children: [
              const SizedBox(height: 60),
              // 위치 아이콘
              Container(
                width: 120,
                height: 120,
                decoration: BoxDecoration(
                  color: AppTheme.primaryBlue.withOpacity(0.1),
                  shape: BoxShape.circle,
                ),
                child: const Icon(
                  Icons.location_on,
                  size: 60,
                  color: AppTheme.primaryBlue,
                ),
              ),
              const SizedBox(height: 40),
              // 제목
              Text(
                '위치 권한이 필요합니다',
                style: AppTheme.koreanTextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                  color: AppTheme.textPrimary,
                ),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 16),
              // 설명
              Text(
                '주변 주차장을 찾고 추천하기 위해\n위치 정보가 필요합니다',
                style: AppTheme.koreanTextStyle(
                  fontSize: 16,
                  color: AppTheme.textSecondary,
                ),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 40),
              // 개인정보 보호 설명 카드
              Container(
                padding: const EdgeInsets.all(20),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: AppTheme.borderColor),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Icon(
                          Icons.security,
                          size: 20,
                          color: AppTheme.primaryBlue,
                        ),
                        const SizedBox(width: 8),
                        Text(
                          '개인정보 보호',
                          style: AppTheme.koreanTextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.w600,
                            color: AppTheme.textPrimary,
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 12),
                    Text(
                      '• 위치 정보는 주차장 추천 목적으로만 사용됩니다\n• 개인을 식별할 수 없는 익명화된 데이터로 처리됩니다\n• 언제든지 설정에서 권한을 변경할 수 있습니다',
                      style: AppTheme.koreanTextStyle(
                        fontSize: 14,
                        color: AppTheme.textSecondary,
                      ),
                    ),
                  ],
                ),
              ),
              const Spacer(),
              // 버튼들
              Column(
                children: [
                  SizedBox(
                    width: double.infinity,
                    child: ElevatedButton(
                      onPressed: _isRequesting ? null : _requestLocationPermission,
                      child: _isRequesting
                          ? const SizedBox(
                              width: 20,
                              height: 20,
                              child: CircularProgressIndicator(
                                strokeWidth: 2,
                                valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                              ),
                            )
                          : Text(
                              '위치 권한 허용',
                              style: AppTheme.koreanTextStyle(
                                fontSize: 16,
                                fontWeight: FontWeight.w600,
                                color: Colors.white,
                              ),
                            ),
                    ),
                  ),
                  const SizedBox(height: 12),
                  SizedBox(
                    width: double.infinity,
                    child: OutlinedButton(
                      onPressed: _isRequesting ? null : () {
                        ref.read(appStateProvider.notifier).goToMain();
                      },
                      child: Text(
                        '나중에 설정',
                        style: AppTheme.koreanTextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.w600,
                          color: AppTheme.primaryBlue,
                        ),
                      ),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 20),
            ],
          ),
        ),
      ),
    );
  }
}
