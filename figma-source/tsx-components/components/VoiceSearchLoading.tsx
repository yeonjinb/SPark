import { useEffect, useState } from 'react';
import { Mic, Volume2, MapPin, Clock, Car, Zap } from 'lucide-react';
import { motion } from 'motion/react';

interface VoiceSearchLoadingProps {
  onComplete: () => void;
  onError: () => void;
}

export function VoiceSearchLoading({ onComplete, onError }: VoiceSearchLoadingProps) {
  const [currentStep, setCurrentStep] = useState(0);
  const [progress, setProgress] = useState(0);

  const steps = [
    { icon: Mic, text: '음성을 인식하고 있습니다...', duration: 2000 },
    { icon: Volume2, text: '요청을 분석하고 있습니다...', duration: 1500 },
    { icon: MapPin, text: '주변 주차장을 검색하고 있습니다...', duration: 2000 },
    { icon: Car, text: '최적의 주차장을 찾고 있습니다...', duration: 1500 }
  ];

  useEffect(() => {
    let stepTimer: NodeJS.Timeout;
    let progressTimer: NodeJS.Timeout;
    
    const startStep = (stepIndex: number) => {
      if (stepIndex >= steps.length) {
        // 모든 단계 완료 시
        setTimeout(() => {
          // 5% 확률로 에러 발생 시뮬레이션
          if (Math.random() < 0.05) {
            onError();
          } else {
            onComplete();
          }
        }, 500);
        return;
      }

      setCurrentStep(stepIndex);
      setProgress(0);

      const step = steps[stepIndex];
      const progressInterval = step.duration / 100;

      progressTimer = setInterval(() => {
        setProgress(prev => {
          const next = prev + 1;
          if (next >= 100) {
            clearInterval(progressTimer);
            return 100;
          }
          return next;
        });
      }, progressInterval);

      stepTimer = setTimeout(() => {
        clearInterval(progressTimer);
        startStep(stepIndex + 1);
      }, step.duration);
    };

    startStep(0);

    return () => {
      clearTimeout(stepTimer);
      clearInterval(progressTimer);
    };
  }, [onComplete, onError]);

  const CurrentIcon = steps[currentStep]?.icon || Mic;

  return (
    <div className="bg-white min-h-screen flex flex-col items-center justify-center p-6">
      {/* 로고 */}
      <div className="mb-12">
        <div className="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center mb-4 mx-auto">
          <svg 
            className="w-6 h-6 text-white" 
            viewBox="0 0 24 24" 
            fill="currentColor"
          >
            <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
          </svg>
        </div>
        <h1 
          className="text-xl text-blue-900 text-center"
          style={{ 
            fontFamily: 'Inter, sans-serif', 
            fontWeight: '700',
            fontStyle: 'italic',
            transform: 'skewX(-12deg)',
            fontSize: '20px'
          }}
        >
          spark
        </h1>
      </div>

      {/* 애니메이션 아이콘 */}
      <div className="mb-8">
        <motion.div
          className="w-24 h-24 bg-blue-100 rounded-full flex items-center justify-center"
          animate={{
            scale: [1, 1.1, 1],
            rotate: [0, 5, -5, 0]
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            ease: "easeInOut"
          }}
        >
          <motion.div
            animate={{
              scale: [1, 1.2, 1]
            }}
            transition={{
              duration: 1.5,
              repeat: Infinity,
              ease: "easeInOut"
            }}
          >
            <CurrentIcon className="w-12 h-12 text-blue-600" />
          </motion.div>
        </motion.div>
      </div>

      {/* 단계별 메시지 */}
      <div className="text-center mb-8">
        <motion.p 
          key={currentStep}
          className="text-lg text-gray-700 mb-2"
          style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontWeight: '500' }}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          {steps[currentStep]?.text}
        </motion.p>
        
        <p 
          className="text-sm text-gray-500"
          style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontWeight: '400' }}
        >
          잠시만 기다려주세요
        </p>
      </div>

      {/* 진행률 바 */}
      <div className="w-full max-w-xs mb-8">
        <div className="bg-gray-200 rounded-full h-2 overflow-hidden">
          <motion.div
            className="bg-blue-600 h-full rounded-full"
            initial={{ width: 0 }}
            animate={{ width: `${progress}%` }}
            transition={{ duration: 0.1, ease: "easeOut" }}
          />
        </div>
        <div className="flex justify-between mt-2">
          <span 
            className="text-xs text-gray-500"
            style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontWeight: '400' }}
          >
            {currentStep + 1}/4 단계
          </span>
          <span 
            className="text-xs text-gray-500"
            style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontWeight: '400' }}
          >
            {Math.round(progress)}%
          </span>
        </div>
      </div>

      {/* 단계 인디케이터 */}
      <div className="flex space-x-2 mb-8">
        {steps.map((_, index) => (
          <div
            key={index}
            className={`w-3 h-3 rounded-full transition-colors duration-300 ${
              index < currentStep 
                ? 'bg-blue-600' 
                : index === currentStep 
                ? 'bg-blue-400' 
                : 'bg-gray-300'
            }`}
          />
        ))}
      </div>

      {/* 음성 파형 애니메이션 */}
      <div className="flex items-center justify-center space-x-1">
        {[...Array(5)].map((_, i) => (
          <motion.div
            key={i}
            className="w-1 bg-blue-600 rounded-full"
            animate={{
              height: [8, 24, 8],
            }}
            transition={{
              duration: 1.2,
              repeat: Infinity,
              delay: i * 0.1,
              ease: "easeInOut"
            }}
          />
        ))}
      </div>

      {/* 팁 메시지 */}
      <div className="mt-12 text-center">
        <div className="bg-blue-50 rounded-lg p-4 max-w-sm">
          <div className="flex items-start space-x-2">
            <Clock className="w-4 h-4 text-blue-600 mt-0.5 flex-shrink-0" />
            <div>
              <p 
                className="text-sm text-blue-800"
                style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontWeight: '500' }}
              >
                💡 음성 검색 팁
              </p>
              <p 
                className="text-xs text-blue-700 mt-1"
                style={{ fontFamily: 'Inter, Noto Sans KR, sans-serif', fontWeight: '400' }}
              >
                "2시간 주차 가능한 곳", "전기차 충전소 있는 주차장" 등으로 말씀해보세요
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}