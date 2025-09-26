import { useState } from 'react';
import { Button } from './ui/button';
import { Card, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { Mic, Settings, MapPin, Navigation } from 'lucide-react';

interface MainMapProps {
  onVoiceSearch: () => void;
  onSettings: () => void;
}

export function MainMap({ onVoiceSearch, onSettings }: MainMapProps) {
  const [isListening, setIsListening] = useState(false);

  const handleVoiceSearch = () => {
    setIsListening(true);
    setTimeout(() => {
      setIsListening(false);
      onVoiceSearch();
    }, 2000);
  };

  const mockParkingLots = [
    { id: 1, name: '강남역 지하주차장', distance: '200m', available: 15, type: 'public' },
    { id: 2, name: '코엑스몰 주차장', distance: '500m', available: 8, type: 'mall' },
    { id: 3, name: '테헤란로 빌딩 주차장', distance: '300m', available: 3, type: 'building' }
  ];

  return (
    <div className="h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <div className="bg-white shadow-sm p-4 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
            <span className="text-white text-sm font-bold">S</span>
          </div>
          <span className="font-semibold text-gray-900" style={{ fontFamily: 'Inter, sans-serif' }}>SPARK</span>
        </div>
        
        <Button 
          variant="ghost" 
          size="icon"
          onClick={onSettings}
          className="text-gray-600"
        >
          <Settings className="h-5 w-5" />
        </Button>
      </div>



      {/* Map Area */}
      <div className="flex-1 relative bg-gradient-to-br from-blue-100 to-green-100">
        {/* Map Placeholder */}
        <div className="w-full h-full flex items-center justify-center">
          <div className="text-center text-gray-600">
            <MapPin className="h-16 w-16 mx-auto mb-4 text-blue-600" />
            <p>지도 영역</p>
            <p className="text-sm mt-1">현재 위치: 서울시 강남구</p>
          </div>
        </div>

        {/* Parking Lot Markers */}
        <div className="absolute top-20 left-4">
          <div className="w-3 h-3 bg-blue-600 rounded-full border-2 border-white shadow-lg"></div>
        </div>
        <div className="absolute top-32 right-6">
          <div className="w-3 h-3 bg-green-600 rounded-full border-2 border-white shadow-lg"></div>
        </div>
        <div className="absolute bottom-32 left-6">
          <div className="w-3 h-3 bg-orange-600 rounded-full border-2 border-white shadow-lg"></div>
        </div>

        {/* Current Location Button */}
        <Button
          className="absolute top-4 right-4 bg-white text-gray-600 hover:bg-gray-50 border shadow-md"
          size="icon"
        >
          <Navigation className="h-4 w-4" />
        </Button>
      </div>

      {/* Nearby Parking Info */}
      <div className="bg-white p-4 border-t">
        <div className="flex items-center justify-between mb-3">
          <h3 className="font-semibold text-gray-900">주변 주차장</h3>
          <Badge variant="secondary" className="bg-blue-100 text-blue-700">
            {mockParkingLots.length}개 발견
          </Badge>
        </div>
        
        <div className="space-y-2">
          {mockParkingLots.slice(0, 2).map((lot) => (
            <Card key={lot.id} className="cursor-pointer hover:shadow-md transition-shadow">
              <CardContent className="p-3">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium text-sm">{lot.name}</p>
                    <p className="text-xs text-gray-500">{lot.distance} · 여유 {lot.available}대</p>
                  </div>
                  <Badge variant={lot.available > 10 ? "default" : lot.available > 5 ? "secondary" : "destructive"}>
                    {lot.available > 10 ? "여유" : lot.available > 5 ? "보통" : "부족"}
                  </Badge>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Voice Search Button */}
      <div className="bg-white p-6 border-t">
        <Button
          onClick={handleVoiceSearch}
          className={`w-full h-14 rounded-full text-white font-semibold text-lg shadow-lg transition-all ${
            isListening 
              ? 'bg-red-500 hover:bg-red-600 animate-pulse' 
              : 'bg-blue-600 hover:bg-blue-700'
          }`}
        >
          <Mic className="h-6 w-6 mr-2" />
          {isListening ? '듣고 있어요...' : '음성으로 주차장 검색'}
        </Button>
      </div>
    </div>
  );
}