'use client';

import { useEffect, useId, useRef } from 'react';
import { SurveyAiFeedback } from '@/features/student-assessment/components/survey-ai-feedback';
import type { StudentAnswerRes } from '@/features/student-assessment/types';

interface SurveyQuestionReviewProps {
  questionNumber: number;
  totalQuestions: number;
  businessName: string;
  questionText: string;
  answerText?: string | null;
  feedback?: StudentAnswerRes | null;
  error?: string | null;
  onStart: () => void;
}

/** Read this question's saved answer and AI feedback before rating it. */
export function SurveyQuestionReview({
  questionNumber, totalQuestions, businessName, questionText, answerText, feedback, error, onStart,
}: SurveyQuestionReviewProps) {
  const dialogRef = useRef<HTMLDialogElement>(null);
  const headingRef = useRef<HTMLHeadingElement>(null);
  const titleId = useId();
  const descriptionId = useId();

  useEffect(() => {
    const dialog = dialogRef.current;
    const previousFocus = document.activeElement;
    if (dialog && !dialog.open) {
      dialog.showModal();
      headingRef.current?.focus();
    }
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => {
      dialog?.close();
      document.body.style.overflow = previousOverflow;
      if (previousFocus instanceof HTMLElement && previousFocus.isConnected) previousFocus.focus();
    };
  }, []);

  return (
    <dialog
      ref={dialogRef}
      aria-labelledby={titleId}
      aria-describedby={descriptionId}
      onCancel={event => event.preventDefault()}
      className="fixed inset-0 m-auto w-[calc(100%-2rem)] max-w-3xl max-h-[90dvh] rounded-3xl border border-line bg-panel p-0 text-fg shadow-2xl backdrop:bg-black/60 backdrop:backdrop-blur-sm"
    >
      <div className="flex max-h-[90dvh] flex-col">
        <header className="shrink-0 border-b border-line px-5 py-4 md:px-7">
          <p className="text-xs font-bold text-accent">Câu {questionNumber} / {totalQuestions} · {businessName}</p>
          <h2 ref={headingRef} tabIndex={-1} id={titleId} className="mt-1 text-lg md:text-xl font-bold outline-none">
            Đọc câu trả lời và nhận xét của AI
          </h2>
          <p id={descriptionId} className="mt-2 text-sm text-muted">
            Đọc nội dung bên dưới, sau đó bấm “Bắt đầu đánh giá” để điền khảo sát cho câu này.
          </p>
        </header>
        <div className="min-h-0 overflow-y-auto overscroll-contain p-5 md:p-7 space-y-6">
          <section className="space-y-2">
            <h3 className="text-xs font-bold uppercase tracking-wider text-accent">Câu hỏi</h3>
            <p className="text-sm md:text-base font-semibold leading-relaxed whitespace-pre-wrap">{questionText}</p>
          </section>
          <section className="space-y-2">
            <h3 className="text-xs font-bold uppercase tracking-wider text-accent">Câu trả lời của bạn</h3>
            <p className="rounded-2xl border border-line bg-bg p-4 text-sm leading-relaxed whitespace-pre-wrap">
              {answerText?.trim() ? answerText : '(Không có nội dung câu trả lời)'}
            </p>
          </section>
          <section className="space-y-3">
            <h3 className="text-xs font-bold uppercase tracking-wider text-accent">Nhận xét của AI</h3>
            <SurveyAiFeedback feedback={feedback} error={error} />
          </section>
        </div>
        <footer className="shrink-0 border-t border-line px-5 py-4 md:px-7 flex justify-end">
          <button type="button" onClick={onStart} className="h-11 rounded-full bg-accent px-6 text-sm font-semibold text-white hover:bg-accent-strong focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent focus-visible:ring-offset-2">
            Bắt đầu đánh giá
          </button>
        </footer>
      </div>
    </dialog>
  );
}
