import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Separator } from './ui/separator';
import { ArrowLeft, MapPin, Clock, DollarSign, Star, Navigation, Phone, Zap, Car, Shield, Wifi } from 'lucide-react';

interface ParkingDetailsProps {
  onBack: () => void;
  onNavigate: () => void;
  parkingId: number;
}

export function ParkingDetails({ onBack, onNavigate, parkingId }: ParkingDetailsProps) {
  // Mock data - in real app this would be fetched based on parkingId
  const parkingDetails = {
    id: parkingId,
    name: '건대입구역 지하주차장',
    address: '서울시 광진구 능동로 209',
    fullAddress: '서울특별시 광진구 능동로 209 지하 1층',
    distance: '네비 기준 2분 (150m)',
    rating: 4.3,
    reviewCount: 89,
    operatingHours: '24시간 운영',
    pricing: {
      basic: '30분당 800원',
      hourly: '1시간 1,600원',
      daily: '일일 최대 12,000원',
      twoHour: '2시간 3,200원'
    },
    features: [
      { icon: <Car className="h-4 w-4" />, name: '높이 제한', value: '2.0m' },
      { icon: <Shield className="h-4 w-4" />, name: 'CCTV 보안', available: true },
      { icon: <Wifi className="h-4 w-4" />, name: '카드 결제', available: true },
      { icon: <MapPin className="h-4 w-4" />, name: '맛집 근처', available: true }
    ],
    availability: {
      total: 80,
      available: 12,
      lastUpdated: '2분전'
    },
    contact: '02-3456-7890',
    images: [
      'https://images.unsplash.com/photo-1627834376385-2288c6732535?w=400',
      'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400'
    ]
  };

  return (
    <div className="h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <div className="bg-white shadow-sm p-4 flex items-center justify-between">
        <div className="flex items-center">
          <Button variant="ghost" size="icon" onClick={onBack} className="mr-3">
            <ArrowLeft className="h-5 w-5" />
          </Button>
          <div>
            <h1 className="font-semibold text-gray-900">상세 정보</h1>
            <div className="flex items-center gap-2 mt-1">
              <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
              <span className="text-sm text-gray-600">
                {parkingDetails.rating} ({parkingDetails.reviewCount}개 리뷰)
              </span>
            </div>
          </div>
        </div>
        
        <Button variant="ghost" size="icon">
          <Phone className="h-5 w-5" />
        </Button>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto">
        {/* Hero Image */}
        <div className="h-48 bg-gradient-to-br from-blue-100 to-gray-100 relative">
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="text-center text-gray-600">
              <MapPin className="h-16 w-16 mx-auto mb-2 text-blue-600" />
              <p>주차장 이미지</p>
            </div>
          </div>
          
          {/* Availability Badge */}
          <div className="absolute top-4 left-4">
            <Badge className="bg-green-600 text-white">
              여유 {parkingDetails.availability.available}대
            </Badge>
          </div>
        </div>

        <div className="p-4 space-y-6">
          {/* Basic Info */}
          <Card>
            <CardHeader>
              <CardTitle className="text-xl">{parkingDetails.name}</CardTitle>
              <p className="text-gray-600">{parkingDetails.fullAddress}</p>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-2 text-sm">
                  <MapPin className="h-4 w-4 text-blue-600" />
                  <span>{parkingDetails.distance}</span>
                </div>
                <div className="flex items-center gap-2 text-sm">
                  <Clock className="h-4 w-4 text-blue-600" />
                  <span>{parkingDetails.operatingHours}</span>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Pricing */}
          <Card>
            <CardHeader>
              <CardTitle>주차 요금</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="grid grid-cols-2 gap-4">
                <div className="text-sm">
                  <span className="text-gray-600">기본 요금</span>
                  <div className="font-semibold">{parkingDetails.pricing.basic}</div>
                </div>
                <div className="text-sm">
                  <span className="text-gray-600">시간 요금</span>
                  <div className="font-semibold">{parkingDetails.pricing.hourly}</div>
                </div>
              </div>
              <Separator />
              <div className="bg-blue-50 p-3 rounded-lg">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-blue-700">예상 주차 요금 (2시간)</span>
                  <span className="font-bold text-blue-900">{parkingDetails.pricing.twoHour}</span>
                </div>
              </div>
              <div className="text-xs text-gray-500">
                일일 최대: {parkingDetails.pricing.daily}
              </div>
            </CardContent>
          </Card>

          {/* Features */}
          <Card>
            <CardHeader>
              <CardTitle>주차장 정보</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 gap-4">
                {parkingDetails.features.map((feature, index) => (
                  <div key={index} className="flex items-center gap-2 text-sm">
                    <div className="text-blue-600">{feature.icon}</div>
                    <span className="flex-1">{feature.name}</span>
                    {feature.available && (
                      <Badge variant="secondary" className="text-xs">가능</Badge>
                    )}
                    {feature.value && (
                      <span className="text-gray-600 text-xs">{feature.value}</span>
                    )}
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Real-time Availability */}
          <Card>
            <CardHeader>
              <CardTitle>실시간 주차 현황</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">전체 주차 공간</span>
                  <span className="font-semibold">{parkingDetails.availability.total}대</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">주차 가능</span>
                  <span className="font-semibold text-blue-600">
                    {parkingDetails.availability.available}대
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-blue-600 h-2 rounded-full"
                    style={{ 
                      width: `${(parkingDetails.availability.available / parkingDetails.availability.total) * 100}%` 
                    }}
                  ></div>
                </div>
                <div className="text-xs text-gray-500 text-right">
                  최종 업데이트: {parkingDetails.availability.lastUpdated}
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Navigation Button */}
      <div className="bg-white p-4 border-t">
        <Button 
          onClick={onNavigate}
          className="w-full h-14 bg-blue-600 hover:bg-blue-700 text-white font-semibold text-lg"
        >
          <Navigation className="h-6 w-6 mr-2" />
          카카오맵으로 길안내
        </Button>
      </div>
    </div>
  );
}
