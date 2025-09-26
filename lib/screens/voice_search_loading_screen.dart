import 'dart:async';
import 'package:flutter/material.dart';
import '../widgets/voice_recognition_widget.dart';

class VoiceSearchLoadingScreen extends StatefulWidget {
  final VoidCallback? onComplete;
  final VoidCallback? onError;
  final String? recognizedText;

  const VoiceSearchLoadingScreen({
    super.key,
    this.onComplete,
    this.onError,
    this.recognizedText,
  });

  @override
  State<VoiceSearchLoadingScreen> createState() => _VoiceSearchLoadingScreenState();
}

class _VoiceSearchLoadingScreenState extends State<VoiceSearchLoadingScreen>
    with TickerProviderStateMixin {
  late AnimationController _waveController;
  late AnimationController _pulseController;
  late AnimationController _progressController;
  late Animation<double> _waveAnimation;
  late Animation<double> _pulseAnimation;
  late Animation<double> _progressAnimation;

  int _currentStep = 0;
  double _progress = 0.0;
  Timer? _progressTimer;

  final List<VoiceStep> _steps = [
    VoiceStep(
      icon: Icons.mic,
      text: '음성을 인식하고 있습니다...',
      duration: 2000,
    ),
    VoiceStep(
      icon: Icons.volume_up,
      text: '요청을 분석하고 있습니다...',
      duration: 1500,
    ),
    VoiceStep(
      icon: Icons.location_on,
      text: '주변 주차장을 검색하고 있습니다...',
      duration: 2000,
    ),
    VoiceStep(
      icon: Icons.local_parking,
      text: '최적의 주차장을 찾고 있습니다...',
      duration: 1500,
    ),
  ];

  @override
  void initState() {
    super.initState();
    
    // 파형 애니메이션
    _waveController = AnimationController(
      duration: const Duration(milliseconds: 1000),
      vsync: this,
    );
    _waveAnimation = Tween<double>(
      begin: 0.0,
      end: 1.0,
    ).animate(CurvedAnimation(
      parent: _waveController,
      curve: Curves.easeInOut,
    ));

    // 펄스 애니메이션
    _pulseController = AnimationController(
      duration: const Duration(milliseconds: 1500),
      vsync: this,
    );
    _pulseAnimation = Tween<double>(
      begin: 0.8,
      end: 1.2,
    ).animate(CurvedAnimation(
      parent: _pulseController,
      curve: Curves.easeInOut,
    ));

    // 진행률 애니메이션
    _progressController = AnimationController(
      duration: const Duration(milliseconds: 100),
      vsync: this,
    );
    _progressAnimation = Tween<double>(
      begin: 0.0,
      end: 1.0,
    ).animate(_progressController);

    _startVoiceSearch();
  }

  void _startVoiceSearch() {
    _waveController.repeat();
    _pulseController.repeat(reverse: true);
    _processStep(0);
  }

  void _processStep(int stepIndex) {
    if (stepIndex >= _steps.length) {
      // 모든 단계 완료
      Future.delayed(const Duration(milliseconds: 500), () {
        if (mounted) {
          // 5% 확률로 에러 발생 시뮬레이션
          if (0.05 > (DateTime.now().millisecondsSinceEpoch % 100) / 100) {
            widget.onError?.call();
          } else {
            widget.onComplete?.call();
          }
        }
      });
      return;
    }

    setState(() {
      _currentStep = stepIndex;
      _progress = 0.0;
    });

    final step = _steps[stepIndex];
    final progressInterval = step.duration / 100;

    _progressTimer?.cancel();
    _progressTimer = Timer.periodic(Duration(milliseconds: progressInterval.round()), (timer) {
      if (!mounted) {
        timer.cancel();
        return;
      }

      setState(() {
        _progress += 1.0;
      });

      if (_progress >= 100) {
        timer.cancel();
        _processStep(stepIndex + 1);
      }
    });
  }

  @override
  void dispose() {
    _waveController.dispose();
    _pulseController.dispose();
    _progressController.dispose();
    _progressTimer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            children: [
              const SizedBox(height: 40),
              // 뒤로가기 버튼
              Row(
                children: [
                  IconButton(
                    onPressed: () {
                      Navigator.of(context).pop();
                    },
                    icon: const Icon(Icons.arrow_back),
                    style: IconButton.styleFrom(
                      backgroundColor: Colors.grey.shade100,
                      foregroundColor: Colors.black87,
                    ),
                  ),
                ],
              ),
              const Spacer(),
              // SPARK 로고
              _buildLogo(),
              const SizedBox(height: 60),
              // 음성 파형 애니메이션
              _buildVoiceWaveAnimation(),
              const SizedBox(height: 40),
              // 현재 단계 표시
              _buildCurrentStep(),
              const SizedBox(height: 40),
              // 진행률 바
              _buildProgressBar(),
              const Spacer(),
              // 취소 버튼
              _buildCancelButton(),
              const SizedBox(height: 20),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildLogo() {
    return Column(
      children: [
        Container(
          width: 48,
          height: 48,
          decoration: BoxDecoration(
            color: Colors.blue.shade600,
            shape: BoxShape.circle,
          ),
          child: const Icon(
            Icons.flash_on,
            color: Colors.white,
            size: 24,
          ),
        ),
        const SizedBox(height: 16),
        Text(
          'spark',
          style: TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.bold,
            color: Colors.blue.shade900,
            fontFamily: 'Inter',
            fontStyle: FontStyle.italic,
          ),
        ),
      ],
    );
  }

  Widget _buildVoiceWaveAnimation() {
    return AnimatedBuilder(
      animation: _waveAnimation,
      builder: (context, child) {
        return Column(
          children: [
            // 중앙 마이크 아이콘
            AnimatedBuilder(
              animation: _pulseAnimation,
              builder: (context, child) {
                return Transform.scale(
                  scale: _pulseAnimation.value,
                  child: Container(
                    width: 120,
                    height: 120,
                    decoration: BoxDecoration(
                      color: Colors.blue.shade600,
                      shape: BoxShape.circle,
                      boxShadow: [
                        BoxShadow(
                          color: Colors.blue.shade600.withOpacity(0.3),
                          blurRadius: 30,
                          spreadRadius: 10,
                        ),
                      ],
                    ),
                    child: const Icon(
                      Icons.mic,
                      color: Colors.white,
                      size: 50,
                    ),
                  ),
                );
              },
            ),
            const SizedBox(height: 40),
            // 파형 바들
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: List.generate(5, (index) {
                final delay = index * 0.1;
                final animationValue = (_waveAnimation.value - delay).clamp(0.0, 1.0);
                final height = 20 + (40 * (1 - (animationValue * 2 - 1).abs()));
                
                return Container(
                  margin: const EdgeInsets.symmetric(horizontal: 3),
                  width: 6,
                  height: height,
                  decoration: BoxDecoration(
                    color: Colors.blue.shade600.withOpacity(0.7),
                    borderRadius: BorderRadius.circular(3),
                  ),
                );
              }),
            ),
          ],
        );
      },
    );
  }

  Widget _buildCurrentStep() {
    final step = _steps[_currentStep];
    
    return Column(
      children: [
        Icon(
          step.icon,
          size: 48,
          color: Colors.blue.shade600,
        ),
        const SizedBox(height: 16),
        Text(
          step.text,
          style: const TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.w600,
            color: Colors.black87,
            fontFamily: 'Inter',
          ),
          textAlign: TextAlign.center,
        ),
        const SizedBox(height: 8),
        Text(
          '${_currentStep + 1}/${_steps.length}',
          style: TextStyle(
            fontSize: 14,
            color: Colors.grey.shade600,
            fontFamily: 'Inter',
          ),
        ),
      ],
    );
  }

  Widget _buildProgressBar() {
    return Column(
      children: [
        LinearProgressIndicator(
          value: _progress / 100,
          backgroundColor: Colors.grey.shade300,
          valueColor: AlwaysStoppedAnimation<Color>(Colors.blue.shade600),
          minHeight: 8,
        ),
        const SizedBox(height: 8),
        Text(
          '${_progress.round()}%',
          style: TextStyle(
            fontSize: 14,
            color: Colors.grey.shade600,
            fontFamily: 'Inter',
          ),
        ),
      ],
    );
  }

  Widget _buildCancelButton() {
    return SizedBox(
      width: double.infinity,
      child: OutlinedButton(
        onPressed: () {
          Navigator.of(context).pop();
        },
        style: OutlinedButton.styleFrom(
          side: BorderSide(color: Colors.blue.shade600),
          padding: const EdgeInsets.symmetric(vertical: 16),
        ),
        child: Text(
          '취소',
          style: TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.w600,
            color: Colors.blue.shade600,
            fontFamily: 'Inter',
          ),
        ),
      ),
    );
  }
}

class VoiceStep {
  final IconData icon;
  final String text;
  final int duration;

  const VoiceStep({
    required this.icon,
    required this.text,
    required this.duration,
  });
}