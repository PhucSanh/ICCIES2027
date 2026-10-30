# Xử lý năm nhận xét — 30/10/2026

## 1. Ethics placeholder

Đã thay “Author confirmation required” bằng mô tả sự việc được tác giả xác nhận: mục đích nghiên cứu thông báo công khai trước sinh viên và giảng viên, mentor phối hợp xin vào lớp, tham gia tự nguyện, từ chối không có hậu quả. Không tự suy sự cho phép vào lớp thành phê duyệt/miễn xét duyệt đạo đức chính thức. Chưa xác minh quy trình cụ thể của FPT, nên không khẳng định một loại giấy bắt buộc hoặc thủ tục đã hoàn tất. Bản thảo không nhận đã có quyết định xét duyệt hay consent record riêng khi chưa được cung cấp.

Đây là hoàn thiện cách báo cáo trung thực, không phải tự cấp chứng nhận ethics. Tác giả/mentor cần xác định quy trình áp dụng tại trường trước khi tuyên bố institutional approval/exemption.

## 2. Supplement

Đã tạo `supplement/` và gói ZIP để tác giả xem/đính kèm phù hợp quy định venue. Có bảng hỏi tiếng Việt từ snapshot, trình tự/UI, mã và kết quả aggregate cũ, full pipeline dùng workbook hạn chế, thống kê đủ theo 28 repository và script NumPy chạy độc lập cho RQ3/90 contrast. Không có student IDs, câu trả lời, code repository sinh viên, reply hay credentials.

Đã chạy aggregate-only reproduction ở đường dẫn tách biệt: JSON kết quả byte-identical. Đối chiếu độc lập workbook bằng student-dummy OLS và kiểm tra toàn bộ 90 paired means, 15 item means/endorsements: sai lệch tối đa 1.4211e-14. Bốn bootstrap draws được đối chiếu thêm bằng weighted student-dummy OLS.

Không nhận toàn bộ kết quả cũ có thể tái sinh từ aggregate mới: một số mô hình/CI cũ cần workbook hạn chế và RNG sequence gốc. Supplement chưa được công khai/đăng tải ra ngoài và cần disclosure review trước chia sẻ.

## 3. RQ3

Acceptance là outcome trực tiếp; AAI thứ cấp. Cùng 5.000 repository draws, seed 20261030:

- Acceptance: b_raw=0.03437, CI95% [-0.17985, 0.25720].
- AAI: b_raw=0.07235, CI95% [-0.02483, 0.18739].
- Cả 5.000 mô hình đủ hạng; 26 sinh viên có cả hai context thuộc 12 repository.

Abstract, methods, results và bảng RQ3 đã đồng bộ. Không suy tương đương hoặc causal context effect.

## 4. Trình tự và UI

Trình tự thu thập được tác giả xác nhận: viết và nộp cả bốn câu → xem feedback AI → rating Likert. Supplement S2 đối chiếu current frontend source: review question/answer/feedback, labelled 1–5 ratings, optional reply, previous/next và completed survey read-only. HEAD frontend ngày 27/10, sau ngày thu thập 20–26/10: không trình bày thành deployment lịch sử đã xác minh. Chưa có screenshot/log lịch sử; không dựng screenshot giả hoặc nhận đã xác minh reading time/carryover.

## 5. Actionability và multiplicity

Ghi rõ contrast được làm nổi bật sau khi xem profile, mang tính thăm dò. Giữ CI95% unadjusted cũ [0.16,0.57], bổ sung family 15 item × 6 cặp = 90 two-sided contrasts (gồm Rejection chưa đảo dấu). Dùng centred bootstrap-standardised maximum để tạo approximate simultaneous 95% bands; fixed bootstrap SD, không nested studentisation. Cặp Sandwich–Explainable: difference 0.37209, simultaneous band [0.01928,0.72490].

Không gọi đây là confirmatory result hoặc exact family-wise coverage; chỉ có 28 repository, các quyết định phân tích khác ngoài family này chưa được điều chỉnh. All 90 contrasts và cả sáu Actionability contrasts được công bố trong supplement.

## Bố cục

Giữ template, font và lề. Chuyển construct-profile figure sang Supplement S4 để giữ bản chính 15 trang; không bỏ kết quả khỏi gói kiểm tra.

## Xác nhận bổ sung của tác giả về consent và bảo mật

Tác giả đã xác nhận rõ: sinh viên được thông báo đầy đủ về mục đích dùng dữ liệu, đồng ý tham gia để đóng góp nghiên cứu; không bị ép buộc, từ chối không gây bất lợi. Email được ẩn khỏi tài liệu chia sẻ; MSSV không công khai và chỉ có thể dùng cho việc kiểm tra minh bạch bởi hội đồng theo quyền truy cập phù hợp. Ethics statement đã cập nhật các thông tin này, không còn ghi rằng consent chưa được mô tả. Không suy một quy trình đồng ý tham gia đã được xác nhận thành một quyết định institutional approval/exemption có tên, ngày hoặc mã chưa được cung cấp.

## Kiểm tra cuối

Bản PDF cuối: 15 trang, đã đồng bộ nguồn; không có undefined citation/reference, missing character, overfull box hoặc BibTeX warning. Đã render/xem toàn bộ các trang qua contact sheets và kiểm tra riêng procedure, RQ3 và ethics ở kích thước đọc được; trang ethics được render lại sau xác nhận bổ sung. `git diff --check` đạt. ZIP 40 file đã kiểm tra CRC và SHA-256 manifest, không chứa workbook, `.env`, credentials hoặc dữ liệu định danh. Supplement chỉ chuẩn bị cục bộ, chưa đăng tải/nộp ra ngoài. Không có screenshot/UI lịch sử hoặc quyết định institutional ethics được dựng thêm.
