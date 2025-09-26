package com.example.spark

import android.os.Bundle
import android.util.Log
import io.flutter.embedding.android.FlutterActivity
import com.kakao.maps.open.android.KakaoMapSdk
import java.lang.UnsatisfiedLinkError

class MainActivity : FlutterActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        try {
            // 카카오지도 SDK 초기화 (실제 기기에서만)
            KakaoMapSdk.init(this, "fc9248fb37c47471e8ac96d2336946f2")
        } catch (e: UnsatisfiedLinkError) {
            // 에뮬레이터에서 아키텍처 불일치 시 무시
            Log.w("MainActivity", "카카오지도 SDK 초기화 실패 (에뮬레이터): ${e.message}")
        }
    }
}
