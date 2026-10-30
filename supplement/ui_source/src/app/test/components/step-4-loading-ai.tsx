'use client';

import React, { useEffect, useState } from 'react';
import {
  BrainCircuit,
  CheckCircle2,
  Loader2,
  AlertCircle,
  RotateCcw,
  Sparkles,
  ArrowRight,
} from 'lucide-react';
import { studentAssessmentService } from '@/features/student-assessment/services';
import {
  StudentAnswerRequest,
  StudentSubmissionResultDto,
  StudentSubmissionJoinedDto,
} from '@/features/student-assessment/types';
import { detailToResult } from '@/features/student-assessment/services/submission-contract';
import { FlatQuestion } from './step-2-select-questions';

interface Step4LoadingAiProps {
  session: StudentSubmissionJoinedDto;
  answers: StudentAnswerRequest[];
  selectedQuestions: FlatQuestion[];
  onCompleted: (result: StudentSubmissionResultDto) => void;
}

export const Step4LoadingAi: React.FC<Step4LoadingAiProps> = ({
  session,
  answers,
  selectedQuestions,
  onCompleted,
}) => {
  const attempt = React.useRef<Promise<StudentSubmissionResultDto> | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [progressStage, setProgressStage] = useState(1);

  const executeSubmit = React.useCallback(async () => {
    setError(null);
    setProgressStage(1);

    const timer1 = setTimeout(() => setProgressStage(2), 1200);
    const timer2 = setTimeout(() => setProgressStage(3), 2800);

    try {
      attempt.current ||= studentAssessmentService.submit({
        submissionId: session.submissionId,
        answers: answers,
      });
      const response = await attempt.current;

      clearTimeout(timer1);
      clearTimeout(timer2);
      onCompleted(response);
    } catch (err: unknown) {
      clearTimeout(timer1);
      clearTimeout(timer2);
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const msg = (err as any)?.response?.data?.message || (err as any)?.message;
      setError(msg || 'Lỗi kết nối khi nộp bài. Có thể backend API chưa chạy hoặc gặp sự cố mạng.');
    }
  }, [answers, onCompleted, session.submissionId]);

  useEffect(() => {
    executeSubmit();
  }, [executeSubmit]);

  // Existing result action retrieves persisted data; it never creates demo feedback.
  const handleViewSavedResult = async () => {
    try {
      const detail = await studentAssessmentService.retrieve({ submissionId: session.submissionId });
      onCompleted(detailToResult(detail));
    } catch (error) { setError(error instanceof Error ? error.message : 'Không lấy được bài đã nộp.'); }
  };

  return (
    <div className="max-w-xl mx-auto py-8">
      <div className="rounded-[28px] border border-line bg-panel p-8 md:p-12 shadow-card text-center space-y-6">
        {/* Animated AI Brain Icon */}
        <div className="relative mx-auto w-20 h-20 flex items-center justify-center">
          <div className="absolute inset-0 rounded-full border-4 border-accent border-t-transparent animate-spin" />
          <div className="w-16 h-16 rounded-full bg-accent-soft flex items-center justify-center">
            <BrainCircuit className="w-8 h-8 text-accent animate-pulse" />
          </div>
        </div>

        {/* Heading */}
        <div>
          <span className="text-xs font-bold text-accent uppercase tracking-wider inline-flex items-center gap-1.5">
            <Sparkles className="w-3.5 h-3.5" />
            Bước 4: Chờ AI chấm điểm
          </span>
          <h2 className="text-xl md:text-2xl font-extrabold text-fg tracking-tight mt-1">
            Đang phân tích & Đánh giá bài làm...
          </h2>
          <p className="mt-2 text-xs md:text-sm text-muted leading-relaxed">
            Hệ thống đang đối chiếu câu trả lời của bạn với mã nguồn thực tế trong repository để xây dựng nhận xét sư phạm.
          </p>
        </div>

        {/* Error Notice if API fails */}
        {error ? (
          <div className="rounded-2xl border border-err/30 bg-err/5 p-5 text-left space-y-3">
            <div className="flex items-start gap-3 text-err text-xs md:text-sm">
              <AlertCircle className="w-5 h-5 shrink-0 mt-0.5" />
              <div>
                <p className="font-bold">Chưa tải được kết quả bài làm</p>
                <p className="text-muted mt-0.5">{error}</p>
              </div>
            </div>

            <div className="pt-2 flex flex-col sm:flex-row items-center justify-between gap-3 border-t border-err/20">
              <button
                type="button"
                onClick={handleViewSavedResult}
                className="h-9 px-4 rounded-full border border-err text-err hover:bg-err/10 text-xs font-semibold inline-flex items-center gap-1.5"
              >
                <RotateCcw className="w-3.5 h-3.5" />
                <span>Tải lại kết quả</span>
              </button>

              <button
                type="button"
                onClick={handleViewSavedResult}
                className="h-9 px-5 rounded-full bg-accent text-white text-xs font-semibold hover:bg-accent-strong shadow-glow inline-flex items-center gap-1.5"
              >
                <span>Xem bài làm đã lưu</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        ) : (
          /* Processing Steps List */
          <div className="rounded-2xl border border-line bg-bg p-5 text-left text-xs space-y-3">
            <div className="flex items-center gap-3">
              <CheckCircle2 className="w-4 h-4 text-ok shrink-0" />
              <span className="font-semibold text-fg">1. Đã đóng băng và gửi {answers.length} câu trả lời</span>
            </div>

            <div className="flex items-center gap-3">
              {progressStage >= 2 ? (
                <CheckCircle2 className="w-4 h-4 text-ok shrink-0" />
              ) : (
                <Loader2 className="w-4 h-4 text-accent animate-spin shrink-0" />
              )}
              <span className={progressStage >= 2 ? 'font-semibold text-fg' : 'text-accent font-bold'}>
                2. AI đối chiếu mã nguồn repository ({session.repoName || 'Repo'})
              </span>
            </div>

            <div className="flex items-center gap-3">
              {progressStage >= 3 ? (
                <Loader2 className="w-4 h-4 text-accent animate-spin shrink-0" />
              ) : (
                <div className="w-4 h-4 rounded-full border border-line-strong flex items-center justify-center text-[10px] text-subtle">
                  3
                </div>
              )}
              <span className={progressStage >= 3 ? 'text-accent font-bold' : 'text-subtle'}>
                3. Đang nhận xét
              </span>
            </div>
          </div>
        )}

        <p className="text-[11px] text-subtle">
          Bạn có thể mở lại bài đã nộp để xem câu hỏi, câu trả lời và feedback đã lưu.
        </p>
      </div>
    </div>
  );
};
