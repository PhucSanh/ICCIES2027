'use client';

import React, { useState, useCallback } from 'react';
import { PageHeroBanner } from '@/features/student-assessment/components/page-hero-banner';
import { studentAssessmentService } from '@/features/student-assessment/services';
import { TestStepHeader } from './components/test-step-header';
import { Step1Join } from './components/step-1-join';
import { Step2SelectQuestions, FlatQuestion } from './components/step-2-select-questions';
import { Step3AnswerQuestions } from './components/step-3-answer-questions';
import { Step4LoadingAi } from './components/step-4-loading-ai';
// Tạm ẩn trang đọc feedback AI; giữ component để bật lại sau.
// import { Step5EvaluationResults } from './components/step-5-evaluation-results';
import { StepSurveyRubric } from './components/step-survey-rubric';
import {
  StudentSubmissionJoinedDto,
  StudentAnswerRequest,
  StudentSubmissionResultDto,
} from '@/features/student-assessment/types';

export default function TestAssessmentFlowPage() {
  const [currentStep, setCurrentStep] = useState<number>(1);
  const [session, setSession] = useState<StudentSubmissionJoinedDto | null>(null);
  const [selectedQuestions, setSelectedQuestions] = useState<FlatQuestion[]>([]);
  const [answers, setAnswers] = useState<StudentAnswerRequest[]>([]);
  const [result, setResult] = useState<StudentSubmissionResultDto | null>(null);

  const handleJoinSuccess = async (newSession: StudentSubmissionJoinedDto) => {
    const savedResult = await studentAssessmentService.completedResult(newSession);
    setSession(newSession);
    if (savedResult) {
      setResult(savedResult);
      setCurrentStep(5);
    } else {
      setCurrentStep(2);
    }
  };

  const handleSelectQuestionsSuccess = (questions: FlatQuestion[]) => {
    setSelectedQuestions(questions);
    setCurrentStep(3);
  };

  const handleAnswerSubmit = (submittedAnswers: StudentAnswerRequest[]) => {
    setAnswers(submittedAnswers);
    setCurrentStep(4);
  };

  const handleLoadingComplete = useCallback((evalResult: StudentSubmissionResultDto) => {
    setResult(evalResult);
    setCurrentStep(5);
  }, []);

  const handleResetFlow = () => {
    setSession(null);
    setSelectedQuestions([]);
    setAnswers([]);
    setResult(null);
    setCurrentStep(1);
  };

  return (
    <div className="min-h-full px-4 sm:px-6 lg:px-8 py-8 max-w-7xl mx-auto">
      {/* PACE Page Hero Navy Banner */}
      <PageHeroBanner
        align="center"
        breadcrumbs={[
          { label: 'Hệ thống PACE' },
          { label: 'Phòng kiểm thử', href: '/test' },
          { label: `Bước ${currentStep}: ${
            currentStep === 1
              ? 'Xác thực sinh viên'
              : currentStep === 2
              ? 'Chọn câu hỏi'
              : currentStep === 3
              ? 'Soạn câu trả lời'
              : currentStep === 4
              ? 'AI đang chấm'
              : 'Khảo sát đồng thuận'
          }` },
        ]}
        title="Kiểm thử Đánh giá"
        highlightWord="Vấn đáp"
        description="Nền tảng Hỗ trợ Đồ án & Đánh giá Học phần (PACE) – Ứng dụng Trí tuệ Nhân tạo phân tích kiến trúc mã nguồn và đánh giá năng lực vấn đáp của sinh viên một cách trực quan, chính xác và minh bạch."
      />

      {/* Stepper Header */}
      <TestStepHeader currentStep={currentStep} />

      {/* Step Views */}
      <div className="mt-4">
        {currentStep === 1 && (
          <Step1Join onSuccess={handleJoinSuccess} />
        )}

        {currentStep === 2 && session && (
          <Step2SelectQuestions
            session={session}
            onBack={() => setCurrentStep(1)}
            onSuccess={handleSelectQuestionsSuccess}
          />
        )}

        {currentStep === 3 && (
          <Step3AnswerQuestions
            selectedQuestions={selectedQuestions}
            onBack={() => setCurrentStep(2)}
            onSubmit={handleAnswerSubmit}
          />
        )}

        {currentStep === 4 && session && (
          <Step4LoadingAi
            session={session}
            answers={answers}
            selectedQuestions={selectedQuestions}
            onCompleted={handleLoadingComplete}
          />
        )}

        {/* Tạm ẩn bước đọc feedback AI. Sau khi chấm xong, mở trực tiếp khảo sát.
        {currentStep === 5 && result && (
          <Step5EvaluationResults
            result={result}
            onReset={handleResetFlow}
            onProceedToSurvey={() => setCurrentStep(6)}
          />
        )}
        */}

        {currentStep === 5 && result && (
          <StepSurveyRubric
            result={result}
            onReset={handleResetFlow}
          />
        )}
      </div>
    </div>
  );
}
