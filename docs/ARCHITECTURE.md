# Kiến trúc bản 1.0

Browser dùng MQTT.js qua WSS; Agent dùng Paho qua WSS hoặc MQTT/TLS. Broker phân phối message. Không có Flask hoặc database server trong bản này: đây là bản GitHub Pages có MQTT thật và lưu lịch sử cục bộ.

## Topic và dữ liệu

Prefix `pcmon/v1/<room>`.
- `/devices/<device>/metrics`: JSON {cpu,ram,disk,hostname,source,timestamp}; QoS 1, không retained.
- `/devices/<device>/status`: JSON {state:"online"|"offline",source}; Agent QoS 1 retained, Last Will offline.
- `/lab/<topic>`: payload tự do dưới 16 KB; QoS và retained theo lựa chọn.
- `/presence/<session>`: Last Will của trình duyệt, không ánh xạ thành Last Will của từng máy thử.

Phòng 6–40 ký tự chữ/số/_/-. Mã thiết bị 1–40 ký tự cùng quy tắc. Các chỉ số phải là number hữu hạn trong [0,100].

## Online và phục hồi

Số đo mới đánh dấu Online; status offline hoặc quá 15 giây không nhận số đo đánh dấu Offline. Browser MQTT client reconnect mỗi 3 giây và subscribe lại; Agent exponential reconnect 1–30 giây. Mỗi client có ID ngẫu nhiên. Dùng mã thiết bị duy nhất.

## Lưu trữ

localStorage key `pcmon:<room>`, tối đa 2.000 mẫu/phòng. Nhật ký DOM tối đa 150 mục, biểu đồ tối đa 60 mẫu/máy. Người dùng có thể xóa hoặc xuất CSV. Không có lịch sử đồng bộ giữa người dùng; backend lưu tập trung là giai đoạn tiếp theo.

## Mở rộng

Backend Subscriber + SQLite/PostgreSQL cho lịch sử tập trung; cấp tài khoản ngắn hạn và ACL cho phòng; giới hạn tốc độ; đóng gói Agent EXE; host Broker riêng. Các phần này chưa được triển khai.
