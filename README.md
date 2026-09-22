# 🖥️ HỆ THỐNG GIÁM SÁT PHÒNG MÁY THỜI GIAN THỰC QUA MẠNG

## 📌 Giới thiệu

**Hệ thống giám sát phòng máy thời gian thực qua mạng** là đề tài được xây dựng trong môn **Lập trình mạng**.

Hệ thống cho phép quản trị viên theo dõi trạng thái hoạt động của các máy tính trong phòng máy thông qua mạng LAN. Mỗi máy tính chạy một chương trình Client/Agent để thu thập thông tin hệ thống và gửi dữ liệu về Server theo thời gian thực.

Server tiếp nhận, xử lý và quản lý dữ liệu từ nhiều máy Client, sau đó cung cấp thông tin cho giao diện Dashboard để quản trị viên theo dõi tập trung.

## 🎯 Mục tiêu

- Giám sát trạng thái Online/Offline của các máy tính.
- Theo dõi mức sử dụng CPU và RAM theo thời gian thực.
- Thu thập thông tin từ nhiều máy tính thông qua mạng.
- Xây dựng mô hình giao tiếp Client–Server.
- Áp dụng lập trình Socket và giao thức TCP/IP.
- Xử lý nhiều Client kết nối đồng thời.
- Phát hiện và thông báo khi máy tính mất kết nối.
- Lưu trữ dữ liệu giám sát để phục vụ theo dõi và thống kê.

## 🏗️ Kiến trúc hệ thống

```text
┌──────────────┐
│    Client    │
│     PC 01    │
└──────┬───────┘
       │
       │ TCP/IP
       ▼
┌──────────────┐
│    Server    │
│              │
│ Socket Server│
│ Data Handler │
└──────┬───────┘
       │
       │
       ▼
┌──────────────┐
│   Dashboard  │
│              │
│ CPU / RAM    │
│ Online/Offline│
└──────────────┘
