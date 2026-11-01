# Kiểm thử

## Tự động

`npm test`: Topic wildcard, reserved Topic, dữ liệu lỗi, mã phòng và CSV formula injection.
`node --check assets/app.js`: cú pháp JavaScript.
`python -m py_compile agent/agent.py`: cú pháp Python.

## Tích hợp cần chạy với Broker truy cập được

1. Hai trình duyệt, cùng Broker/phòng: gửi PC01 → bên còn lại nhận.
2. Hai phòng khác nhau: không nhận chéo qua UI.
3. Subscribe chính xác, +, #; unsubscribe; kiểm tra nhật ký.
4. Retained: gửi, subscribe từ tab mới, xóa retained, kiểm tra tab mới không nhận giá trị cũ.
5. Gửi payload HTML: hiển thị text, không chạy script.
6. JSON lỗi và CPU ngoài [0,100]: không thêm thẻ thiết bị.
7. Dừng thiết bị; đóng tab đột ngột; chờ >15 giây.
8. Agent thật; Ctrl+C; ngắt mạng; khôi phục mạng; Agent tự kết nối lại.
9. Broker không truy cập được: trạng thái lỗi/kết nối lại, không báo kết nối thành công.
10. Xuất CSV; reload; lịch sử vẫn còn và trạng thái cũ không Online.
11. Mobile: thao tác tab và slider, không tràn ngang.
12. Chạy trên GitHub Pages thực tế sau push; CDN và WSS phải truy cập được.

Kiểm tra tự động không thay thế kiểm thử mạng. Ghi riêng các mục đã chạy và chưa chạy trong báo cáo nghiệm thu.

## Trạng thái kiểm tra khi bàn giao

- Đạt: 5 kiểm thử logic Node, kiểm tra cú pháp JavaScript và Python.
- Chưa chạy được kiểm thử trình duyệt: runtime thiếu Chromium.
- Chưa xác minh MQTT WSS đầu cuối: endpoint Broker không truy cập được từ môi trường tạo project.
- Chưa triển khai GitHub Pages; cần người dùng push và bật Pages.
