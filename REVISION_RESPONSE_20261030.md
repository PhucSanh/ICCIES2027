# Đối chiếu review và bản sửa — 30/10/2026

Đã đọc chat `01a18a4b-3f14-7810-98c9-d63d943a94e8` bằng read_thread và các báo cáo trong `/home/qhius/research-paper-review/reviews/`. Bản gốc trước vòng sửa được giữ tại `_archive/pre_revision_20261030/` (không đưa vào Git). Không đổi dữ liệu, chạy ghi DB, gọi model sinh phản hồi hay tạo câu trả lời khảo sát.

## Thay đổi trong bài

| Ý kiến review | Xử lý |
|---|---|
| R1–R4: agreement không đồng nghĩa composite đa miền | Abstract, phương pháp, RQ2 và Conclusion đặt Acceptance làm outcome trực tiếp; AAI là tổng hợp phụ. Công khai đổi trọng tâm trong vòng sửa, không nhận là preregistered. |
| R2–R3: rank p chưa xử lý repository | Bảng RQ2 thay bằng đủ sáu contrast Acceptance CI95% và AAI CI90% theo repository. Đưa Friedman/mixed model về kiểm tra phụ, bỏ pairwise rank p khỏi đoạn kết luận chính. |
| R1–R3: thiếu sensitivity margin | Từ sáu interval lưu sẵn: ±0.25 chứa 6/6, ±0.20 chứa 5/6, ±0.10 chứa 1/6. Không gọi ngưỡng nào là đã được hiệu chuẩn giáo dục. |
| R1/R4: novelty chưa rõ | Thêm đoạn đối chiếu trực tiếp QLC 2021, Zhang 2024 và Lehtinen 2024. Định vị contribution ở task, bối cảnh repository nhóm và evaluation; không tuyên bố thuật toán mới. |
| R2/R4: chưa hiểu khác biệt bundle | Thêm giải thích xuyên suốt cùng câu hỏi contract-balance cho bốn content requirements, ghi rõ đây là sơ đồ yêu cầu, không phải bốn output quan sát cùng input. Hình không còn ngụ ý tất cả cấu hình chỉ đi qua một model. |
| R3: bootstrap/measurement khó kiểm tra | Nêu trọng số từng item, pooled repeated-instance reliability, standardisation giữ cố định và cách lặp complete blocks khi bootstrap repository. |
| R1/R4: motivation bị gọi lẫn affect | Đổi tên item trong bảng thành Motivation; Affect vẫn là tên nhóm hai item. Chú thích hình giải thích nhãn export. |
| R1–R4: supplement nói có nhưng không kèm | Sửa availability: scripts và aggregate đang ở workspace, chưa phát hành supplement cho reviewer. Không bịa link hoặc tuyên bố công khai. |
| Recruitment/voluntariness | Theo xác nhận mới của tác giả: chọn lớp ngẫu nhiên, cá nhân tự nguyện, có người không điền; mentor giữ quyền DB. Không suy ra sampling frame/response rate/consent/ethics approval từ các thông tin này. |
| Qualitative evidence | Giữ số reply, không dùng nội dung chưa truy vết làm chứng cứ uptake hoặc lỗi kỹ thuật; không bịa quotes/coding. |

## Đính chính cách diễn giải audit

Tác giả xác nhận tất cả 344 lượt đánh giá do sinh viên thật tự nguyện điền; chỉ mentor giữ quyền truy cập DB. Đây là **344 lượt từ 86 sinh viên**, mỗi sinh viên bốn cấu hình, theo cấu trúc export hiện có.

File `analysis/data_provenance_audit.json` và script đã tồn tại trước vòng sửa này. Đã chạy lại script ra `/tmp/pace-provenance-verified.json`: kết quả số học khớp file có sẵn. Script so sánh workbook với file snapshot/review cục bộ, KHÔNG kết nối hoặc xác thực DB production. Sự trùng khớp 144 record/2.160 điểm/144 reply và receipt cục bộ không tự xác định môi trường DB, người ghi, quyền truy cập, hoặc nguồn gốc phản hồi trước đó.

Vì vậy, kết luận trước của trợ lý rằng đã xác nhận khảo sát bị ghi đè hoặc phản hồi là giả vượt quá phạm vi xác minh. Bản sửa không đưa kết luận đó vào bài. Đồng thời, không xóa/sửa bằng chứng cục bộ để tạo ra sự nhất quán giả. Nguồn phản hồi được trình bày theo xác nhận tác giả; kiểm toán độc lập DB chưa được thực hiện. Việc đối chiếu lịch sử export/snapshot với mentor, nếu cần, là công việc xác minh riêng; không yêu cầu tiết lộ key hoặc cấp quyền DB cho trợ lý.

## Chưa thể hoàn thành từ dữ liệu hiện có

- Ethics/research consent, quan hệ điểm số, review/exemption, quyền gửi repository qua API: cần hồ sơ thực tế, không tự điền.
- Exact deployed model IDs, prompt/schema, thứ tự hiển thị/khả năng nộp lại, provider/fallback logs: cần artifact đúng phiên bản deployment. Chưa bịa ví dụ đầu ra hay screenshot.
- Leave-one-repository-out đã được bổ sung trên workbook hiện có; phân tích order chưa thực hiện vì thiếu timeline được xác minh. Bảng sáu cặp dùng các CI đã lưu, không nhận đã bootstrap lại trong vòng này.
- Chưa phát hành supplement/data anonymised; chưa thể xác nhận tuân thủ chính sách hội nghị hoặc hoàn tất bản nộp.

Các nhận xét review là mô phỏng học thuật, không phải quyết định hội nghị. Không gửi bài, email, công khai dữ liệu hoặc thay đổi DB.

## Kiểm tra số liệu trong vòng sửa

- Không đổi số liệu gốc hoặc tính lại kết quả từ DB. Đối chiếu đủ 12 ước lượng/interval của bảng contrast với aggregate: khớp khi làm tròn ba chữ số.
- Kiểm tra cả sáu Acceptance CI chứa zero; margin counts AAI là 6, 5, 1 ở ±0.25, ±0.20, ±0.10.
- Hai block bảng generated trong LaTeX khớp file standalone sau đổi nhãn Motivation. Hình Likert được giữ ở thư mục figures như artifact phụ; bản chính ưu tiên bảng phân bố item để tránh lặp và giữ giới hạn trang.
- `build_report.py` chưa chạy được trong runtime hiện tại vì thiếu matplotlib; không tuyên bố đã regenerate figures. Đã sửa mapping nhãn để các lần chạy đủ dependencies sau này giữ đúng tên item.
- Bổ sung Lehtinen 2024 được xác minh ở trang arXiv của tác giả (abstract/metadata), không nhận đã audit full text hoặc DOI Crossref cho nguồn DataCite này.
- Đọc độc lập workbook và pivot theo sinh viên/cấu hình: 86 complete blocks; toàn bộ 18 paired means AAI, Acceptance và Actionability khớp aggregate trong `1e-12`.
- Thêm `analysis/build_contrasts.py` chỉ cần thư viện chuẩn để tái tạo bảng sáu cặp và in sensitivity margin. Script đã chạy thành công; không truy cập DB hoặc sinh ratings.

Trang hướng dẫn hội nghị đã được kiểm tra lại ngày 30/10: vẫn ghi LNCS/LNAI và 12–15 trang; mục AI-generated text vẫn có câu cấm và đoạn tiếp theo nhắc ICCIES 2026. Không tự chứng nhận compliance cho văn bản được trợ lý sửa.

- Đối chiếu hồi quy bằng OLS với biến giả sinh viên độc lập với phép demean: sai lệch lớn nhất `4.3854e-15`. Không chạy lại bootstrap hoặc tuyên bố tái kiểm chứng CI từ đầu trong vòng này.

## Kiểm tra leave-one-repository-out bổ sung

Đã chạy `analysis/leave_one_repository_out.py` trên workbook đang dùng; kết quả aggregate ở `analysis/leave_one_repository_out.json`. Mỗi lần bỏ một repository, giữ nguyên complete blocks của các sinh viên còn lại. Không truy cập DB, không sửa ratings.

- 28 lần bỏ repository; chênh Actionability Sandwich–Explainable: 0.3415–0.4118, không đổi dấu.
- 26 sinh viên có cả hai context thuộc 12 repository; hệ số context đầy đủ 0.072349 khớp aggregate; range khi bỏ từng repository 0.0467–0.1136. Cả 28 mô hình đủ hạng.
- Range là độ nhạy của **point estimate**, không phải CI, không thay percentile bootstrap và không giải quyết confounding do router.

## PDF và kiểm tra cuối

- Tectonic 0.17.0 biên dịch bản cuối thành **15 trang**; `main.pdf` và `main.bbl` đã đồng bộ với nguồn.
- Không có citation/reference undefined, missing character, overfull box hoặc BibTeX warning trong log cuối. Poppler có font-type warning khi trích văn bản; các trang render vẫn hiển thị bình thường.
- Đã render cả 15 trang, xem contact sheets toàn bộ và xem riêng hình pipeline, bảng instrument và bảng sáu contrast ở kích thước lớn. Không thấy bảng tràn hoặc chữ chồng.
- Ba generated blocks (item, regression, paired contrasts) khớp file standalone; 37 citation keys đều có entry; `git diff --check` đạt.
- Cắt phần diễn giải trùng lặp và chuyển hình Likert (lặp bảng item) ra khỏi bản chính để giữ 15 trang; không thu nhỏ font hoặc đổi lề template.
- Bản này đã được cải thiện để tác giả rà soát, chưa tự xác nhận hoàn tất ethics, deployment logs, supplementary release hay chính sách AI của venue.
