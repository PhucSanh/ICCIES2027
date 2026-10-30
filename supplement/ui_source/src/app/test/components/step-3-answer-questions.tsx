'use client';

import React, { useState } from 'react';
import {
  FileText,
  ArrowRight,
  ArrowLeft,
  AlertCircle,
  Sparkles,
  CheckCircle2,
  Clock,
  Layers,
  Send,
} from 'lucide-react';
import { FlatQuestion } from './step-2-select-questions';
import { StudentAnswerRequest } from '@/features/student-assessment/types';

interface Step3AnswerQuestionsProps {
  selectedQuestions: FlatQuestion[];
  onBack: () => void;
  onSubmit: (answers: StudentAnswerRequest[]) => void;
}

const MAX_WORDS = 2000;

export const Step3AnswerQuestions: React.FC<Step3AnswerQuestionsProps> = ({
  selectedQuestions,
  onBack,
  onSubmit,
}) => {
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [validationError, setValidationError] = useState<string | null>(null);

  // Helper count words
  const countWords = (text: string): number => {
    const trimmed = text.trim();
    if (!trimmed) return 0;
    return trimmed.split(/\s+/).filter(Boolean).length;
  };

  const handleTextChange = (questionId: string, val: string) => {
    setValidationError(null);
    setAnswers((prev) => ({
      ...prev,
      [questionId]: val,
    }));
  };

  // Pre-fill realistic sample answers for quick testing

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setValidationError(null);

    // Validate that all questions are answered
    for (let i = 0; i < selectedQuestions.length; i++) {
      const q = selectedQuestions[i];
      const text = (answers[q.questionId] || '').trim();

      if (!text || text.length < 5) {
        setValidationError(`Vui lòng nhập câu trả lời cho Câu ${i + 1} (${q.businessName}).`);
        return;
      }

      const words = countWords(text);
      if (words > MAX_WORDS) {
        setValidationError(`Câu trả lời số ${i + 1} đã vượt quá giới hạn 2000 từ (${words}/2000 từ). Vui lòng rút gọn.`);
        return;
      }
    }

    const payload: StudentAnswerRequest[] = selectedQuestions.map((q) => ({
      businessId: q.businessId,
      questionId: q.questionId,
      answerText: (answers[q.questionId] || '').trim(),
    }));

    onSubmit(payload);
  };

  // Check overall completion
  const completedCount = selectedQuestions.filter((q) => {
    const txt = (answers[q.questionId] || '').trim();
    return txt.length >= 5 && countWords(txt) <= MAX_WORDS;
  }).length;

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Top Banner */}
      <div className="rounded-[20px] border border-line bg-panel p-5 shadow-card flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <span className="text-xs font-bold text-accent uppercase tracking-wider">
            Bước 3: Soạn thảo câu trả lời
          </span>
          <h2 className="text-lg font-bold text-fg mt-0.5">
            Trả lời {selectedQuestions.length} câu hỏi đã chọn
          </h2>
        </div>

        <div className="flex items-center gap-3">
          <span className="text-xs font-bold text-fg">
            {completedCount}/{selectedQuestions.length} câu hoàn tất
          </span>
        </div>
      </div>

      {/* Validation Error banner */}
      {validationError && (
        <div className="rounded-xl border border-err/30 bg-err/5 p-4 flex items-center gap-3 text-xs md:text-sm text-err">
          <AlertCircle className="w-5 h-5 shrink-0" />
          <span>{validationError}</span>
        </div>
      )}

      {/* Answer Form */}
      <form onSubmit={handleSubmit} className="space-y-6">
        {selectedQuestions.map((q, idx) => {
          const currentText = answers[q.questionId] || '';
          const words = countWords(currentText);
          const isOverLimit = words > MAX_WORDS;

          return (
            <div
              key={q.questionId}
              className="rounded-[24px] border border-line bg-panel p-6 md:p-8 shadow-card space-y-4"
            >
              {/* Question header */}
              <div className="flex items-start gap-3 pb-3 border-b border-line">
                <span className="w-8 h-8 rounded-full bg-navy text-white text-xs font-bold flex items-center justify-center shrink-0 mt-0.5">
                  0{idx + 1}
                </span>
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <span className="text-[11px] font-bold text-accent uppercase tracking-wider">
                      [{q.businessName}]
                    </span>
                  </div>
                  <h3 className="text-base md:text-lg font-semibold text-fg leading-relaxed mt-1">
                    {q.questionText}
                  </h3>
                </div>
              </div>

              {/* Textarea container */}
              <div>
                <div className="flex items-center justify-between mb-2">
                  <label
                    htmlFor={`ans-${q.questionId}`}
                    className="text-xs font-bold uppercase tracking-wider text-fg flex items-center gap-1.5"
                  >
                    <FileText className="w-3.5 h-3.5 text-accent" />
                    <span>Nội dung câu trả lời (Giới hạn tối đa 2000 từ)</span>
                  </label>

                  <div className="flex items-center gap-3 text-xs">
                    <span
                      className={`font-mono font-bold ${
                        isOverLimit
                          ? 'text-err bg-err/10 px-2 py-0.5 rounded'
                          : words > 1500
                          ? 'text-warn'
                          : 'text-subtle'
                      }`}
                    >
                      {words} / {MAX_WORDS} từ
                    </span>
                  </div>
                </div>

                <textarea
                  id={`ans-${q.questionId}`}
                  rows={7}
                  value={currentText}
                  onChange={(e) => handleTextChange(q.questionId, e.target.value)}
                  placeholder="Nhập giải thích chi tiết về luồng xử lý mã nguồn, lớp đối tượng, hàm phụ trách và cách bắt lỗi ngoại lệ trong dự án..."
                  className={`w-full p-4 rounded-2xl border text-fg text-sm leading-relaxed outline-none transition-all placeholder:text-subtle font-sans ${
                    isOverLimit
                      ? 'border-err bg-err/5 focus:ring-2 focus:ring-err/20'
                      : 'border-line-strong bg-panel focus:border-accent focus:ring-2 focus:ring-accent/20'
                  }`}
                />

                {isOverLimit && (
                  <p className="mt-1.5 text-xs text-err font-medium flex items-center gap-1">
                    <AlertCircle className="w-3.5 h-3.5" />
                    Bạn đã vượt quá {words - MAX_WORDS} từ. Vui lòng rút gọn dưới 2000 từ để được nộp bài.
                  </p>
                )}
              </div>
            </div>
          );
        })}

        {/* Action Bottom Bar */}
        <div className="pt-4 flex items-center justify-between">
          <button
            type="button"
            onClick={onBack}
            className="h-10 px-4 rounded-[10px] border border-line-strong bg-panel text-sm text-fg font-medium hover:bg-raised transition-all inline-flex items-center gap-1.5"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Quay lại chọn câu hỏi</span>
          </button>

          {/* ONE primary button per area, orange pill */}
          <button
            type="submit"
            className="h-11 px-8 rounded-full bg-accent text-white font-semibold text-sm hover:bg-accent-strong active:scale-95 transition-all shadow-glow inline-flex items-center gap-2"
          >
            <Send className="w-4 h-4" />
            <span>Nộp bài & Chờ AI chấm điểm</span>
          </button>
        </div>
      </form>
    </div>
  );
};
