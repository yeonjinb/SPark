import { useState, useMemo } from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { ArrowLeft, MapPin, DollarSign, Star, Zap } from 'lucide-react';

interface RecommendationResultsProps {
  onBack: () => void;
  onSelectParking: (id: number) => void;
  searchQuery: string;
}

export function RecommendationResults({ onBack, onSelectParking, searchQuery }: RecommendationResultsProps) {
  const [selectedIndex, setSelectedIndex] = useState(0);

  const recommendations = useMemo(() => [
    {
      id: 1,
      name: '건대입구역 지하주차장',
      address: '서울시 광진구 능동로 209',
      distance: '네비 기준 2분 (150m)',
      price: '2시간 3,200원',
      type: 'optimal',
      badge: '최적',
      badgeColor: 'bg-blue-500',
      rating: 4.3,
      features: ['24시간', '실내주차', '카드결제'],
      available: 12
    },
    {
      id: 2,
      name: '건대 로데오거리 노상주차장',
      address: '서울시 광진구 아차산로29길 18',
      distance: '네비 기준 1분 (80m)',
      price: '2시간 2,400원',
      type: 'nearest',
      badge: '최단거리',
      badgeColor: 'bg-green-500',
      rating: 4.0,
      features: ['노상주차', '단기주차', '맛집근처'],
      available: 5
    },
    {
      id: 3,
      name: '건국대학교 주변 공영주차장',
      address: '서울시 광진구 능동로 120',
      distance: '네비 기준 4분 (300m)',
      price: '2시간 2,000원',
      type: 'cheapest',
      badge: '최저가격',
      badgeColor: 'bg-orange-600',
      rating: 4.1,
      features: ['공영주차', '저렴', '넓음'],
      available: 18
    }
  ], []);



  const handleSelect = (id: number, index: number) => {
    setSelectedIndex(index);
    setTimeout(() => onSelectParking(id), 300);
  };

  return (
    <div className="h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <div className="bg-white shadow-sm p-4 flex items-center">
        <Button variant="ghost" size="icon" onClick={onBack} className="mr-3">
          <ArrowLeft className="h-5 w-5" />
        </Button>
        <div>
          <h1 className="font-semibold text-gray-900">추천 주차장</h1>
          <p className="text-sm text-gray-500">"{searchQuery}" 검색 결과</p>
        </div>
      </div>

      {/* Map Preview */}
      <div className="h-48 bg-gradient-to-br from-blue-100 to-gray-100 relative border-b">
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="text-center text-gray-600">
            <MapPin className="h-12 w-12 mx-auto mb-2 text-blue-600" />
            <p className="text-sm">지도에서 위치 확인</p>
          </div>
        </div>
        
        {/* Map markers */}
        <div className="absolute top-16 left-8">
          <div className="w-4 h-4 bg-blue-500 rounded-full border-2 border-white shadow-lg"></div>
        </div>
        <div className="absolute top-20 right-12">
          <div className="w-4 h-4 bg-blue-400 rounded-full border-2 border-white shadow-lg"></div>
        </div>
        <div className="absolute bottom-16 left-12">
          <div className="w-4 h-4 bg-blue-600 rounded-full border-2 border-white shadow-lg"></div>
        </div>
      </div>

      {/* Recommendations List */}
      <div className="flex-1 p-4 space-y-4 overflow-y-auto">
        {recommendations.map((parking, index) => (
          <Card 
            key={parking.id} 
            className={`cursor-pointer transition-all duration-300 ${
              selectedIndex === index ? 'scale-105 shadow-lg border-blue-500' : 'hover:shadow-md'
            }`}
            onClick={() => handleSelect(parking.id, index)}
          >
            <CardHeader className="pb-3">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <CardTitle className="text-lg">{parking.name}</CardTitle>
                    <Badge className={`${parking.badgeColor} text-white text-xs`}>
                      {parking.badge}
                    </Badge>
                  </div>
                  <p className="text-sm text-gray-600">{parking.address}</p>
                </div>
                <div className="flex items-center gap-1 text-sm text-gray-500">
                  <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                  {parking.rating}
                </div>
              </div>
            </CardHeader>
            
            <CardContent className="pt-0">
              <div className="grid grid-cols-2 gap-4 mb-3">
                <div className="flex items-center gap-2 text-sm">
                  <MapPin className="h-4 w-4 text-blue-600" />
                  <span>{parking.distance}</span>
                </div>
                <div className="flex items-center gap-2 text-sm">
                  <DollarSign className="h-4 w-4 text-blue-600" />
                  <span>{parking.price}</span>
                </div>
              </div>
              
              <div className="flex items-center justify-between">
                <div className="flex flex-wrap gap-1">
                  {parking.features.map((feature, idx) => (
                    <Badge key={idx} variant="secondary" className="text-xs">
                      {feature === '전기차충전' && <Zap className="h-3 w-3 mr-1" />}
                      {feature}
                    </Badge>
                  ))}
                </div>
                <div className="text-sm">
                  <Badge variant={parking.available > 10 ? "default" : parking.available > 5 ? "secondary" : "destructive"}>
                    여유 {parking.available}대
                  </Badge>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>


    </div>
  );
}