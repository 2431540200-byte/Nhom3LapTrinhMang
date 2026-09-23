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
2. 🔎 Các Project tham khảo

Nhóm tham khảo một số project mã nguồn mở có liên quan đến MQTT, monitoring và thu thập dữ liệu hệ thống.

Project 1: Eclipse Paho MQTT

GitHub:

https://github.com/eclipse-paho

Eclipse Paho cung cấp các thư viện MQTT Client cho nhiều ngôn ngữ lập trình.

Nhóm tham khảo project này để tìm hiểu:

MQTT Client
Publish
Subscribe
MQTT Topic
Kết nối tới MQTT Broker
Gửi và nhận message
Project 2: MQTT Examples

GitHub:

https://github.com/tigoe/mqtt-examples

Project cung cấp nhiều ví dụ về cách sử dụng MQTT trong các ứng dụng thực tế.

Nhóm tham khảo:

Cách xây dựng Publisher
Cách xây dựng Subscriber
Cách tổ chức MQTT Topic
Cách truyền dữ liệu giữa các thiết bị
Project 3: Eclipse Mosquitto

GitHub:

https://github.com/eclipse-mosquitto/mosquitto

Mosquitto là một MQTT Broker mã nguồn mở.

Nhóm sử dụng Mosquitto làm cơ sở để triển khai MQTT Broker cho hệ thống.

Nhóm tìm hiểu:

MQTT Broker
Client connection
Topic
Publish/Subscribe
QoS
Retained Message
Last Will and Testament
3. 🚀 Những điểm nhóm phát triển thêm

Các project tham khảo chủ yếu tập trung vào việc minh họa hoặc cung cấp thư viện/giao thức MQTT.

Nhóm sẽ phát triển thành một ứng dụng giám sát phòng máy hoàn chỉnh, tập trung vào việc quản lý nhiều máy tính trong cùng một hệ thống.

Các chức năng nhóm dự kiến bổ sung
3.1. 🖥️ Giám sát nhiều máy tính

Cho phép nhiều máy tính trong phòng máy cùng kết nối đến MQTT Broker.

Ví dụ:

PC01 🟢 Online
PC02 🟢 Online
PC03 🔴 Offline
PC04 🟢 Online
PC05 🟢 Online
3.2. 📊 Giám sát tài nguyên máy

Hệ thống thu thập:

CPU: 45%
RAM: 62%
Disk: 70%

và cập nhật lên Dashboard theo thời gian thực.

3.3. 🔴 Phát hiện máy Offline

Nếu Client mất kết nối với hệ thống, Dashboard sẽ cập nhật trạng thái:

PC03 🔴 OFFLINE

Nhóm dự kiến sử dụng cơ chế phù hợp của MQTT như Last Will and Testament để hỗ trợ phát hiện trạng thái mất kết nối.

3.4. ⚠️ Cảnh báo tài nguyên

Khi CPU hoặc RAM vượt ngưỡng được cấu hình:

CPU > 90%

Dashboard hiển thị:

⚠️ CẢNH BÁO

PC02 đang sử dụng CPU 95%
3.5. 📈 Dashboard thời gian thực

Xây dựng giao diện tập trung cho phép quản trị viên:

Xem danh sách máy.
Xem trạng thái Online/Offline.
Theo dõi CPU.
Theo dõi RAM.
Theo dõi Disk.
Xem cảnh báo.
Theo dõi dữ liệu theo thời gian thực.
3.6. 💾 Lưu lịch sử dữ liệu

Khác với các ví dụ MQTT cơ bản chỉ truyền message, hệ thống của nhóm sẽ lưu dữ liệu giám sát vào Database.

Ví dụ:

PC01 | 12:30:01 | CPU 45% | RAM 60%
PC01 | 12:30:05 | CPU 48% | RAM 61%
PC01 | 12:30:10 | CPU 52% | RAM 63%

Từ đó có thể xây dựng biểu đồ thống kê mức sử dụng tài nguyên.

🛠️ Công nghệ dự kiến
Python
MQTT
Eclipse Mosquitto
Paho MQTT
MySQL / SQLite
Flask / HTML / CSS / JavaScript
Git & GitHub
