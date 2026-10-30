> Cập nhật 30/10/2026: xem [REVISION_RESPONSE_20261030.md](REVISION_RESPONSE_20261030.md) cho vòng sửa sau phản biện và đính chính phạm vi audit nguồn phản hồi. Những mô tả phiên bản cũ bên dưới là lịch sử; không thay thế thông tin mới.

# Bản sửa theo review ICCIES 2027

Ngày: 29/10/2026. Branch của vòng sửa trước: `quanghieu`.

**Cập nhật `codex-review`:** Xem `SELF_REVIEW.md` cho vòng sửa và kiểm tra mới nhất. Bảng item và hình cấu hình hiện dùng CI theo repository; hồi quy thêm biến cấu hình; RQ3 dùng student fixed effects; thư mục tham khảo có 36 mục. Những con số CI/mô hình mô tả bên dưới là lịch sử vòng sửa trước nếu khác bản hiện tại.

## Đã sửa

- Đổi cách mô tả từ bốn format thuần trình bày sang bốn cấu hình phản hồi, vì chúng khác cả nội dung và pipeline mô hình.
- Viết lại Abstract, contributions, Discussion và Conclusion; giới hạn kết luận ở cảm nhận, tránh suy luận nhân quả, correctness khách quan hay learning gains.
- Bổ sung tuyển người tham gia theo thông tin tác giả xác nhận: đến lớp mời sinh viên dùng công tâm để ôn tập cho câu hỏi trước hội đồng bảo vệ.
- Gọi AAI là chỉ số tổng hợp khám phá; công khai quyết định loại Rejection dựa trên kiểm tra dữ liệu; không suy ra dimensionality từ alpha/omega.
- Thay bảng mô hình acceptance bằng hồi quy fixed effects theo sinh viên, tách motivation và psychological safety; CI bootstrap theo repository.
- Bổ sung CI theo repository cho AAI và sensitivity analysis sáu chênh lệch cấu hình. Kiểm tra xác nhận sinh viên và câu hỏi đều nằm trong một repository.
- Giữ RQ3 ở mức khám phá do router phụ thuộc method count và context dùng cho cả câu hỏi lẫn đánh giá; bỏ suy luận tương đương và p-value Mann–Whitney trên từng dòng.
- Bỏ p-value tương quan trên từng dòng, kết luận về self-serving bias, và số liệu token/cost chưa có log tái tạo.
- Không dùng straight-lining để kết luận chắc chắn người tham gia thiếu chú ý.
- Chuyển free-text sang minh họa khám phá, bỏ tỷ lệ coding chưa có quy trình tái lập và phân biệt phản ánh của sinh viên với lỗi đã được chuyên gia xác minh.
- Thay “ground-truth context” bằng “reference context”. Bỏ tên hiển thị chưa xác minh của mô hình sinh câu hỏi, chờ API model ID thực tế.

## Đính chính review ban đầu về Researching

Review nhận xét metadata model trống dựa trên bộ đọc cũ. Khi nhận Excel gốc, xác định trường nằm ở `researching.models_involved`, không phải `models_involved` cấp ngoài. Cả 86 bản ghi Researching đều liệt kê:

- DeepSeek-V3 (Code Inspector).
- Groq-GPT-OSS-120B (Pedagogical Synthesizer).

Đã sửa `analysis/run_analysis.py` và trường metadata trong `analysis/results.json`. Không thay đổi số liệu khảo sát cũ. Metadata export không thay thế log provider độc lập.

## Kiểm tra độ tuân thủ cấu hình

Tất cả nhãn `feedback_type` trong JSON khớp nhãn cấu hình trên Excel. Tuy nhiên, một payload Rubric chứa next steps và thiếu criteria; 85 payload Rubric còn lại có criteria. Bản sửa báo cáo sai lệch, giữ phân tích theo nhãn được gán và thêm sensitivity check loại block sinh viên liên quan. Không đổi nhãn quan sát để làm kết quả đẹp hơn.

## Nguồn dữ liệu đã kiểm tra

`/home/qhius/Downloads/PACE-BaiDaNop-DaDanhGiaAI-2026-10-29 (5).xlsx`

- Sheet `Chi tiết khảo sát sinh viên`: 344 phản hồi, 86 sinh viên, 28 repository, 190 câu hỏi.
- Bốn cấu hình: mỗi cấu hình 86 phản hồi.
- Context: 280 Graph, 64 Codebase.
- 64 phản hồi straight-lined.
- File nguồn giữ nguyên, không đưa vào Git; file audit chỉ chứa kết quả tổng hợp và SHA-256.

## Kiểm tra thống kê đã chạy

1. Chạy lại toàn bộ `run_analysis.py` trong thư mục tạm bằng Excel gốc; so sánh đệ quy mọi trường số trong kết quả cũ và mới với ngưỡng tuyệt đối `1e-7`: **không có trường số thay đổi vượt ngưỡng**. Vì vậy giữ số liệu/figure cũ, chỉ sửa metadata sai.
2. `analysis/check_export.py`: đọc nguồn độc lập, xác nhận từng sinh viên có đúng một phản hồi mỗi cấu hình, ratings 1–5, JSON hợp lệ, không có marker fixture và tính lồng nhóm phù hợp.
3. Trung bình từng item và thống kê Friedman AAI tái tính khớp hoàn toàn kết quả lưu sẵn.
4. Repository bootstrap: 5.000 lần, seed 20261029; giữ mọi sinh viên và câu hỏi trong repository được lấy mẫu.
5. AAI = 4.0716, CI95% repository = [3.9035, 4.2291]. Cả sáu CI90% chênh lệch AAI vẫn trong biên khám phá ±0.25; không áp dụng kết luận này cho từng item.
6. Kiểm tra độc lập hệ số hồi quy bằng statsmodels với biến giả sinh viên: chênh lệch lớn nhất so với phép demean là `1.15e-14`.
7. Hồi quy within-student mới dùng motivation và psychological safety riêng; mỗi outcome có đủ 5.000 bootstrap fits không thiếu hạng. Các CI là khám phá, chưa điều chỉnh đa kiểm định.

Kết quả bổ sung: `analysis/source_audit.json`. Không diễn giải bootstrap CI như một thử nghiệm ngẫu nhiên hóa độc lập next steps hoặc context.

## Còn cần tác giả hoàn thiện trước khi nộp

- Xác nhận tự nguyện, ảnh hưởng điểm, research consent, institutional review/exemption và bảo vệ dữ liệu. Việc sinh viên đồng ý dùng hệ thống trong lớp chưa tự xác nhận research consent.
- Xác minh model ID/version, prompt và routing implementation từ mã/log; audit provider và token usage nếu muốn phục hồi kết luận ensemble/cost.
- Tài liệu/đường dẫn công trình PACE trước đó nếu có; phân định phần đóng góp mới và overlap.
- Ví dụ xuyên suốt bốn cấu hình trên cùng một input, ghi rõ nếu tạo thêm sau nghiên cứu; không dựng ví dụ rồi trình bày thành quan sát thực nghiệm.
- Đánh giá correctness/grounding bởi chuyên gia nếu có nguồn lực. Hiện bài không khẳng định đã có kiểm tra này.
- Làm rõ chính sách AI-generated text với hội nghị, sau đó tác giả rà soát và chịu trách nhiệm bản nộp.
- Bản PDF đã biên dịch thành công bằng Tectonic 0.17.0: **15 trang**, không có overfull box, citation/reference chưa xác định hoặc missing character trong log cuối. Đã render và kiểm tra trực quan toàn bộ 15 trang; bảng mô hình mới và phần ethics được kiểm tra riêng. PDF hiện lưu tại `main.pdf`.
