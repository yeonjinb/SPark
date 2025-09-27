package com.example.spark

import android.os.Bundle
import android.util.Log
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel
import kotlinx.coroutines.*
import java.io.File
// import com.kakao.maps.open.android.KakaoMapSdk
import java.lang.UnsatisfiedLinkError

class MainActivity : FlutterActivity() {
    private val CHANNEL = "vosk_flutter"
    private var voskModel: Any? = null
    private var voskRecognizer: Any? = null
    private var isListening = false
    private val scope = CoroutineScope(Dispatchers.Main + SupervisorJob())

    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)
        
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, CHANNEL).setMethodCallHandler { call, result ->
            when (call.method) {
                "initialize" -> {
                    val modelPath = call.argument<String>("modelPath")
                    if (modelPath != null) {
                        scope.launch {
                            try {
                                initializeVosk(modelPath)
                                result.success(true)
                            } catch (e: Exception) {
                                Log.e("MainActivity", "Vosk 초기화 실패", e)
                                result.error("INIT_ERROR", e.message, null)
                            }
                        }
                    } else {
                        result.error("INVALID_ARGUMENT", "Model path is null", null)
                    }
                }
                "startListening" -> {
                    scope.launch {
                        try {
                            startVoskListening()
                            result.success(null)
                        } catch (e: Exception) {
                            Log.e("MainActivity", "음성 인식 시작 실패", e)
                            result.error("START_ERROR", e.message, null)
                        }
                    }
                }
                "stopListening" -> {
                    scope.launch {
                        try {
                            stopVoskListening()
                            result.success(null)
                        } catch (e: Exception) {
                            Log.e("MainActivity", "음성 인식 중지 실패", e)
                            result.error("STOP_ERROR", e.message, null)
                        }
                    }
                }
                else -> {
                    result.notImplemented()
                }
            }
        }
    }

    private suspend fun initializeVosk(modelPath: String) = withContext(Dispatchers.IO) {
        try {
            val modelDir = File(modelPath)
            if (!modelDir.exists()) {
                throw Exception("Vosk 모델 디렉토리가 존재하지 않습니다: $modelPath")
            }
            
            Log.d("MainActivity", "Vosk 모델 초기화 시작: $modelPath")
            
            // Vosk 모델 초기화 (실제 구현은 Vosk 라이브러리 사용)
            // 여기서는 시뮬레이션
            Thread.sleep(1000) // 초기화 시뮬레이션
            
            Log.d("MainActivity", "Vosk 모델 초기화 완료")
        } catch (e: Exception) {
            Log.e("MainActivity", "Vosk 초기화 실패", e)
            throw e
        }
    }

    private suspend fun startVoskListening() = withContext(Dispatchers.IO) {
        if (isListening) return@withContext
        
        try {
            Log.d("MainActivity", "음성 인식 시작")
            isListening = true
            
            // 실제 음성 인식 로직은 여기에 구현
            // 현재는 시뮬레이션
            scope.launch {
                while (isListening) {
                    delay(2000) // 2초마다 시뮬레이션 결과 전송
                    if (isListening) {
                        sendRecognitionResult("음성 인식 테스트 결과")
                    }
                }
            }
        } catch (e: Exception) {
            Log.e("MainActivity", "음성 인식 시작 실패", e)
            throw e
        }
    }

    private suspend fun stopVoskListening() = withContext(Dispatchers.IO) {
        try {
            Log.d("MainActivity", "음성 인식 중지")
            isListening = false
        } catch (e: Exception) {
            Log.e("MainActivity", "음성 인식 중지 실패", e)
            throw e
        }
    }

    private fun sendRecognitionResult(text: String) {
        try {
            val messenger = flutterEngine?.dartExecutor?.binaryMessenger
            if (messenger != null) {
                val channel = MethodChannel(messenger, CHANNEL)
                channel.invokeMethod("onResult", mapOf("text" to text))
            }
        } catch (e: Exception) {
            Log.e("MainActivity", "결과 전송 실패", e)
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        // 카카오지도 SDK는 Flutter 플러그인을 통해 초기화됩니다
        // try {
        //     // 카카오지도 SDK 초기화 (실제 기기에서만)
        //     KakaoMapSdk.init(this, "fc9248fb37c47471e8ac96d2336946f2")
        // } catch (e: UnsatisfiedLinkError) {
        //     // 에뮬레이터에서 아키텍처 불일치 시 무시
        //     Log.w("MainActivity", "카카오지도 SDK 초기화 실패 (에뮬레이터): ${e.message}")
        // }
    }

    override fun onDestroy() {
        super.onDestroy()
        scope.cancel()
    }
}
