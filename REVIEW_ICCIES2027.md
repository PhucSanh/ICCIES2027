# Nhận xét bản thảo nộp ICCIES 2027

> **Cập nhật sau khi nhận Excel gốc:** Nhận xét mục 3.B về metadata trống bắt nguồn từ bộ đọc JSON sai cấp. Trường đúng là `researching.models_involved`; cả 86 phản hồi liệt kê hai mô hình. Đã đính chính trong bản sửa và `REVISION_NOTES.md`. Excel gốc đã được đối chiếu và phân tích bổ sung; giới hạn “thiếu Excel” dưới đây chỉ mô tả thời điểm review ban đầu.

**Ngày đánh giá:** 29/10/2026  
**Bài báo:** Do Students Agree with LLM Feedback on Their Own Code? A Within-Subject Study of Four Feedback Formats in Software Project Courses

## Kết luận chung

Bài có chất liệu để nộp ICCIES 2027, nhưng bản hiện tại cần sửa lớn trước khi nộp. Rủi ro chính nằm ở thiết kế so sánh và cách diễn giải kết quả, hơn là tiếng Anh.

Nếu phản biện bản hiện tại, tôi nghiêng về **weak reject**, chủ yếu vì chưa tách được các yếu tố trong điều kiện so sánh, một số kết luận quá mạnh và phần ethics chưa hoàn tất. Đây là đánh giá học thuật, không phải dự đoán quyết định của hội nghị.

## Phạm vi kiểm tra và giới hạn

Đã đọc bản thảo `main.tex`, mã phân tích `analysis/run_analysis.py`, kết quả lưu sẵn `analysis/results.json`, danh mục `refs.bib`; kiểm tra một số trang của `main.pdf`.

**Chưa chạy lại được thống kê vì thư mục thiếu Excel đầu vào. Chưa xác minh độc lập toàn bộ tài liệu tham khảo.** Những số liệu thống kê được nhận xét dưới đây dựa trên bản thảo, mã và kết quả lưu sẵn; chưa phải kết quả tái lập độc lập.

## 1. Mức độ phù hợp với ICCIES 2027

Bài phù hợp về chủ đề. Session **AI-Driven Intelligent Digital Education — AIDE** bao gồm automated feedback, question generation, programming learning và technology acceptance. Tuy nhiên, session yêu cầu đóng góp rõ về phương pháp, hệ thống hoặc đánh giá; bài cần làm nổi bật đóng góp của PACE thay vì chỉ trình bày khảo sát hài lòng.

- Session AIDE: https://iccies.tdtu.edu.vn/2027/ai-driven-intelligent-digital-education/
- Hướng dẫn nộp bài: https://iccies.tdtu.edu.vn/2027/how-to-submit/
- Trang hội nghị: https://iccies.tdtu.edu.vn/2027/

PDF hiện có **15 trang**, nằm trong giới hạn **12–15 trang**, và dùng lớp `llncs`, phù hợp yêu cầu định dạng cơ bản. Đây chưa phải xác nhận tuân thủ toàn bộ yêu cầu template.

## 2. Những điểm đáng giữ

- **Bối cảnh thực tế có giá trị:** phản hồi cho câu trả lời về repository của chính nhóm sinh viên, gần hoạt động đánh giá hiểu biết trong môn dự án.
- **Thiết kế trong cùng người tham gia hợp lý:** 86 sinh viên đều trải nghiệm bốn điều kiện, giúp giảm ảnh hưởng của khác biệt cá nhân.
- **Phân tích vượt mức khảo sát mô tả:** có cluster bootstrap, Friedman, effect size, mixed model và equivalence testing.
- **Kết quả đáng bàn:** sinh viên đánh giá phản hồi tích cực nhưng động lực và ý định tiếp tục sử dụng thấp hơn. Đây là câu chuyện nghiên cứu tốt hơn việc chỉ báo cáo điểm trung bình trên 4.

## 3. Những vấn đề cần sửa trước khi nộp

### A. So sánh “format” đang thay đổi nhiều thứ cùng lúc

**Mức ưu tiên: rất cao.**

**Vị trí:** `main.tex`, dòng 143–150, phần Feedback Generation.

Bài viết rằng bốn dạng chỉ khác JSON schema. Nhưng Researching còn thay đổi:

- Số mô hình và quy trình sinh phản hồi.
- Thành phần nội dung.
- Độ dài và lượng token.

Sandwich và Researching có next steps; hai dạng còn lại không có. Vì vậy, dữ liệu cho phép so sánh **bốn cấu hình phản hồi hoàn chỉnh**, chưa tách riêng được tác động của cách trình bày hay next steps.

**Đề xuất sửa:**

1. Mô tả đúng các điều kiện, loại bỏ khẳng định rằng chúng chỉ khác JSON schema.
2. Hạ kết luận “next steps tạo ra tác động” thành “các cấu hình có next steps được đánh giá actionable hơn”.
3. Nêu rõ muốn chứng minh cơ chế cần thí nghiệm riêng, giữ các yếu tố khác ổn định và chỉ thay đổi next steps.

### B. Khẳng định 86/86 Researching chạy đủ ensemble chưa được dữ liệu hiện có xác nhận

**Mức ưu tiên: rất cao.**

**Vị trí:** `main.tex`, dòng 150; `analysis/results.json`, trường `screening.researching_models`.

Bài khẳng định toàn bộ 86 Researching instances được tạo bởi full ensemble. Tuy nhiên, kết quả lưu sẵn ghi:

```json
{"researching_models": {"": 86}}
```

Điều này **không chứng minh hệ thống chạy sai**. Nó cho thấy metadata mà script hiện tại đọc chưa xác nhận được khẳng định.

**Đề xuất sửa:**

- Đối chiếu log provider, trạng thái fallback và schema export.
- Kiểm tra trường `models_involved` có nằm đúng vị trí mà script đang đọc hay không.
- Chỉ giữ khẳng định “86/86 full ensemble” khi có bằng chứng tương ứng.
- Bổ sung đường dẫn tái tạo phần token/cost: script hiện tại chưa tái tạo các số liệu này trong bài.

### C. Phụ thuộc dữ liệu chưa được xử lý đầy đủ

**Mức ưu tiên: cao.**

**Vị trí:** `main.tex`, phần Analysis; `analysis/run_analysis.py`, các phân tích Spearman và Mann–Whitney.

Dữ liệu gồm 344 phản hồi từ 86 sinh viên thuộc 28 repository, với câu hỏi dùng chung. Random intercept theo sinh viên là bước tốt, nhưng chưa xử lý hết cấu trúc nhóm/câu hỏi.

Các kiểm định Spearman và Mann–Whitney chạy trên từng dòng, không điều chỉnh phụ thuộc trong sinh viên. Do đó, p-value của các phân tích này cần được xem xét lại.

**Đề xuất sửa:**

- Ưu tiên sensitivity analysis có xét repository và câu hỏi khi dữ liệu cho phép.
- Dùng suy luận theo cụm cho các phân tích phụ.
- Không nhất thiết đưa mọi random effect vào một mô hình; lựa chọn mô hình theo cấu trúc dữ liệu, khả năng nhận diện và độ ổn định.
- Nêu rõ đơn vị quan sát, đơn vị ngẫu nhiên hóa và cấu trúc phụ thuộc.

### D. RQ3 bị nhiễu bởi độ phức tạp và đang kết luận quá mạnh

**Mức ưu tiên: cao.**

**Vị trí:** `main.tex`, dòng 138 và dòng 350.

Router chọn graph khi có hơn 10 methods, raw code khi ít hơn. Vì vậy, hai nhóm khác nhau có hệ thống về độ phức tạp. Context còn được dùng cho cả sinh câu hỏi và đánh giá.

`p = .22` không đủ để kết luận raw code và graph tương đương. Câu “rules out … any meaningful advantage” cần hạ xuống.

**Đề xuất sửa:**

- Xem RQ3 là phân tích khám phá.
- Báo cáo ước lượng và confidence interval, nói rõ chưa cô lập được tác động của context type.
- Phân biệt không phát hiện khác biệt với chứng minh tương đương.
- Nếu có thông tin độ phức tạp, xem xét phân tích điều chỉnh và kiểm tra mức độ chồng lấp giữa hai nhóm; việc điều chỉnh cũng không tự biến thiết kế thành thử nghiệm ngẫu nhiên.

### E. Thang đo chưa đủ cơ sở cho một agreement index thống nhất

**Mức ưu tiên: cao.**

**Vị trí:** `main.tex`, phần Instrument, Scores, Reliability and Data Quality.

AAI gộp accuracy, trust, motivation, psychological safety và intention. Alpha/omega cao chưa chứng minh tất cả đo cùng một khái niệm. Affect có alpha `.56`, nhưng vẫn được dùng làm predictor để diễn giải willingness.

Bỏ Rejection sau khi quan sát dữ liệu là quyết định cần trình bày minh bạch.

**Đề xuất sửa:**

- Gọi AAI là chỉ số tổng hợp mang tính khám phá.
- Ưu tiên phân tích Acceptance riêng.
- Thử tách motivation và psychological safety trong sensitivity analysis.
- Nêu rõ việc loại Rejection được quyết định sau khi kiểm tra dữ liệu nếu đúng thực tế.
- Không gọi những người còn lại là “attentive respondents” chỉ vì họ không straight-line. Straight-lining là dấu hiệu cần kiểm tra, chưa đủ để phân loại chắc chắn mức độ chú ý.

### F. Một số câu vượt quá bằng chứng

**Mức ưu tiên: cao.**

| Cách viết hiện tại | Vấn đề | Hướng sửa |
|---|---|---|
| “What drives acceptance” | Dữ liệu đồng thời chỉ hỗ trợ liên hệ | Dùng cách diễn đạt về association/correlates |
| “Utility and trust matter more than correctness” | Đo perceived quality, chưa đo correctness khách quan | Giữ rõ từ “perceived”; tránh suy luận về độ đúng thực tế |
| “Length does not explain the pattern” | Covariate không có ý nghĩa thống kê chưa loại trừ vai trò độ dài | Nói mô hình điều chỉnh chưa cung cấp bằng chứng rõ về liên hệ với độ dài |
| “Acceptance itself did not vary” | Không có ý nghĩa thống kê không chứng minh không có khác biệt | Nói chưa phát hiện khác biệt |
| “No pair … differed by more than ±0.25” | Cần giới hạn ở AAI; actionability chênh khoảng 0.38 | Nêu rõ outcome và loại ước lượng/CI đang được nói tới |

Equivalence testing là điểm mạnh, nhưng cần giải thích vì sao **±0.25** là ngưỡng có ý nghĩa thực tế. Không mở rộng kết luận tương đương của AAI sang mọi thành phần.

### G. Ethics và khả năng tái lập còn thiếu thông tin

**Mức ưu tiên: rất cao.**

**Vị trí:** `main.tex`, dòng 159 và dòng 407.

Phần Context and Participants còn TODO về tuyển người tham gia, tự nguyện, điểm số và consent.

**Cần bổ sung đúng thực tế:**

- Cách tuyển và tỷ lệ tham gia.
- Quan hệ giữa khảo sát với chấm điểm.
- Quy trình consent; phê duyệt hoặc miễn xét duyệt nếu có.
- Bảo vệ thông tin sinh viên và mã nguồn repository.
- Phạm vi dữ liệu và tài liệu có thể chia sẻ để tái lập.

Không tự điền một tuyên bố ethics chung chung nếu chưa có căn cứ.

## 4. Hai bổ sung có thể nâng chất lượng bài rõ nhất

### Một ví dụ xuyên suốt

Dùng cùng câu hỏi, câu trả lời và context để minh họa bốn đầu ra. Điều này giúp reviewer hiểu các điều kiện khác nhau thế nào. Nếu sinh thêm sau nghiên cứu, phải ghi rõ đó là ví dụ minh họa bổ sung.

### Đánh giá chuyên gia trên một mẫu phản hồi

Nếu còn nguồn lực, lấy mẫu theo format và context để chuyên gia đánh giá correctness và grounding. Bài hiện đo cảm nhận tốt hơn đo độ đúng; kiểm tra độc lập sẽ giúp reviewer đánh giá ý nghĩa của mức agreement cao.

Đây là đề xuất nâng chất lượng, không phải khẳng định mọi nghiên cứu về cảm nhận đều bắt buộc có đánh giá chuyên gia.

## 5. Thứ tự sửa đề xuất

1. **Xác minh log và nguồn số liệu:** full ensemble, fallback, token/cost và model identifiers từ log thực tế.
2. **Hoàn thiện ethics:** recruitment, voluntariness, grading, consent và bảo vệ dữ liệu.
3. **Sửa cách gọi điều kiện và giới hạn kết luận:** bốn cấu hình phản hồi; association thay cho causation; RQ3 mang tính khám phá.
4. **Chạy sensitivity analysis:** cấu trúc cụm, Acceptance riêng, motivation và psychological safety riêng; xem lại các p-value coi từng dòng là độc lập.
5. **Hoàn thiện cách trình bày:** rút abstract, thêm ví dụ, làm rõ ngưỡng equivalence và đóng góp mới so với công trình PACE trước đó nếu có.

## 6. Lưu ý về chính sách AI của hội nghị

Trang hướng dẫn ICCIES 2027 hiện ghi cấm bài chứa văn bản do AI tạo, dù đoạn tiếp theo vẫn nhắc năm 2026. Nhóm cần làm rõ phạm vi chính sách với ban tổ chức trước khi dùng văn bản AI soạn trong bản nộp.

Nguồn: https://iccies.tdtu.edu.vn/2027/how-to-submit/

Bản nhận xét này là tài liệu hỗ trợ rà soát, không phải văn bản để chép nguyên vào bài báo.
