# Kế hoạch thực hiện bản 1.0

Phạm vi: website tĩnh cho GitHub Pages, MQTT thật qua WSS, MQTT Lab, phòng chung, Dashboard, Agent. Người dùng đã yêu cầu bắt đầu triển khai theo hướng đã thống nhất.

- [x] Test quy tắc Topic, dữ liệu và CSV trước khi triển khai core.
- [x] Giao diện responsive, form kết nối và trạng thái lỗi.
- [x] Subscribe/Publish, QoS, retained, phòng theo prefix.
- [x] Thiết bị thử, Dashboard, timeout, biểu đồ, CSV, localStorage.
- [x] Agent Python lấy số đo thật và MQTT TLS, Last Will, reconnect.
- [x] README, kiến trúc, checklist tích hợp, GitHub checks.
- [ ] Xác minh mạng đầu cuối với Broker công cộng trên máy người dùng.
- [ ] Push repository và bật GitHub Pages bằng tài khoản người dùng.

Rủi ro cần kiểm tra: mất mạng; trùng mã máy; dữ liệu cũ; message không hợp lệ; Broker công cộng không có bảo mật phòng. Không có database tập trung hoặc tài khoản ở phiên bản này.
