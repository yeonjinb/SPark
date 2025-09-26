import { useEffect } from 'react';
import { Zap } from 'lucide-react';

interface SplashScreenProps {
  onComplete: () => void;
}

export function SplashScreen({ onComplete }: SplashScreenProps) {
  useEffect(() => {
    const timer = setTimeout(() => {
      onComplete();
    }, 2000); // 2초 후 다음 화면으로

    return () => clearTimeout(timer);
  }, [onComplete]);

  return (
    <div className="bg-white h-screen w-full flex items-center justify-center">
      <div className="flex flex-col items-center space-y-6">
        {/* SPARK Logo */}
        <div className="flex items-center space-x-4">
          <div className="w-20 h-20 bg-blue-600 rounded-full flex items-center justify-center shadow-xl animate-pulse">
            <Zap className="w-10 h-10 text-white" />
          </div>
          <span 
            className="text-blue-900"
            style={{ 
              fontFamily: 'Inter, sans-serif', 
              fontWeight: '700',
              fontStyle: 'italic',
              transform: 'skewX(-12deg)',
              fontSize: '36px'
            }}
          >
            SPARK
          </span>
        </div>
        
        {/* Loading Animation */}
        <div className="flex space-x-2 mt-8">
          <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
          <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
          <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
        </div>
        
        {/* Subtitle */}
        <p 
          className="text-gray-600 text-center mt-4"
          style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontWeight: '500', fontSize: '16px' }}
        >
          스마트 주차장 검색 시스템
        </p>
      </div>
    </div>
  );
}
