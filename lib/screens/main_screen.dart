import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../providers/app_state_provider.dart';
import '../theme/app_theme.dart';
import '../widgets/figma_components/parking_card.dart';
import '../widgets/figma_components/voice_search_button.dart';

class MainScreen extends ConsumerStatefulWidget {
  const MainScreen({super.key});

  @override
  ConsumerState<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends ConsumerState<MainScreen> {
  int _selectedIndex = 0;

  @override
  Widget build(BuildContext context) {
    final recommendedParkings = ref.watch(recommendedParkingsProvider);
    final isLoggedIn = ref.watch(isLoggedInProvider);

    return Scaffold(
      backgroundColor: AppTheme.backgroundBlue,
      body: Stack(
        children: [
          // 지도 영역 (가상 마커들)
          _buildMapArea(),
          
          // 상단 앱바
          _buildTopAppBar(),
          
          // 주변 주차장 카드들
          _buildParkingCards(recommendedParkings),
          
          // 음성 검색 버튼
          _buildVoiceSearchButton(),
        ],
      ),
      bottomNavigationBar: _buildBottomNavigationBar(isLoggedIn),
    );
  }

  Widget _buildMapArea() {
    return Container(
      width: double.infinity,
      height: double.infinity,
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
          colors: [
            AppTheme.primaryBlue.withOpacity(0.1),
            AppTheme.backgroundBlue,
          ],
        ),
      ),
      child: Stack(
        children: [
          // 가상 지도 배경
          Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(
                  Icons.map,
                  size: 120,
                  color: AppTheme.primaryBlue.withOpacity(0.3),
                ),
                const SizedBox(height: 16),
                Text(
                  '지도 영역',
                  style: AppTheme.koreanTextStyle(
                    fontSize: 18,
                    color: AppTheme.textSecondary,
                  ),
                ),
                Text(
                  '카카오맵이 여기에 표시됩니다',
                  style: AppTheme.koreanTextStyle(
                    fontSize: 14,
                    color: AppTheme.textTertiary,
                  ),
                ),
              ],
            ),
          ),
          // 가상 마커들
          ...List.generate(5, (index) {
            return Positioned(
              left: 50 + (index * 60).toDouble(),
              top: 200 + (index % 2) * 100.0,
              child: Container(
                width: 20,
                height: 20,
                decoration: BoxDecoration(
                  color: AppTheme.primaryBlue,
                  shape: BoxShape.circle,
                  border: Border.all(color: Colors.white, width: 3),
                  boxShadow: [
                    BoxShadow(
                      color: AppTheme.primaryBlue.withOpacity(0.3),
                      blurRadius: 8,
                      spreadRadius: 2,
                    ),
                  ],
                ),
              ),
            );
          }),
        ],
      ),
    );
  }

  Widget _buildTopAppBar() {
    return Positioned(
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
        decoration: BoxDecoration(
          color: Colors.white,
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.05),
              blurRadius: 10,
              offset: const Offset(0, 2),
            ),
          ],
        ),
        child: Row(
          children: [
            // 현재 위치 표시
            Icon(
              Icons.my_location,
              color: AppTheme.primaryBlue,
              size: 20,
            ),
            const SizedBox(width: 8),
            Expanded(
              child: Text(
                '강남역 근처',
                style: AppTheme.koreanTextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.w600,
                  color: AppTheme.textPrimary,
                ),
              ),
            ),
            // 알림 버튼
            IconButton(
              onPressed: () {},
              icon: Icon(
                Icons.notifications_outlined,
                color: AppTheme.textSecondary,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildParkingCards(List<ParkingLot> parkings) {
    return Positioned(
      bottom: 100,
      left: 0,
      right: 0,
      child: Container(
        height: 200,
        child: ListView.builder(
          scrollDirection: Axis.horizontal,
          padding: const EdgeInsets.symmetric(horizontal: 20),
          itemCount: parkings.length,
          itemBuilder: (context, index) {
            return Padding(
              padding: const EdgeInsets.only(right: 16),
              child: ParkingCard(
                parking: parkings[index],
                onTap: () {
                  ref.read(selectedParkingIdProvider.notifier).state = parkings[index].id;
                  ref.read(appStateProvider.notifier).goToDetails();
                },
              ),
            );
          },
        ),
      ),
    );
  }

  Widget _buildVoiceSearchButton() {
    return Positioned(
      bottom: 20,
      right: 20,
      child: VoiceSearchButton(
        onPressed: () {
          ref.read(appStateProvider.notifier).goToVoiceLoading();
        },
      ),
    );
  }

  Widget _buildBottomNavigationBar(bool isLoggedIn) {
    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.1),
            blurRadius: 10,
            offset: const Offset(0, -2),
          ),
        ],
      ),
      child: BottomNavigationBar(
        currentIndex: _selectedIndex,
        onTap: (index) {
          setState(() {
            _selectedIndex = index;
          });
          
          switch (index) {
            case 0:
              // 이미 메인 화면
              break;
            case 1:
              ref.read(appStateProvider.notifier).goToMyPage();
              break;
            case 2:
              if (isLoggedIn) {
                ref.read(appStateProvider.notifier).goToMyProfile();
              } else {
                ref.read(appStateProvider.notifier).goToMain(); // 로그인 화면으로
              }
              break;
          }
        },
        type: BottomNavigationBarType.fixed,
        selectedItemColor: AppTheme.primaryBlue,
        unselectedItemColor: AppTheme.textTertiary,
        items: [
          const BottomNavigationBarItem(
            icon: Icon(Icons.explore),
            label: '탐색',
          ),
          const BottomNavigationBarItem(
            icon: Icon(Icons.favorite),
            label: '내페이지',
          ),
          BottomNavigationBarItem(
            icon: Icon(isLoggedIn ? Icons.person : Icons.login),
            label: isLoggedIn ? '내정보' : '로그인',
          ),
        ],
      ),
    );
  }
}
