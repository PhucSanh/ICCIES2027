# S2. Procedure and interface evidence

## Collection sequence: author-confirmed on 30 October 2026

The research purpose was announced in front of the students and the course instructor. Students wrote and submitted all four answers, then viewed AI feedback, then completed the Likert ratings. No interview or historical event-log audit was conducted to independently establish viewing time, reading completeness, or participant-level navigation.

## Current implementation inspected; not a historical deployment screenshot

Frontend HEAD: `cf7e40e36ad4dec02a9b3ed2c3b27e7427e0f435` (27 October 2026), after the 20–26 October collection interval. Working tree was clean when inspected. This is supporting implementation evidence, not proof of the exact deployed revision.

| Source file | Visible behaviour | SHA-256 |
|---|---|---|
| `src/app/test/page.tsx` | Join → select questions → write answers → submit/generate feedback → survey. Standalone feedback-results step is commented out in this revision. | `638c17d896412486dabb196643c402397da3b2c3c9bd2a9d95fd4535cb0d2cd5` |
| `src/app/test/components/step-3-answer-questions.tsx` | Validates every selected answer and submits the four-answer array together. | `59de117ef1be678c574577e086424422b23beae8b9189de9db29b2903fdd3147` |
| `src/app/test/components/step-4-loading-ai.tsx` | Calls submission with the answer array, then enters the survey. | `8db38d243d0f906dbf540d668b987b4382c923d83e2ed0e46937c88d080938db` |
| `src/app/test/components/step-survey-rubric.tsx` | A per-question review modal precedes the rating panel; previous/next navigation, 1–5 labelled stars, optional text reply; final submission requires every criterion. Existing completed surveys are read-only in this UI. | `af0e74e0c5d68948ad1dc888f33141e52227cf2ac0656dddb29bae084eb1126d` |
| `src/app/test/components/survey-question-review.tsx` | Review modal shows question, saved answer, feedback and button “Bắt đầu đánh giá” (Start rating). No minimum dwell-time check is implemented in this component. | `5cf53f116a9575ae299075df23a6be281b72daf69a5878f64e4332b00df44678` |
| `src/features/student-assessment/components/survey-ai-feedback.tsx` | Renders nonempty positives, criticism, next steps, logic, Researching fields, criterion scores and code evidence as separate sections. | `d8f4496ea4bdccdaf88680857866728b639552076595be1665501b7fa235aa00` |

No historical screenshots, provider request logs, immutable deployment mapping or verified carryover/timing data are supplied. Do not treat this implementation inspection as an executed user study or infer that participants read every feedback section.

The interface uses per-question Likert labels: 1 Hoàn toàn không đồng ý; 2 Không đồng ý; 3 Trung lập / Phân vân; 4 Đồng ý; 5 Hoàn toàn đồng ý.

The six inspected source files are included verbatim under `ui_source/` at their relative paths. They are inspection excerpts, not a standalone runnable frontend; omitted imports, build configuration and runtime/API dependencies are not supplied. No `.env`, credential files or individual survey content are included.

## Participant information and confidentiality: author-confirmed

The research purpose and intended use of responses were explained publicly to students with the course instructor present. Students agreed voluntarily to contribute research data; refusal had no disadvantage. Personal email addresses and student identifiers are excluded from shared artifacts. Committee-level identity verification, if justified and authorised, would use controlled access rather than public release. No formal institutional ethics decision is established by these statements.
