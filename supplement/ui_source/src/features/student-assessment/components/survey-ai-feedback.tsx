import type { StudentAnswerRes } from '../types';

/** Show every returned section, including mixed/legacy feedback formats. */
export function SurveyAiFeedback({ feedback, error }: { feedback?: StudentAnswerRes | null; error?: string | null }) {
  const sections = [
    ['Điểm sáng & Nội dung hiểu đúng', feedback?.positives],
    ['Điểm cần hoàn thiện & Lưu ý kỹ thuật', feedback?.constructive_criticism],
    ['Hướng dẫn cải thiện tiếp theo', feedback?.next_steps],
    ['Giải thích logic', feedback?.logic_explanation],
    ['Tổng hợp đánh giá', feedback?.researching?.consensus_summary],
    ['Đối chiếu mã nguồn', feedback?.researching?.code_inspection],
    ['Hướng dẫn sư phạm', feedback?.researching?.pedagogical_guidance],
    ['Nhận xét chung', feedback?.comment],
  ].filter(([, text]) => text?.trim());
  const criteria = (feedback?.criteria || []).filter(c => c.name?.trim() || c.comment?.trim());
  const code = feedback?.code_evidence?.trim();
  const hasContent = sections.length > 0 || criteria.length > 0 || !!code;

  return <div className="space-y-3">
    {sections.map(([label, text]) => <section key={label} className="rounded-2xl border border-line bg-raised/50 p-4 space-y-1">
      <h4 className="text-xs font-bold uppercase tracking-wider text-subtle">{label}</h4>
      <p className="text-xs md:text-sm text-fg leading-relaxed whitespace-pre-wrap">{text}</p>
    </section>)}
    {criteria.length > 0 && <section className="rounded-2xl border border-line bg-raised/50 p-4 space-y-3">
      <h4 className="text-xs font-bold uppercase tracking-wider text-subtle">Đánh giá theo tiêu chí của AI</h4>
      {criteria.map((criterion, index) => <div key={index} className="space-y-1">
        <p className="text-sm font-semibold text-fg">{criterion.name} <span className="text-accent">{criterion.score}/5</span></p>
        {criterion.comment && <p className="text-xs md:text-sm text-fg leading-relaxed whitespace-pre-wrap">{criterion.comment}</p>}
      </div>)}
    </section>}
    {code && <section className="rounded-2xl border border-line bg-raised/50 p-4 space-y-2">
      <h4 className="text-xs font-bold uppercase tracking-wider text-subtle">Minh chứng mã nguồn</h4>
      <pre className="overflow-x-auto whitespace-pre-wrap text-xs text-fg"><code>{code}</code></pre>
    </section>}
    {!hasContent && <p role="status" className="rounded-2xl border border-line bg-bg p-4 text-xs md:text-sm text-muted">
      {error || 'Chưa có nội dung feedback AI cho câu trả lời này. Vui lòng liên hệ giảng viên để kiểm tra.'}
    </p>}
  </div>;
}
