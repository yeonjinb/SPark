import 'dart:async';
import 'package:flutter/material.dart';
import '../services/vosk_service.dart';

class VoiceRecognitionWidget extends StatefulWidget {
  final Function(String) onResult;
  final Function(String)? onError;
  final VoidCallback? onStart;
  final VoidCallback? onStop;

  const VoiceRecognitionWidget({
    super.key,
    required this.onResult,
    this.onError,
    this.onStart,
    this.onStop,
  });

  @override
  State<VoiceRecognitionWidget> createState() => _VoiceRecognitionWidgetState();
}

class _VoiceRecognitionWidgetState extends State<VoiceRecognitionWidget>
    with TickerProviderStateMixin {
  bool _isListening = false;
  bool _isInitialized = false;
  String _recognizedText = '';
  StreamSubscription<String>? _recognitionSubscription;
  late AnimationController _pulseController;
  late AnimationController _waveController;
  late Animation<double> _pulseAnimation;
  late Animation<double> _waveAnimation;

  @override
  void initState() {
    super.initState();
    _initializeAnimations();
    _initializeVosk();
  }

  void _initializeAnimations() {
    _pulseController = AnimationController(
      duration: const Duration(milliseconds: 1000),
      vsync: this,
    );
    _waveController = AnimationController(
      duration: const Duration(milliseconds: 1500),
      vsync: this,
    );

    _pulseAnimation = Tween<double>(
      begin: 1.0,
      end: 1.2,
    ).animate(CurvedAnimation(
      parent: _pulseController,
      curve: Curves.easeInOut,
    ));

    _waveAnimation = Tween<double>(
      begin: 0.0,
      end: 1.0,
    ).animate(CurvedAnimation(
      parent: _waveController,
      curve: Curves.easeInOut,
    ));
  }

  Future<void> _initializeVosk() async {
    try {
      print('Vosk 초기화 시작...');
      final success = await VoskService.initialize();
      print('Vosk 초기화 결과: $success');
      if (mounted) {
        setState(() {
          _isInitialized = success;
        });
        if (success) {
          print('Vosk가 성공적으로 초기화되었습니다.');
        } else {
          print('Vosk 초기화에 실패했습니다.');
        }
      }
    } catch (e) {
      print('Vosk 초기화 중 오류 발생: $e');
      if (mounted) {
        widget.onError?.call('Vosk 초기화 실패: $e');
      }
    }
  }

  Future<void> _startListening() async {
    if (!_isInitialized || _isListening) return;

    try {
      widget.onStart?.call();
      
      final stream = VoskService.startListening();
      _recognitionSubscription = stream.listen(
        (text) {
          setState(() {
            _recognizedText = text;
          });
          widget.onResult(text);
        },
        onError: (error) {
          widget.onError?.call('음성 인식 오류: $error');
          _stopListening();
        },
      );

      setState(() {
        _isListening = true;
      });

      _pulseController.repeat(reverse: true);
      _waveController.repeat();
    } catch (e) {
      widget.onError?.call('음성 인식 시작 실패: $e');
    }
  }

  Future<void> _stopListening() async {
    if (!_isListening) return;

    try {
      await VoskService.stopListening();
      _recognitionSubscription?.cancel();
      _recognitionSubscription = null;

      setState(() {
        _isListening = false;
      });

      _pulseController.stop();
      _waveController.stop();
      _pulseController.reset();
      _waveController.reset();

      widget.onStop?.call();
    } catch (e) {
      widget.onError?.call('음성 인식 중지 실패: $e');
    }
  }

  @override
  void dispose() {
    _recognitionSubscription?.cancel();
    _pulseController.dispose();
    _waveController.dispose();
    VoskService.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(24),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          // 음성 인식 상태 표시
          if (!_isInitialized)
            const Text(
              '음성 인식 초기화 중...',
              style: TextStyle(
                fontSize: 16,
                color: Colors.grey,
                fontFamily: 'Inter',
              ),
            )
          else if (_isListening)
            const Text(
              '듣고 있습니다...',
              style: TextStyle(
                fontSize: 16,
                color: Colors.blue,
                fontWeight: FontWeight.w600,
                fontFamily: 'Inter',
              ),
            )
          else
            const Text(
              '마이크를 눌러 음성으로 검색하세요',
              style: TextStyle(
                fontSize: 16,
                color: Colors.grey,
                fontFamily: 'Inter',
              ),
            ),

          const SizedBox(height: 24),

          // 음성 인식 버튼
          GestureDetector(
            onTap: _isListening ? _stopListening : _startListening,
            child: AnimatedBuilder(
              animation: _pulseAnimation,
              builder: (context, child) {
                return Transform.scale(
                  scale: _isListening ? _pulseAnimation.value : 1.0,
                  child: Container(
                    width: 120,
                    height: 120,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      color: _isListening ? Colors.red : Colors.blue,
                      boxShadow: [
                        BoxShadow(
                          color: (_isListening ? Colors.red : Colors.blue)
                              .withOpacity(0.3),
                          blurRadius: 20,
                          spreadRadius: 5,
                        ),
                      ],
                    ),
                    child: Icon(
                      _isListening ? Icons.stop : Icons.mic,
                      size: 48,
                      color: Colors.white,
                    ),
                  ),
                );
              },
            ),
          ),

          const SizedBox(height: 24),

          // 음파 애니메이션
          if (_isListening)
            AnimatedBuilder(
              animation: _waveAnimation,
              builder: (context, child) {
                return Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: List.generate(5, (index) {
                    final delay = index * 0.2;
                    final animationValue = (_waveAnimation.value + delay) % 1.0;
                    final height = 20 + (animationValue * 40);
                    
                    return Container(
                      width: 4,
                      height: height,
                      margin: const EdgeInsets.symmetric(horizontal: 2),
                      decoration: BoxDecoration(
                        color: Colors.blue.withOpacity(0.7),
                        borderRadius: BorderRadius.circular(2),
                      ),
                    );
                  }),
                );
              },
            ),

          const SizedBox(height: 16),

          // 인식된 텍스트 표시
          if (_recognizedText.isNotEmpty)
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Colors.grey.shade100,
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: Colors.grey.shade300),
              ),
              child: Text(
                _recognizedText,
                style: const TextStyle(
                  fontSize: 16,
                  fontFamily: 'Inter',
                ),
                textAlign: TextAlign.center,
              ),
            ),

          const SizedBox(height: 16),

          // 인식된 텍스트 지우기 버튼 (필요한 경우에만)
          if (_recognizedText.isNotEmpty)
            ElevatedButton.icon(
              onPressed: () {
                setState(() {
                  _recognizedText = '';
                });
              },
              icon: const Icon(Icons.clear, size: 20),
              label: const Text('텍스트 지우기'),
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.grey,
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(
                  horizontal: 24,
                  vertical: 12,
                ),
              ),
            ),
        ],
      ),
    );
  }
}
