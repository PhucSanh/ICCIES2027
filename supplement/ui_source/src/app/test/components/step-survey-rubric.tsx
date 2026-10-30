'use client';

import React, { useState, useEffect } from 'react';
import { 
  Star, 
  Send, 
  CheckCircle2, 
  AlertCircle, 
  Sparkles, 
  MessageSquare, 
  Loader2, 
  ChevronRight,
  ChevronLeft,
  Heart,
  Check
} from 'lucide-react';
import { SavedSurvey } from '@/features/student-assessment/components/saved-survey';
import { detailToResult } from '@/features/student-assessment/services/submission-contract';
import { SurveyQuestionReview } from './survey-question-review';
import { studentAssessmentService } from '@/features/student-assessment/services';
import type { 
  StudentSubmissionResultDto, 
  RubricCriterionItem, 
  SubmitSurveyRequest,
  StudentAnswerSurveyInput
} from '@/features/student-assessment/types';

interface StepSurveyRubricProps {
  result: StudentSubmissionResultDto;
  onReset?: () => void;
  onBackToEvaluation?: () => void;
}

const RATING_LABELS: Record<number, string> = {
  1: 'Hoàn toàn không đồng ý',
  2: 'Không đồng ý',
  3: 'Trung lập / Phân vân',
  4: 'Đồng ý',
  5: 'Hoàn toàn đồng ý',
};

const RATING_COLORS: Record<number, string> = {
  1: 'text-rose-500 fill-rose-500',
  2: 'text-amber-500 fill-amber-500',
  3: 'text-yellow-400 fill-yellow-400',
  4: 'text-teal-500 fill-teal-500',
  5: 'text-emerald-500 fill-emerald-500',
};

export const StepSurveyRubric: React.FC<StepSurveyRubricProps> = ({
  result,
  onReset,
  onBackToEvaluation,
}) => {
  const [savedResult, setSavedResult] = useState<StudentSubmissionResultDto | null>(null);
  const readOnly = result.surveyCompleted || result.evaluatedAnswers.some(a => (a.rubricScores?.length || 0) > 0);
  const [criteria, setCriteria] = useState<RubricCriterionItem[]>([]);
  const [loadingCriteria, setLoadingCriteria] = useState(true);
  const [criteriaError, setCriteriaError] = useState<string | null>(null);

  // Carousel active index (0-based)
  const [activeIndex, setActiveIndex] = useState(0);
  const [reviewedQuestionId, setReviewedQuestionId] = useState<string | null>(null);

  // Ratings state: { [questionId]: { [criterionId]: number } }
  const [ratings, setRatings] = useState<Record<string, Record<string, number>>>({});
  // Hover ratings state for visual preview
  const [hoverRatings, setHoverRatings] = useState<Record<string, Record<string, number>>>({});
  // Student replies state: { [questionId]: string }
  const [replies, setReplies] = useState<Record<string, string>>({});

  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [submitSuccess, setSubmitSuccess] = useState(false);
  const [stepWarning, setStepWarning] = useState<string | null>(null);

  // Fetch criteria
  useEffect(() => {
    let isMounted = true;
    const fetchCriteria = async () => {
      try {
        setLoadingCriteria(true);
        const list = await studentAssessmentService.getCriteria();
        if (isMounted) {
          setCriteria(list.sort((a, b) => a.displayOrder - b.displayOrder));
          setLoadingCriteria(false);
        }
      } catch (err: unknown) {
        if (isMounted) {
          setLoadingCriteria(false);
          setCriteriaError('Không thể tải danh sách tiêu chí khảo sát. Vui lòng thử lại.');
        }
      }
    };

    fetchCriteria();
    return () => {
      isMounted = false;
    };
  }, []);

  const totalQuestions = result.evaluatedAnswers?.length || 0;
  const currentItem = result.evaluatedAnswers?.[activeIndex];

  // Helper check if a question is complete
  const isQuestionAnswered = (questionId: string) => {
    const qRatings = ratings[questionId] || {};
    return criteria.length > 0 && criteria.every(c => (qRatings[c.id] || 0) > 0);
  };

  // Progress calculations
  const answeredQuestionsCount = result.evaluatedAnswers?.filter(item => 
    isQuestionAnswered(item.questionId)
  ).length || 0;

  const isCurrentQuestionDone = currentItem ? isQuestionAnswered(currentItem.questionId) : false;
  const isFormComplete = totalQuestions > 0 && criteria.length > 0 && answeredQuestionsCount === totalQuestions;

  const handleRatingChange = (questionId: string, criterionId: string, score: number) => {
    setStepWarning(null);
    setRatings(prev => ({
      ...prev,
      [questionId]: {
        ...(prev[questionId] || {}),
        [criterionId]: score,
      },
    }));
  };

  const handleHoverChange = (questionId: string, criterionId: string, score: number) => {
    setHoverRatings(prev => ({
      ...prev,
      [questionId]: {
        ...(prev[questionId] || {}),
        [criterionId]: score,
      },
    }));
  };

  const handleReplyChange = (questionId: string, text: string) => {
    setReplies(prev => ({
      ...prev,
      [questionId]: text,
    }));
  };

  // Carousel Navigation handlers
  const handleNext = () => {
    if (!isCurrentQuestionDone) {
      setStepWarning('Bạn vui lòng đánh giá đầy đủ các tiêu chí sao cho câu hỏi này trước khi sang câu tiếp theo nhé!');
      return;
    }
    setStepWarning(null);
    if (activeIndex < totalQuestions - 1) {
      setReviewedQuestionId(null);
      setActiveIndex(prev => prev + 1);
      window.scrollTo({ top: 120, behavior: 'smooth' });
    }
  };

  const handlePrevious = () => {
    setStepWarning(null);
    if (activeIndex > 0) {
      setReviewedQuestionId(null);
      setActiveIndex(prev => prev - 1);
      window.scrollTo({ top: 120, behavior: 'smooth' });
    }
  };

  // Submit survey
  const handleSubmitSurvey = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    setSubmitError(null);
    setStepWarning(null);

    if (!isFormComplete) {
      setSubmitError('Vui lòng đánh giá đủ tất cả tiêu chí cho toàn bộ các câu hỏi trước khi hoàn tất.');
      return;
    }

    if (readOnly || savedResult) return;
    setSubmitting(true);
    try {
      const answersInput: StudentAnswerSurveyInput[] = result.evaluatedAnswers.map(item => {
        const qRatings = ratings[item.questionId] || {};
        const studentAnswerId = item.studentAnswerId || item.aiEvaluation?.student_answer_id || '';

        return {
          studentAnswerId: studentAnswerId,
          questionId: item.questionId,
          studentReply: replies[item.questionId]?.trim() || undefined,
          scores: criteria.map(c => ({
            criterionId: c.id,
            score: qRatings[c.id] || 5,
          })),
        };
      });

      const payload: SubmitSurveyRequest = {
        submissionId: result.submissionId,
        answers: answersInput,
      };

      await studentAssessmentService.submitSurvey(payload);
      setSubmitSuccess(true);
      setSavedResult(detailToResult(await studentAssessmentService.retrieve({ submissionId: result.submissionId })));
      setSubmitting(false);
      setSubmitSuccess(true);
      window.scrollTo({ top: 80, behavior: 'smooth' });
    } catch (err: any) {
      if (err.response?.status === 409) {
        try {
          const persisted = detailToResult(await studentAssessmentService.retrieve({ submissionId: result.submissionId }));
          if (persisted.surveyCompleted) setSavedResult(persisted);
        } catch { /* Preserve the original server error if reload is unavailable. */ }
      }
      setSubmitting(false);
      const msg = err.response?.data?.message || err.message || 'Không thể lưu kết quả khảo sát. Vui lòng thử lại.';
      setSubmitError(msg);
    }
  };

  // MÀN HÌNH HOÀN THÀNH: "Cảm ơn bạn rất nhiều!"
  if (savedResult || readOnly) return <SavedSurvey result={savedResult || result} />;

  if (submitSuccess) {
    return (
      <div className="max-w-3xl mx-auto rounded-[32px] border border-line bg-panel p-8 md:p-14 shadow-card text-center space-y-8 animate-in zoom-in-95 duration-400">
        <div className="relative mx-auto w-24 h-24 rounded-full bg-gradient-to-tr from-rose-500/10 via-accent/15 to-emerald-500/10 flex items-center justify-center">
          <div className="w-18 h-18 rounded-full bg-panel shadow-sm flex items-center justify-center border border-line">
            <Heart className="w-10 h-10 text-rose-500 fill-rose-500 animate-pulse" />
          </div>
          <span className="absolute -top-1 -right-1 w-7 h-7 rounded-full bg-emerald-500 text-white flex items-center justify-center shadow-md">
            <Check className="w-4 h-4 stroke-[3]" />
          </span>
        </div>

        <div className="space-y-3">
          <span className="inline-flex items-center gap-1.5 px-3.5 py-1 rounded-full bg-emerald-50 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-300 text-xs font-bold border border-emerald-200 dark:border-emerald-800">
            <CheckCircle2 className="w-3.5 h-3.5" />
            Khảo sát đã hoàn tất thành công
          </span>

          <h1 className="text-3xl md:text-5xl font-black text-fg tracking-tight">
            Cảm ơn bạn rất nhiều!
          </h1>

          <p className="text-sm md:text-base text-subtle max-w-xl mx-auto leading-relaxed pt-1">
            Đánh giá mức độ đồng thuận của bạn đối với nhận xét của AI là dữ liệu vô cùng quý giá, giúp hệ thống không ngừng nâng cao năng lực hỗ trợ sinh viên trong các bài tập tiếp theo.
          </p>
        </div>

        {/* Stats card */}
        <div className="p-5 md:p-6 rounded-2xl bg-bg border border-line text-xs text-muted grid grid-cols-3 gap-4">
          <div>
            <span className="block text-subtle font-medium text-xs mb-1">Số câu đã khảo sát</span>
            <strong className="text-base md:text-lg font-bold text-fg">{totalQuestions} / {totalQuestions} câu</strong>
          </div>
          <div className="border-x border-line">
            <span className="block text-subtle font-medium text-xs mb-1">Tiêu chí mỗi câu</span>
            <strong className="text-base md:text-lg font-bold text-fg">{criteria.length} tiêu chí</strong>
          </div>
          <div>
            <span className="block text-subtle font-medium text-xs mb-1">Trạng thái dữ liệu</span>
            <strong className="text-base md:text-lg font-bold text-emerald-600 dark:text-emerald-400">Đã lưu thành công</strong>
          </div>
        </div>

        {onBackToEvaluation && (
          <div className="pt-2 flex flex-wrap items-center justify-center gap-4">
            <button
              type="button"
              onClick={onBackToEvaluation}
              className="h-12 px-8 rounded-full border border-line-strong bg-panel text-sm text-fg font-semibold hover:bg-raised transition-all"
            >
              Xem lại nhận xét AI
            </button>
          </div>
        )}
      </div>
    );
  }

  const currentQRatings = currentItem ? (ratings[currentItem.questionId] || {}) : {};
  const currentQHover = currentItem ? (hoverRatings[currentItem.questionId] || {}) : {};

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-16">
      {/* Top Banner & Question Progress Indicators */}
      <div className="rounded-[24px] border border-line bg-panel p-6 md:p-8 shadow-card space-y-5">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1.5">
            <div className="flex flex-wrap items-center gap-2.5">
              <span className="inline-flex items-center px-3.5 py-1 rounded-full bg-accent text-white text-xs font-bold whitespace-nowrap shrink-0 shadow-xs">
                Bước 5: Khảo sát mức độ đồng thuận
              </span>
              <span className="inline-flex items-center text-xs text-subtle font-mono bg-raised px-2.5 py-1 rounded-full border border-line whitespace-nowrap shrink-0">
                Đã hoàn thành: {answeredQuestionsCount}/{totalQuestions} câu
              </span>
            </div>

            <h2 className="text-xl md:text-2xl font-extrabold text-fg tracking-tight">
              Khảo sát Đánh giá <span className="text-accent">Nhận xét của AI</span>
            </h2>
          </div>

          {onBackToEvaluation && (
            <button
              type="button"
              onClick={onBackToEvaluation}
              className="h-9 px-4 rounded-full border border-line-strong bg-panel text-xs text-fg font-medium hover:bg-raised transition-all self-start md:self-center shrink-0"
            >
              &larr; Xem lại nhận xét đầy đủ
            </button>
          )}
        </div>

        {/* Carousel Progress Bar */}
        <div className="w-full bg-line rounded-full h-2 overflow-hidden">
          <div 
            className="bg-accent h-full transition-all duration-300 ease-out"
            style={{ width: `${totalQuestions > 0 ? (answeredQuestionsCount / totalQuestions) * 100 : 0}%` }}
          />
        </div>
      </div>

      {loadingCriteria ? (
        <div className="rounded-[24px] border border-line bg-panel p-16 text-center space-y-3">
          <Loader2 className="w-8 h-8 text-accent animate-spin mx-auto" />
          <p className="text-sm font-medium text-fg">Đang tải bộ tiêu chí khảo sát Rubric…</p>
        </div>
      ) : criteriaError ? (
        <div className="rounded-[24px] border border-red-200 bg-red-50 p-8 text-center space-y-3">
          <AlertCircle className="w-8 h-8 text-red-600 mx-auto" />
          <p className="text-sm text-red-700">{criteriaError}</p>
          <button
            type="button"
            onClick={() => window.location.reload()}
            className="h-9 px-4 rounded-lg bg-red-600 text-white text-xs font-semibold"
          >
            Tải lại trang
          </button>
        </div>
      ) : currentItem && reviewedQuestionId !== currentItem.questionId ? (
        <SurveyQuestionReview
          key={currentItem.questionId}
          questionNumber={activeIndex + 1}
          totalQuestions={totalQuestions}
          businessName={currentItem.businessName}
          questionText={currentItem.questionText}
          answerText={currentItem.answerText}
          feedback={currentItem.aiEvaluation}
          error={currentItem.evaluationError}
          onStart={() => setReviewedQuestionId(currentItem.questionId)}
        />
      ) : currentItem ? (
        <div className="space-y-6">
          {/* Main Slide Card */}
          <div 
            key={currentItem.questionId}
            className="rounded-[28px] border border-line bg-panel p-6 md:p-8 shadow-card space-y-6 animate-in fade-in-50 duration-200"
          >
            {/* Header: Question Badge & Title */}
            <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-3 pb-5 border-b border-line">
              <div className="space-y-1.5">
                <div className="flex items-center gap-2">
                  <span className="px-2.5 py-0.5 rounded-full bg-accent/10 text-accent font-bold text-xs uppercase tracking-wider">
                    {currentItem.businessName}
                  </span>
                  <span className="text-xs font-semibold text-muted">
                    Câu hỏi {activeIndex + 1} / {totalQuestions}
                  </span>
                </div>
                <h3 className="text-base md:text-xl font-bold text-fg leading-snug">
                  {currentItem.questionText}
                </h3>
              </div>

              <span className={`h-7 px-3 rounded-full text-xs font-semibold shrink-0 self-start inline-flex items-center gap-1.5 ${
                isCurrentQuestionDone 
                  ? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800' 
                  : 'bg-amber-50 text-amber-700 dark:bg-amber-950 dark:text-amber-300 border border-amber-200 dark:border-amber-800'
              }`}>
                {isCurrentQuestionDone ? (
                  <>
                    <CheckCircle2 size={14} className="text-emerald-600" />
                    <span>Đã đánh giá câu này</span>
                  </>
                ) : (
                  <>
                    <AlertCircle size={14} className="text-amber-600" />
                    <span>Chưa đánh giá đủ</span>
                  </>
                )}
              </span>
            </div>

            <button
              type="button"
              onClick={() => setReviewedQuestionId(null)}
              className="text-sm font-semibold text-accent hover:underline focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent rounded"
            >
              Đọc lại câu trả lời và nhận xét AI
            </button>

            {/* 3. RUBRIC SURVEY CRITERIA RATING */}
            <div className="space-y-4 pt-2">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1 pb-1 border-b border-line">
                <h4 className="text-xs font-bold uppercase tracking-wider text-fg flex items-center gap-1.5">
                  <Sparkles className="w-4 h-4 text-accent" />
                  <span>Mức độ đồng thuận của bạn đối với nhận xét này (1 đến 5 sao):</span>
                </h4>
                <span className="text-xs text-muted">1: Rất không đồng ý &rarr; 5: Rất đồng ý</span>
              </div>

              <div className="space-y-3.5">
                {criteria.map((crit) => {
                  const selectedScore = currentQRatings[crit.id] || 0;
                  const activeHoverScore = currentQHover[crit.id] || 0;
                  const displayScore = activeHoverScore || selectedScore;

                  return (
                    <div 
                      key={crit.id}
                      className="rounded-2xl border border-line bg-bg p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3.5 hover:border-line-strong transition-colors"
                    >
                      <div className="space-y-1 sm:max-w-[55%]">
                        <div className="flex items-center gap-2">
                          <span className="rounded bg-orange-100 dark:bg-orange-950 px-2 py-0.5 font-mono text-[11px] font-bold text-orange-900 dark:text-orange-200">
                            {crit.code}
                          </span>
                          <p className="text-xs md:text-sm font-bold text-fg">
                            {crit.name}
                          </p>
                        </div>
                        <p className="text-xs text-subtle leading-relaxed">
                          {crit.statement}
                        </p>
                      </div>

                      {/* Star Rating Group */}
                      <div className="flex flex-col sm:items-end gap-1 shrink-0">
                        <div 
                          className="flex items-center gap-1.5"
                          onMouseLeave={() => handleHoverChange(currentItem.questionId, crit.id, 0)}
                        >
                          {[1, 2, 3, 4, 5].map((star) => {
                            const isFilled = displayScore >= star;
                            const activeColor = RATING_COLORS[displayScore] || 'text-amber-400 fill-amber-400';

                            return (
                              <button
                                key={star}
                                type="button"
                                onClick={() => handleRatingChange(currentItem.questionId, crit.id, star)}
                                onMouseEnter={() => handleHoverChange(currentItem.questionId, crit.id, star)}
                                className="p-1 rounded-full transition-transform hover:scale-125 focus:outline-none"
                                title={`${star} sao: ${RATING_LABELS[star]}`}
                              >
                                <Star 
                                  className={`w-6 h-6 transition-colors ${
                                    isFilled ? activeColor : 'text-slate-300 dark:text-slate-700'
                                  }`} 
                                />
                              </button>
                            );
                          })}
                        </div>

                        <span className="text-[11px] font-medium text-subtle min-h-[16px]">
                          {displayScore > 0 ? (
                            <span className="font-semibold text-fg">
                              {displayScore} ⭐ — {RATING_LABELS[displayScore]}
                            </span>
                          ) : (
                            <span className="text-slate-400 italic">Chưa đánh giá</span>
                          )}
                        </span>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Optional student comment */}
            <div className="space-y-1.5 pt-1">
              <label className="text-xs font-bold uppercase tracking-wider text-subtle flex items-center gap-1.5">
                <MessageSquare className="w-3.5 h-3.5" />
                <span>Ý kiến hoặc phản hồi bổ sung của bạn cho câu hỏi này (tùy chọn):</span>
              </label>
              <textarea
                rows={2}
                value={replies[currentItem.questionId] || ''}
                onChange={(e) => handleReplyChange(currentItem.questionId, e.target.value)}
                placeholder="VD: Nhận xét của AI rất chi tiết, tôi đồng ý với phần phân tích nghiệp vụ..."
                className="w-full rounded-2xl border border-line bg-bg p-3.5 text-xs md:text-sm text-fg placeholder:text-muted focus:border-accent focus:outline-none leading-relaxed"
              />
            </div>
          </div>

          {/* Feedback & Error alerts */}
          {stepWarning && (
            <div className="flex items-center gap-2.5 rounded-2xl border border-amber-300 bg-amber-50 dark:bg-amber-950/40 dark:border-amber-800 p-4 text-xs md:text-sm text-amber-800 dark:text-amber-200 animate-in fade-in duration-200">
              <AlertCircle className="w-5 h-5 shrink-0" />
              <span>{stepWarning}</span>
            </div>
          )}

          {submitError && (
            <div className="flex items-start gap-2.5 rounded-2xl border border-red-200 bg-red-50 dark:bg-red-950/40 dark:border-red-800 p-4 text-xs md:text-sm text-red-700 dark:text-red-300 animate-in fade-in duration-200">
              <AlertCircle className="w-5 h-5 shrink-0 mt-0.5" />
              <span>{submitError}</span>
            </div>
          )}

          {/* Carousel Navigation Bottom Bar */}
          <div className="rounded-[24px] border border-line bg-panel p-5 md:p-6 shadow-card flex items-center justify-between gap-4">
            {/* Previous Button */}
            <button
              type="button"
              onClick={handlePrevious}
              disabled={activeIndex === 0}
              className="h-11 px-5 rounded-full border border-line-strong bg-panel text-xs md:text-sm text-fg font-semibold hover:bg-raised transition-all disabled:opacity-30 disabled:cursor-not-allowed inline-flex items-center gap-1.5"
            >
              <ChevronLeft className="w-4 h-4" />
              <span>Câu trước</span>
            </button>

            {/* Current Position Indicator */}
            <div className="text-xs font-bold text-fg hidden sm:block">
              Câu {activeIndex + 1} / {totalQuestions}
            </div>

            {/* Next or Finish Button */}
            {activeIndex < totalQuestions - 1 ? (
              <button
                type="button"
                onClick={handleNext}
                className="h-11 px-6 rounded-full bg-accent text-white font-semibold text-xs md:text-sm hover:bg-accent-strong active:scale-95 transition-all shadow-glow inline-flex items-center gap-1.5"
              >
                <span>Sang câu tiếp theo</span>
                <ChevronRight className="w-4 h-4" />
              </button>
            ) : (
              <button
                type="button"
                onClick={() => handleSubmitSurvey()}
                disabled={!isFormComplete || submitting}
                className="h-12 px-7 rounded-full bg-emerald-600 text-white font-semibold text-xs md:text-sm hover:bg-emerald-700 active:scale-95 transition-all shadow-glow disabled:opacity-40 disabled:cursor-not-allowed inline-flex items-center gap-2"
              >
                {submitting ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>Đang hoàn tất…</span>
                  </>
                ) : (
                  <>
                    <Send className="w-4 h-4" />
                    <span>Hoàn tất & Gửi khảo sát</span>
                  </>
                )}
              </button>
            )}
          </div>
        </div>
      ) : null}
    </div>
  );
};

