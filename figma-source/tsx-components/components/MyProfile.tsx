import { useState } from 'react';
import { ArrowLeft, Star, MapPin, Clock, Car, Trash2, Edit3, Plus } from 'lucide-react';
import { Button } from './ui/button';
import { Card } from './ui/card';
import { Textarea } from './ui/textarea';
import { Badge } from './ui/badge';

interface MyPageProps {
  onBack: () => void;
}

interface FavoriteParking {
  id: number;
  name: string;
  address: string;
  distance: string;
  hourlyRate: number;
  maxHeight: number;
  isEVCharging: boolean;
  memo: string;
  addedDate: string;
}

export function MyPage({ onBack }: MyPageProps) {
  const [editingMemo, setEditingMemo] = useState<number | null>(null);
  const [memoText, setMemoText] = useState('');
  const [favorites, setFavorites] = useState<FavoriteParking[]>([
    {
      id: 1,
      name: '강남역 지하주차장',
      address: '서울 강남구 강남대로 396',
      distance: '0.2km',
      hourlyRate: 2000,
      maxHeight: 2.1,
      isEVCharging: true,
      memo: '강남역 바로 연결되어 편리. 전기차 충전소는 B2층에 위치.',
      addedDate: '2024-09-15'
    },
    {
      id: 2,
      name: '테헤란로 노상주차장',
      address: '서울 강남구 테헤란로 152',
      distance: '0.3km',
      hourlyRate: 1800,
      maxHeight: 2.5,
      isEVCharging: false,
      memo: '회사 근처라 자주 이용. 평일 오후엔 만차 주의!',
      addedDate: '2024-09-10'
    },
    {
      id: 3,
      name: '코엑스몰 주차장',
      address: '서울 강남구 영동대로 513',
      distance: '0.8km',
      hourlyRate: 1500,
      maxHeight: 2.3,
      isEVCharging: true,
      memo: '쇼핑할 때 자주 이용. 3시간 이상 주차 시 할인 혜택 있음.',
      addedDate: '2024-09-01'
    }
  ]);

  const handleEditMemo = (parkingId: number, currentMemo: string) => {
    setEditingMemo(parkingId);
    setMemoText(currentMemo);
  };

  const handleSaveMemo = (parkingId: number) => {
    setFavorites(prev => prev.map(parking => 
      parking.id === parkingId 
        ? { ...parking, memo: memoText }
        : parking
    ));
    setEditingMemo(null);
    setMemoText('');
  };

  const handleCancelEdit = () => {
    setEditingMemo(null);
    setMemoText('');
  };

  const handleRemoveFavorite = (parkingId: number) => {
    setFavorites(prev => prev.filter(parking => parking.id !== parkingId));
  };

  return (
    <div className="bg-white min-h-screen">
      {/* Header */}
      <div className="sticky top-0 bg-white z-10 px-6 py-4 border-b border-gray-100">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <Button
              variant="ghost"
              size="icon"
              onClick={onBack}
              className="h-10 w-10"
            >
              <ArrowLeft className="h-5 w-5" />
            </Button>
            <div>
              <h1 
                className="text-xl text-gray-900"
                style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontWeight: '600' }}
              >
                내 페이지
              </h1>
              <p 
                className="text-sm text-gray-500"
                style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontWeight: '400' }}
              >
                즐겨찾는 주차장과 메모를 관리하세요
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="px-6 py-6">
        {/* Statistics */}
        <div className="grid grid-cols-2 gap-4 mb-6">
          <div className="bg-blue-50 rounded-lg p-4 text-center">
            <div 
              className="text-2xl text-blue-600 mb-1"
              style={{ fontFamily: 'Inter, sans-serif', fontWeight: '700' }}
            >
              {favorites.length}
            </div>
            <div 
              className="text-sm text-blue-700"
              style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontWeight: '500' }}
            >
              즐겨찾기 주차장
            </div>
          </div>
          <div className="bg-green-50 rounded-lg p-4 text-center">
            <div 
              className="text-2xl text-green-600 mb-1"
              style={{ fontFamily: 'Inter, sans-serif', fontWeight: '700' }}
            >
              {favorites.filter(p => p.isEVCharging).length}
            </div>
            <div 
              className="text-sm text-green-700"
              style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontWeight: '500' }}
            >
              전기차 충전 가능
            </div>
          </div>
        </div>

        {/* Favorites List */}
        <div className="space-y-4">
          {favorites.length === 0 ? (
            <div className="text-center py-12">
              <Star className="w-12 h-12 text-gray-300 mx-auto mb-4" />
              <p 
                className="text-gray-500 mb-2"
                style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontWeight: '500' }}
              >
                즐겨찾는 주차장이 없습니다
              </p>
              <p 
                className="text-sm text-gray-400"
                style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontWeight: '400' }}
              >
                주차장 상세 정보에서 즐겨찾기를 추가해보세요
              </p>
            </div>
          ) : (
            favorites.map((parking) => (
              <Card key={parking.id} className="p-4">
                <div className="flex justify-between items-start mb-3">
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-1">
                      <h3 
                        className="text-base text-gray-900"
                        style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontWeight: '600' }}
                      >
                        {parking.name}
                      </h3>
                      <Star className="w-4 h-4 text-yellow-500 fill-current" />
                    </div>
                    <div className="flex items-center text-sm text-gray-600 mb-2">
                      <MapPin className="w-4 h-4 mr-1" />
                      <span style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontWeight: '400' }}>
                        {parking.address}
                      </span>
                    </div>
                  </div>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => handleRemoveFavorite(parking.id)}
                    className="h-8 w-8 text-red-500 hover:text-red-700 hover:bg-red-50"
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>

                {/* Parking Info */}
                <div className="flex flex-wrap gap-2 mb-3">
                  <Badge variant="outline" className="text-xs">
                    <Clock className="w-3 h-3 mr-1" />
                    시간당 {parking.hourlyRate.toLocaleString()}원
                  </Badge>
                  <Badge variant="outline" className="text-xs">
                    <Car className="w-3 h-3 mr-1" />
                    높이 {parking.maxHeight}m
                  </Badge>
                  {parking.isEVCharging && (
                    <Badge variant="secondary" className="text-xs bg-green-100 text-green-700">
                      전기차 충전
                    </Badge>
                  )}
                  <Badge variant="outline" className="text-xs">
                    {parking.distance}
                  </Badge>
                </div>

                {/* Memo Section */}
                <div className="border-t pt-3">
                  <div className="flex items-center justify-between mb-2">
                    <span 
                      className="text-sm text-gray-700"
                      style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontWeight: '500' }}
                    >
                      메모
                    </span>
                    {editingMemo !== parking.id && (
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={() => handleEditMemo(parking.id, parking.memo)}
                        className="h-6 w-6"
                      >
                        <Edit3 className="h-3 w-3" />
                      </Button>
                    )}
                  </div>

                  {editingMemo === parking.id ? (
                    <div className="space-y-2">
                      <Textarea
                        value={memoText}
                        onChange={(e) => setMemoText(e.target.value)}
                        placeholder="주차장에 대한 메모를 입력하세요..."
                        className="min-h-[80px] text-sm"
                        style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontWeight: '400' }}
                      />
                      <div className="flex space-x-2">
                        <Button
                          size="sm"
                          onClick={() => handleSaveMemo(parking.id)}
                          className="bg-blue-600 hover:bg-blue-700"
                        >
                          저장
                        </Button>
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={handleCancelEdit}
                        >
                          취소
                        </Button>
                      </div>
                    </div>
                  ) : (
                    <p 
                      className="text-sm text-gray-600 bg-gray-50 rounded-lg p-3"
                      style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontWeight: '400' }}
                    >
                      {parking.memo || '메모가 없습니다. 편집 버튼을 눌러 메모를 추가해보세요.'}
                    </p>
                  )}
                </div>

                {/* Added Date */}
                <div className="text-xs text-gray-400 mt-3 text-right">
                  <span style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontWeight: '400' }}>
                    추가일: {parking.addedDate}
                  </span>
                </div>
              </Card>
            ))
          )}
        </div>

        {/* Add Favorites Tip */}
        {favorites.length > 0 && (
          <div className="mt-8 bg-blue-50 rounded-lg p-4">
            <div className="flex items-start space-x-3">
              <Plus className="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
              <div>
                <p 
                  className="text-sm text-blue-800 mb-1"
                  style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontWeight: '500' }}
                >
                  💡 즐겨찾기 추가 방법
                </p>
                <p 
                  className="text-xs text-blue-700"
                  style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontWeight: '400' }}
                >
                  주차장 검색 후 상세 정보에서 별표(★) 버튼을 눌러 즐겨찾기에 추가할 수 있습니다.
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}