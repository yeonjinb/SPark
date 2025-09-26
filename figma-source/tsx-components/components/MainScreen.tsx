import { useState } from 'react';
import { Button } from './ui/button';
import { Card, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { Dialog, DialogContent, DialogTitle, DialogDescription } from './ui/dialog';
import { Mic, MapPin, Bookmark, User, Zap, Navigation, Users } from 'lucide-react';
import { SignupLogin } from './SignupLogin';

interface MainScreenProps {
  onFindOptimalParking: () => void;
  onMyInfo: () => void;
  onMyPage: () => void;
  isLoggedIn: boolean;
  onLogin: () => void;
  locationPermissionGranted: boolean;
}

export function MainScreen({ onFindOptimalParking, onMyInfo, onMyPage, isLoggedIn, onLogin, locationPermissionGranted }: MainScreenProps) {
  const [showLoginModal, setShowLoginModal] = useState(false);

  const handleLogin = () => {
    onLogin();
    setShowLoginModal(false);
  };

  const handleProfileClick = () => {
    if (isLoggedIn) {
      onMyInfo();
    } else {
      setShowLoginModal(true);
    }
  };

  const mockParkingLots = [
    { id: 1, name: '건대입구역 지하주차장', distance: '200m', available: 15, type: 'public', price: '시간당 2,000원' },
    { id: 2, name: '스타시티 주차장', distance: '350m', available: 8, type: 'mall', price: '시간당 1,500원' },
    { id: 3, name: '건국대학교 주차장', distance: '500m', available: 23, type: 'university', price: '시간당 1,000원' }
  ];

  // Bottom Tab Bar Component
  function BottomTabBar() {
    return (
      <div className="absolute bottom-0 left-0 w-full h-[90px] bg-white/95 backdrop-blur-[10px] shadow-[0px_-0.5px_0px_0px_rgba(0,0,0,0.1)]">
        <div className="absolute h-[60px] left-0 top-0 w-full flex items-center justify-around px-6">
          <Button 
            variant="ghost" 
            size="icon"
            className="flex flex-col items-center justify-center h-[60px] w-[80px] gap-1"
          >
            <MapPin className="h-6 w-6 text-blue-600" />
            <span 
              className="text-xs text-blue-600"
              style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontWeight: '500' }}
            >
              탐색
            </span>
          </Button>
          
          <Button 
            variant="ghost" 
            size="icon"
            className="flex flex-col items-center justify-center h-[60px] w-[80px] gap-1"
            onClick={onMyPage}
          >
            <Bookmark className="h-6 w-6 text-gray-500" />
            <span 
              className="text-xs text-gray-700"
              style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontWeight: '500' }}
            >
              내 페이지
            </span>
          </Button>
          
          <Button 
            variant="ghost" 
            size="icon"
            className="flex flex-col items-center justify-center h-[60px] w-[80px] gap-1"
            onClick={handleProfileClick}
          >
            <User className="h-6 w-6 text-gray-500" />
            <span 
              className="text-xs text-gray-700"
              style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontWeight: '500' }}
            >
              {isLoggedIn ? '내 정보' : '로그인'}
            </span>
          </Button>
        </div>
        
        {/* Home Indicator */}
        <div className="absolute bottom-[8px] left-1/2 transform -translate-x-1/2 w-[134px] h-[5px] bg-black rounded-full" />
      </div>
    );
  }

  return (
    <div className="bg-white relative h-screen w-full overflow-hidden">
      {/* SPARK Logo - Left Top */}
      <div className="absolute top-12 left-6 z-10">
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

      {/* Map Area */}
      <div className="w-full h-full bg-gradient-to-br from-blue-50 to-green-50">
        {/* Map Placeholder */}
        <div className="w-full h-full flex items-center justify-center pt-20">
          <div className="text-center text-gray-600">
            <MapPin className="h-16 w-16 mx-auto mb-4 text-blue-600" />
            <p className="text-lg" style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontWeight: '500' }}>
              지도 영역
            </p>
            {locationPermissionGranted ? (
              <p className="text-sm mt-1 text-gray-500">현재 위치: 서울시 광진구 건대입구</p>
            ) : (
              <p className="text-sm mt-1 text-gray-500">위치 권한이 필요합니다</p>
            )}
          </div>
        </div>

        {/* Parking Lot Markers */}
        <div className="absolute top-32 left-8">
          <div className="w-4 h-4 bg-blue-600 rounded-full border-2 border-white shadow-lg animate-pulse"></div>
        </div>
        <div className="absolute top-40 right-12">
          <div className="w-4 h-4 bg-green-600 rounded-full border-2 border-white shadow-lg animate-pulse"></div>
        </div>
        <div className="absolute top-52 left-1/2 transform -translate-x-1/2">
          <div className="w-4 h-4 bg-orange-600 rounded-full border-2 border-white shadow-lg animate-pulse"></div>
        </div>
        <div className="absolute bottom-60 right-8">
          <div className="w-4 h-4 bg-purple-600 rounded-full border-2 border-white shadow-lg animate-pulse"></div>
        </div>

        {/* Current Location Button */}
        <Button
          className="absolute top-20 right-6 bg-white text-gray-600 hover:bg-gray-50 border shadow-lg z-10"
          size="icon"
        >
          <Navigation className="h-4 w-4" />
        </Button>
      </div>

      {/* Nearby Parking Info Card */}
      <div className="absolute bottom-24 left-0 right-0 mx-4 mb-6">
        <Card className="bg-white/95 backdrop-blur-sm shadow-xl border-0">
          <CardContent className="p-4">
            <div className="flex items-center justify-between mb-3">
              <h3 
                className="text-gray-900"
                style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontWeight: '600', fontSize: '16px' }}
              >
                주변 주차장
              </h3>
              <Badge variant="secondary" className="bg-blue-100 text-blue-700">
                {mockParkingLots.length}개 발견
              </Badge>
            </div>
            
            <div className="space-y-2 max-h-32 overflow-y-auto mb-4">
              {mockParkingLots.slice(0, 2).map((lot) => (
                <div key={lot.id} className="cursor-pointer hover:bg-gray-50 p-2 rounded-lg transition-colors">
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <p 
                        className="text-gray-900"
                        style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontWeight: '500', fontSize: '14px' }}
                      >
                        {lot.name}
                      </p>
                      <p 
                        className="text-gray-500"
                        style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontSize: '12px' }}
                      >
                        {lot.distance} · {lot.price} · 여유 {lot.available}대
                      </p>
                    </div>
                    <Badge variant={lot.available > 15 ? "default" : lot.available > 8 ? "secondary" : "destructive"}>
                      {lot.available > 15 ? "여유" : lot.available > 8 ? "보통" : "부족"}
                    </Badge>
                  </div>
                </div>
              ))}
            </div>
            
            {/* Find Optimal Parking Button */}
            <Button
              onClick={onFindOptimalParking}
              className="w-full h-12 rounded-xl bg-blue-600 hover:bg-blue-700 text-white shadow-lg transition-all duration-300 hover:scale-[1.02]"
              style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontWeight: '600', fontSize: '16px' }}
            >
              <Mic className="h-5 w-5 mr-2" />
              최적의 주차장 찾기
            </Button>
          </CardContent>
        </Card>
      </div>

      <BottomTabBar />

      {/* Login Modal */}
      <Dialog open={showLoginModal} onOpenChange={setShowLoginModal}>
        <DialogContent className="w-full max-w-none h-full max-h-none p-0 m-0 border-0 rounded-none sm:max-w-lg sm:max-h-[90vh] sm:h-auto sm:border sm:rounded-lg sm:m-auto">
          <DialogTitle className="sr-only">로그인 및 회원가입</DialogTitle>
          <DialogDescription className="sr-only">
            SPARK 계정으로 로그인하거나 새 계정을 만드세요.
          </DialogDescription>
          <div className="w-full h-full overflow-y-auto">
            <SignupLogin onLogin={handleLogin} />
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}
