import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { AlertTriangle, Mic, Search, RefreshCw, Wifi } from 'lucide-react';

interface ErrorScreenProps {
  type: 'network' | 'voice' | 'noResults' | 'location';
  onRetry: () => void;
  onAlternative: () => void;
}

export function ErrorScreen({ type, onRetry, onAlternative }: ErrorScreenProps) {
  const errorConfig = {
    network: {
      icon: <Wifi className="h-16 w-16 text-red-500" />,
      title: '네트워크 연결 오류',
      message: '인터넷 연결을 확인하고 다시 시도해주세요.',
      retryText: '다시 시도',
      alternativeText: '오프라인 모드'
    },
    voice: {
      icon: <Mic className="h-16 w-16 text-orange-500" />,
      title: '음성 인식 실패',
      message: '음성을 인식할 수 없습니다. 다시 말해주세요.',
      retryText: '다시 말하기',
      alternativeText: '텍스트로 검색'
    },
    noResults: {
      icon: <Search className="h-16 w-16 text-blue-500" />,
      title: '검색 결과가 없습니다',
      message: '해당 지역에서 조건에 맞는 주차장을 찾을 수 없습니다.',
      retryText: '다른 조건으로 검색',
      alternativeText: '전체 주차장 보기'
    },
    location: {
      icon: <AlertTriangle className="h-16 w-16 text-yellow-500" />,
      title: '위치 권한 필요',
      message: '주변 주차장을 찾기 위해 위치 권한이 필요합니다.',
      retryText: '권한 허용',
      alternativeText: '수동으로 위치 입력'
    }
  };

  const config = errorConfig[type];

  return (
    <div className="h-screen bg-gray-50 flex items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center pb-2">
          <div className="flex justify-center mb-4">
            {config.icon}
          </div>
          <CardTitle className="text-xl text-gray-900">{config.title}</CardTitle>
        </CardHeader>
        
        <CardContent className="text-center space-y-6">
          <p className="text-gray-600">{config.message}</p>
          
          <div className="space-y-3">
            <Button 
              onClick={onRetry}
              className="w-full bg-blue-600 hover:bg-blue-700"
            >
              <RefreshCw className="h-4 w-4 mr-2" />
              {config.retryText}
            </Button>
            
            <Button 
              onClick={onAlternative}
              variant="outline"
              className="w-full"
            >
              {config.alternativeText}
            </Button>
          </div>
          
          {type === 'voice' && (
            <div className="text-xs text-gray-500 mt-4">
              <p>음성 인식 팁:</p>
              <ul className="mt-1 space-y-1 text-left">
                <li>• 조용한 곳에서 말해주세요</li>
                <li>• "2시간 주차장 찾아줘"처럼 명확하게</li>
                <li>• 마이크 권한을 확인해주세요</li>
              </ul>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}