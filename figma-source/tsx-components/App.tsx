import { useState } from 'react';
import { SplashScreen } from './components/SplashScreen';
import { LocationPermission } from './components/LocationPermission';
import { SignupLogin } from './components/SignupLogin';
import { MainScreen } from './components/MainScreen';
import { RecommendationResults } from './components/RecommendationResults';
import { ParkingDetails } from './components/ParkingDetails';
import { ErrorScreen } from './components/ErrorScreen';
import { MyProfile } from './components/MyProfile';
import { MyPage } from './components/MyPage';
import { VoiceSearchLoading } from './components/VoiceSearchLoading';
import { Toaster } from './components/ui/sonner';

type AppState = 'splash' | 'location' | 'login' | 'main' | 'voiceLoading' | 'recommendations' | 'details' | 'error' | 'myProfile' | 'myPage';
type ErrorType = 'network' | 'voice' | 'noResults' | 'location';

export default function App() {
  const [currentState, setCurrentState] = useState<AppState>('splash');
  const [selectedParkingId, setSelectedParkingId] = useState<number | null>(null);
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [errorType, setErrorType] = useState<ErrorType>('network');
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [locationPermissionGranted, setLocationPermissionGranted] = useState(false);

  const handleSplashComplete = () => {
    setCurrentState('location');
  };

  const handleLocationAllow = () => {
    setLocationPermissionGranted(true);
    setCurrentState('main');
  };

  const handleLocationDeny = () => {
    setLocationPermissionGranted(false);
    setCurrentState('main');
  };

  const handleLogin = () => {
    setIsLoggedIn(true);
    setCurrentState('main');
  };

  const handleFindOptimalParking = () => {
    // 최적의 주차장 찾기 버튼 클릭 시 음성 검색 로딩으로 이동
    setCurrentState('voiceLoading');
  };

  const handleVoiceSearchComplete = () => {
    // Simulate voice search processing result
    const mockQueries = [
      "2시간 이용 가능한 주차장 찾아줘",
      "건대입구 근처 주차장",
      "3시간 이용 가능한 주차장 찾아줘",
      "1시간 단기 주차 가능한 곳",
      "건대 맛집 근처 주차장"
    ];
    
    const randomQuery = mockQueries[Math.floor(Math.random() * mockQueries.length)];
    setSearchQuery(randomQuery);
    setCurrentState('recommendations');
  };

  const handleVoiceSearchError = () => {
    setErrorType('voice');
    setCurrentState('error');
  };

  const handleSelectParking = (id: number) => {
    setSelectedParkingId(id);
    setCurrentState('details');
  };

  const handleNavigate = () => {
    // In a real app, this would open Kakao Map with navigation
    alert('카카오맵으로 연결됩니다. (실제 환경에서는 카카오맵 앱이 실행됩니다)');
  };

  const handleBackToMain = () => {
    setCurrentState('main');
    setSelectedParkingId(null);
    setSearchQuery('');
  };

  const handleBackToRecommendations = () => {
    setCurrentState('recommendations');
    setSelectedParkingId(null);
  };

  const handleMyInfo = () => {
    setCurrentState('myProfile');
  };

  const handleMyPage = () => {
    setCurrentState('myPage');
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setCurrentState('main');
    setSelectedParkingId(null);
    setSearchQuery('');
  };



  const handleErrorRetry = () => {
    if (errorType === 'voice') {
      setCurrentState('voiceLoading');
    } else {
      setCurrentState('main');
    }
  };

  const handleErrorAlternative = () => {
    setCurrentState('main');
  };

  // Render current screen based on app state
  const renderScreen = () => {
    switch (currentState) {
      case 'splash':
        return <SplashScreen onComplete={handleSplashComplete} />;
    
    case 'location':
      return (
        <LocationPermission 
          onAllow={handleLocationAllow}
          onDeny={handleLocationDeny}
        />
      );
    
    case 'main':
      return (
        <MainScreen 
          onFindOptimalParking={handleFindOptimalParking}
          onMyInfo={handleMyInfo}
          onMyPage={handleMyPage}
          isLoggedIn={isLoggedIn}
          onLogin={handleLogin}
          locationPermissionGranted={locationPermissionGranted}
        />
      );
    
    case 'voiceLoading':
      return (
        <VoiceSearchLoading
          onComplete={handleVoiceSearchComplete}
          onError={handleVoiceSearchError}
        />
      );

    case 'recommendations':
      return (
        <RecommendationResults
          onBack={handleBackToMain}
          onSelectParking={handleSelectParking}
          searchQuery={searchQuery}
        />
      );
    
    case 'details':
      return (
        <ParkingDetails
          onBack={handleBackToRecommendations}
          onNavigate={handleNavigate}
          parkingId={selectedParkingId!}
        />
      );
    
    case 'error':
      return (
        <ErrorScreen
          type={errorType}
          onRetry={handleErrorRetry}
          onAlternative={handleErrorAlternative}
        />
      );
    
    case 'myProfile':
      return (
        <MyProfile
          onBack={handleBackToMain}
          onLogout={handleLogout}
        />
      );
    
      case 'myPage':
        return (
          <MyPage
            onBack={handleBackToMain}
          />
        );
      
      default:
        return <div>Loading...</div>;
    }
  };

  return (
    <>
      {renderScreen()}
      <Toaster />
    </>
  );
}