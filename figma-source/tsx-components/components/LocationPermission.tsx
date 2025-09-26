import { Button } from './ui/button';
import { Card, CardContent } from './ui/card';
import { MapPin, Shield, Zap } from 'lucide-react';

interface LocationPermissionProps {
  onAllow: () => void;
  onDeny: () => void;
}

export function LocationPermission({ onAllow, onDeny }: LocationPermissionProps) {
  return (
    <div className="bg-white h-screen w-full flex flex-col">
      {/* Header with Logo */}
      <div className="flex items-center justify-center pt-16 pb-8">
        <div className="flex items-center space-x-3">
          <div className="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center shadow-lg">
            <Zap className="w-6 h-6 text-white" />
          </div>
          <span 
            className="text-blue-900"
            style={{ 
              fontFamily: 'Inter, sans-serif', 
              fontWeight: '700',
              fontStyle: 'italic',
              transform: 'skewX(-12deg)',
              fontSize: '22px'
            }}
          >
            SPARK
          </span>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 px-6 flex flex-col justify-center">
        <div className="text-center mb-8">
          {/* Location Icon */}
          <div className="w-24 h-24 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-6">
            <MapPin className="w-12 h-12 text-blue-600" />
          </div>
          
          {/* Title */}
          <h1 
            className="text-gray-900 mb-4"
            style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontWeight: '600', fontSize: '24px', lineHeight: '1.3' }}
          >
            위치 정보 접근 권한
          </h1>
          
          {/* Description */}
          <p 
            className="text-gray-600 mb-8 leading-relaxed px-4"
            style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontWeight: '400', fontSize: '16px', lineHeight: '1.6' }}
          >
            주변 주차장을 찾고 최적의 경로를 
            제공하기 위해 위치 정보가 필요합니다.
          </p>
        </div>

        {/* Permission Benefits */}
        <Card className="mb-8 border border-blue-100">
          <CardContent className="p-6">
            <div className="space-y-4">
              <div className="flex items-start space-x-3">
                <div className="w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                  <MapPin className="w-3 h-3 text-blue-600" />
                </div>
                <div>
                  <p 
                    className="text-gray-900"
                    style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontWeight: '500', fontSize: '14px' }}
                  >
                    주변 주차장 실시간 검색
                  </p>
                  <p 
                    className="text-gray-500"
                    style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontWeight: '400', fontSize: '12px' }}
                  >
                    현재 위치를 기반으로 가까운 주차장을 찾아드립니다
                  </p>
                </div>
              </div>
              
              <div className="flex items-start space-x-3">
                <div className="w-6 h-6 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                  <Shield className="w-3 h-3 text-green-600" />
                </div>
                <div>
                  <p 
                    className="text-gray-900"
                    style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontWeight: '500', fontSize: '14px' }}
                  >
                    개인정보 보호
                  </p>
                  <p 
                    className="text-gray-500"
                    style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontWeight: '400', fontSize: '12px' }}
                  >
                    위치 정보는 서비스 제공 목적으로만 사용됩니다
                  </p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Action Buttons */}
      <div className="px-6 pb-8 space-y-3">
        <Button
          onClick={onAllow}
          className="w-full h-14 rounded-xl bg-blue-600 hover:bg-blue-700 text-white shadow-lg transition-all duration-300"
          style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontWeight: '600', fontSize: '16px' }}
        >
          위치 정보 제공 동의
        </Button>
        
        <Button
          onClick={onDeny}
          variant="ghost"
          className="w-full h-12 text-gray-600 hover:bg-gray-50"
          style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontWeight: '500', fontSize: '14px' }}
        >
          나중에 설정하기
        </Button>
      </div>

      {/* Home Indicator */}
      <div className="absolute bottom-2 left-1/2 transform -translate-x-1/2 w-[134px] h-[5px] bg-black rounded-full" />
    </div>
  );
}
