import { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Checkbox } from './ui/checkbox';
import { RadioGroup, RadioGroupItem } from './ui/radio-group';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Zap } from 'lucide-react';

interface SignupLoginProps {
  onLogin: () => void;
}

export function SignupLogin({ onLogin }: SignupLoginProps) {
  const [isSignup, setIsSignup] = useState(false);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    name: '',
    age: '',
    drivingExperience: '',
    licensePlate: '',
    carType: 'medium',
    preference: 'cost',
    discountTypes: [] as string[]
  });

  return (
    <div className="bg-white relative h-screen w-full overflow-auto">
      {/* Header */}
      <div className="sticky top-0 bg-white z-10 border-b border-gray-100">
        <div className="flex items-center justify-center p-6">
          <div className="flex items-center space-x-3">
            <div className="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center shadow-lg">
              <Zap className="w-6 h-6 text-white" />
            </div>
            <h1 
              className="text-blue-900"
              style={{ 
                fontFamily: 'Inter, sans-serif', 
                fontWeight: '700',
                fontStyle: 'italic',
                transform: 'skewX(-12deg)',
                fontSize: '24px'
              }}
            >
              SPARK
            </h1>
          </div>
        </div>
        <div className="text-center pb-4">
          <p 
            className="text-gray-600"
            style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontWeight: '500', fontSize: '16px' }}
          >
            Smart Parking System
          </p>
        </div>
      </div>

      {/* Content */}
      <div className="px-6 py-6">
        <Tabs value={isSignup ? "signup" : "login"} onValueChange={(value) => setIsSignup(value === "signup")}>
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="login">로그인</TabsTrigger>
            <TabsTrigger value="signup">회원가입</TabsTrigger>
          </TabsList>
          
          <TabsContent value="login" className="space-y-4 mt-4">
            <form className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="email">이메일</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="이메일을 입력하세요"
                  value={formData.email}
                  onChange={(e) => setFormData({...formData, email: e.target.value})}
                  required
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="password">비밀번호</Label>
                <Input
                  id="password"
                  type="password"
                  placeholder="비밀번호를 입력하세요"
                  value={formData.password}
                  onChange={(e) => setFormData({...formData, password: e.target.value})}
                  required
                />
              </div>
              
              <Button 
                type="submit" 
                className="w-full bg-blue-600 hover:bg-blue-700 text-white"
                onClick={(e) => {
                  e.preventDefault();
                  if (formData.email && formData.password) {
                    onLogin();
                  }
                }}
              >
                로그인
              </Button>
            </form>
          </TabsContent>
          
          <TabsContent value="signup" className="space-y-4 mt-4">
            <form className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="signup-email" style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontWeight: '600', fontSize: '14px' }}>이메일</Label>
                <Input
                  id="signup-email"
                  type="email"
                  placeholder="이메일을 입력하세요"
                  value={formData.email}
                  onChange={(e) => setFormData({...formData, email: e.target.value})}
                  required
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="signup-password" style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontWeight: '600', fontSize: '14px' }}>비밀번호</Label>
                <Input
                  id="signup-password"
                  type="password"
                  placeholder="비밀번호를 입력하세요"
                  value={formData.password}
                  onChange={(e) => setFormData({...formData, password: e.target.value})}
                  required
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="name" style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontWeight: '600', fontSize: '14px' }}>이름</Label>
                <Input
                  id="name"
                  placeholder="이름을 입력하세요"
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  required
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="age" style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontWeight: '600', fontSize: '14px' }}>나이</Label>
                <Input
                  id="age"
                  type="number"
                  placeholder="나이를 입력하세요"
                  value={formData.age}
                  onChange={(e) => setFormData({...formData, age: e.target.value})}
                  required
                />
              </div>
              
              <div className="space-y-2">
                <Label style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontWeight: '600', fontSize: '14px' }}>운전 경력</Label>
                <Select value={formData.drivingExperience} onValueChange={(value) => setFormData({...formData, drivingExperience: value})}>
                  <SelectTrigger>
                    <SelectValue placeholder="운전 경력을 선택하세요" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="1년 미만">1년 미만</SelectItem>
                    <SelectItem value="1-3년">1-3년</SelectItem>
                    <SelectItem value="3-5년">3-5년</SelectItem>
                    <SelectItem value="5년 이상">5년 이상</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="licensePlate" style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontWeight: '600', fontSize: '14px' }}>차량 번호판 (선택사항)</Label>
                <Input
                  id="licensePlate"
                  placeholder="예: 12가 3456"
                  value={formData.licensePlate}
                  onChange={(e) => setFormData({...formData, licensePlate: e.target.value})}
                />
              </div>

              <div className="space-y-2">
                <Label style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontWeight: '600', fontSize: '14px' }}>차량 종류</Label>
                <Select value={formData.carType} onValueChange={(value) => setFormData({...formData, carType: value})}>
                  <SelectTrigger>
                    <SelectValue placeholder="차량 종류를 선택하세요" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="compact">경차</SelectItem>
                    <SelectItem value="small">소형차</SelectItem>
                    <SelectItem value="medium">중형차</SelectItem>
                    <SelectItem value="large">대형차</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              
              <div className="space-y-3">
                <Label style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontWeight: '600', fontSize: '14px' }}>선호 옵션</Label>
                <RadioGroup 
                  value={formData.preference} 
                  onValueChange={(value) => setFormData({...formData, preference: value})}
                  className="space-y-2"
                >
                  <div className="flex items-center space-x-2">
                    <RadioGroupItem value="cost" id="cost" />
                    <Label htmlFor="cost">주차 비용 최소</Label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <RadioGroupItem value="time" id="time" />
                    <Label htmlFor="time">이동 시간 최소</Label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <RadioGroupItem value="difficulty" id="difficulty" />
                    <Label htmlFor="difficulty">운전 난이도 최소</Label>
                  </div>
                </RadioGroup>
              </div>
              
              <div className="space-y-3">
                <Label style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontWeight: '600', fontSize: '14px' }}>할인 유형 (선택사항)</Label>
                <div className="grid grid-cols-1 gap-2 max-h-32 overflow-y-auto border rounded-lg p-3">
                  {[
                    '국가유공자/장애인',
                    '저공해차/경차',
                    '다둥이/한부모가족',
                    '기타 할인 대상'
                  ].map((type) => (
                    <div key={type} className="flex items-center space-x-3">
                      <Checkbox 
                        id={`discount-${type}`}
                        checked={formData.discountTypes.includes(type)}
                        onCheckedChange={(checked) => {
                          if (checked) {
                            setFormData({
                              ...formData, 
                              discountTypes: [...formData.discountTypes, type]
                            });
                          } else {
                            setFormData({
                              ...formData,
                              discountTypes: formData.discountTypes.filter(t => t !== type)
                            });
                          }
                        }}
                      />
                      <Label 
                        htmlFor={`discount-${type}`} 
                        className="cursor-pointer"
                        style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontSize: '13px' }}
                      >
                        {type}
                      </Label>
                    </div>
                  ))}
                </div>
              </div>
              
              <div className="flex items-center space-x-2">
                <Checkbox id="location-agree" />
                <Label htmlFor="location-agree" className="text-sm">위치 정보 제공에 동의합니다</Label>
              </div>
              
              <Button 
                type="submit" 
                className="w-full bg-blue-600 hover:bg-blue-700 text-white"
                onClick={(e) => {
                  e.preventDefault();
                  if (formData.email && formData.password && formData.name && formData.age) {
                    onLogin();
                  }
                }}
              >
                회원가입
              </Button>
            </form>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}