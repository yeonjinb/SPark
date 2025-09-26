import 'dart:async';
import 'dart:io';
import 'package:flutter/services.dart';
import 'package:path_provider/path_provider.dart';
import 'package:permission_handler/permission_handler.dart';

class VoskService {
  static const MethodChannel _channel = MethodChannel('vosk_flutter');
  static bool _isInitialized = false;
  static bool _isListening = false;
  static StreamController<String>? _recognitionController;

  /// Vosk 모델 초기화
  static Future<bool> initialize() async {
    if (_isInitialized) return true;

    try {
      // 마이크 권한 요청
      final micPermission = await Permission.microphone.request();
      if (!micPermission.isGranted) {
        print('마이크 권한이 거부되었습니다.');
        return false;
      }

      // Vosk 모델 경로 설정
      final modelPath = await _getModelPath();
      if (modelPath == null) {
        print('Vosk 모델을 찾을 수 없습니다.');
        return false;
      }

      // Vosk 초기화
      final result = await _channel.invokeMethod('initialize', {
        'modelPath': modelPath,
      });

      _isInitialized = result == true;
      print('Vosk 초기화: $_isInitialized');
      return _isInitialized;
    } catch (e) {
      print('Vosk 초기화 실패: $e');
      return false;
    }
  }

  /// 모델 경로 가져오기
  static Future<String?> _getModelPath() async {
    try {
      final directory = await getApplicationDocumentsDirectory();
      final modelDir = Directory('${directory.path}/vosk-model');
      
      if (!await modelDir.exists()) {
        // assets에서 모델 복사
        await _copyModelFromAssets();
      }
      
      return modelDir.path;
    } catch (e) {
      print('모델 경로 설정 실패: $e');
      return null;
    }
  }

  /// Assets에서 모델 복사
  static Future<void> _copyModelFromAssets() async {
    try {
      final directory = await getApplicationDocumentsDirectory();
      final modelDir = Directory('${directory.path}/vosk-model');
      await modelDir.create(recursive: true);

      // 모델 파일들을 assets에서 복사
      final modelFiles = [
        'am/final.mdl',
        'am/final.occs',
        'am/final.mat',
        'am/final.occs',
        'am/final.mdl',
        'graph/phones.txt',
        'graph/words.txt',
        'ivector/final.ie',
        'ivector/global_cmvn.stats',
        'ivector/splice_opts',
        'conf/mfcc.conf',
        'conf/model.conf',
      ];

      for (final file in modelFiles) {
        try {
          final data = await rootBundle.load('assets/models/vosk-model-small-ko-0.22/$file');
          final filePath = '${modelDir.path}/$file';
          final fileDir = Directory(filePath.substring(0, filePath.lastIndexOf('/')));
          await fileDir.create(recursive: true);
          
          final fileHandle = File(filePath);
          await fileHandle.writeAsBytes(data.buffer.asUint8List());
        } catch (e) {
          print('파일 복사 실패 ($file): $e');
        }
      }
    } catch (e) {
      print('모델 복사 실패: $e');
    }
  }

  /// 음성 인식 시작
  static Stream<String> startListening() {
    if (!_isInitialized) {
      throw Exception('Vosk가 초기화되지 않았습니다.');
    }

    if (_isListening) {
      throw Exception('이미 음성 인식이 진행 중입니다.');
    }

    _recognitionController = StreamController<String>.broadcast();
    _isListening = true;

    // 네이티브 메서드 호출
    _channel.invokeMethod('startListening');

    // 결과 스트림 리스너 설정
    _channel.setMethodCallHandler((call) async {
      switch (call.method) {
        case 'onResult':
          final text = call.arguments['text'] as String? ?? '';
          if (text.isNotEmpty) {
            _recognitionController?.add(text);
          }
          break;
        case 'onError':
          final error = call.arguments['error'] as String? ?? '알 수 없는 오류';
          _recognitionController?.addError(Exception(error));
          break;
      }
    });

    return _recognitionController!.stream;
  }

  /// 음성 인식 중지
  static Future<void> stopListening() async {
    if (!_isListening) return;

    try {
      await _channel.invokeMethod('stopListening');
      _isListening = false;
      await _recognitionController?.close();
      _recognitionController = null;
    } catch (e) {
      print('음성 인식 중지 실패: $e');
    }
  }

  /// 현재 상태 확인
  static bool get isInitialized => _isInitialized;
  static bool get isListening => _isListening;

  /// 리소스 정리
  static Future<void> dispose() async {
    if (_isListening) {
      await stopListening();
    }
    _isInitialized = false;
  }
}
