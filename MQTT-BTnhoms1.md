MQTT – Giao thức truyền thông nhẹ cho IoT
1. MQTT là gì?

MQTT (Message Queuing Telemetry Transport) là một giao thức truyền thông nhẹ, được thiết kế để trao đổi dữ liệu giữa các thiết bị thông qua mạng.

MQTT hoạt động theo mô hình Publish/Subscribe, trong đó các thiết bị không cần kết nối trực tiếp với nhau mà giao tiếp thông qua một thành phần trung gian gọi là MQTT Broker.

MQTT thường được sử dụng trong:

IoT (Internet of Things)
Cảm biến và thiết bị thông minh
Nhà thông minh
Hệ thống thu thập dữ liệu
Các ứng dụng cần truyền dữ liệu nhẹ
2. MQTT hoạt động như thế nào?

MQTT có 3 thành phần chính:

Client

Client là thiết bị hoặc chương trình sử dụng MQTT.

Một Client có thể:

Publish dữ liệu
Subscribe dữ liệu
Hoặc thực hiện cả hai.
Broker

Broker là trung gian giao tiếp giữa các Client.

Broker có nhiệm vụ:

Nhận message từ Publisher.
Kiểm tra Topic.
Chuyển message đến các Subscriber đã đăng ký Topic tương ứng.
Topic

Topic là tên của kênh dùng để phân loại dữ liệu.

Ví dụ:

sensor/temperature
sensor/humidity
device/001/status
3. Mô hình MQTT

Mô hình cơ bản:

Publisher
    |
    | Publish
    ↓
 MQTT Broker
    |
    | Message
    ↓
Subscriber

Điểm quan trọng:

Publisher và Subscriber không cần kết nối trực tiếp với nhau. MQTT Broker đứng giữa để nhận và phân phối message.

4. Publish là gì?

Publish nghĩa là gửi một message lên một Topic.

Ví dụ:

Topic:
sensor/temperature

Message:
30°C

Publisher gửi:

Publish
Topic: sensor/temperature
Message: 30°C

Broker nhận message và chuyển đến những Client đã Subscribe Topic đó.

5. Subscribe là gì?

Subscribe nghĩa là đăng ký nhận message từ một Topic.

Ví dụ:

Subscribe:
sensor/temperature

Khi có Publisher gửi:

Topic: sensor/temperature
Message: 30°C

Subscriber sẽ nhận được:

30°C
6. Topic trong MQTT

Topic được sử dụng để phân loại message.

Ví dụ:

sensor/temperature
sensor/humidity
home/livingroom/light
device/001/status

Có thể tổ chức Topic theo nhiều cấp.

Ví dụ:

home/
├── livingroom/
│   ├── temperature
│   └── light
│
└── bedroom/
    ├── temperature
    └── light

Nhờ Topic, Broker biết message cần được gửi đến những Subscriber nào.

7. MQTT Broker

Broker là thành phần trung tâm của hệ thống MQTT.

Một số Broker phổ biến:

Eclipse Mosquitto
EMQX
HiveMQ

Trong bài demo có thể sử dụng Eclipse Mosquitto làm Broker.

Luồng hoạt động:

Client A
   |
   | Publish
   ↓
Broker
   |
   | Phân phối message
   ↓
Client B
   |
Client C
8. MQTT và mô hình OSI

MQTT thuộc tầng ứng dụng – Layer 7 trong mô hình OSI.

MQTT thường chạy trên TCP.

┌──────────────────────┐
│ Application          │
│ MQTT                 │
├──────────────────────┤
│ Transport            │
│ TCP                  │
├──────────────────────┤
│ Internet             │
│ IP                   │
├──────────────────────┤
│ Network Access       │
└──────────────────────┘

Cổng thường gặp:

MQTT       → TCP 1883
MQTT + TLS → TCP 8883
9. QoS trong MQTT

QoS (Quality of Service) quy định mức độ đảm bảo khi gửi message.

MQTT có 3 mức QoS.

QoS 0 – At most once

Message được gửi tối đa một lần.

Publisher → Broker

Không có cơ chế đảm bảo message chắc chắn đến nơi.

Ưu điểm: nhanh và đơn giản.

QoS 1 – At least once

Message được đảm bảo gửi ít nhất một lần.

Có thể xảy ra trường hợp message được nhận nhiều hơn một lần.

Publisher → Broker
       ← ACK
QoS 2 – Exactly once

Message được đảm bảo xử lý đúng một lần.

Độ tin cậy cao hơn nhưng quá trình trao đổi phức tạp hơn.

Bảng tổng hợp
QoS	Ý nghĩa	Độ tin cậy
0	At most once	Thấp
1	At least once	Trung bình
2	Exactly once	Cao
10. Ưu điểm của MQTT
Ưu điểm
Giao thức nhẹ.
Cấu trúc đơn giản.
Tiết kiệm băng thông.
Phù hợp với thiết bị có tài nguyên hạn chế.
Hỗ trợ mô hình Publish/Subscribe.
Có nhiều mức QoS.
Có thể mở rộng cho nhiều Client.
Nhược điểm
Cần MQTT Broker làm trung gian.
Nếu Broker gặp sự cố, hệ thống có thể bị ảnh hưởng.
Cần cấu hình bảo mật phù hợp khi truyền dữ liệu quan trọng.
11. Demo MQTT bằng Python

Có thể sử dụng thư viện Paho MQTT.

Cài đặt:

pip install paho-mqtt
Publisher
import paho.mqtt.client as mqtt

client = mqtt.Client()

client.connect("localhost", 1883)

client.publish("test/message", "Hello MQTT!")

print("Da gui message")

client.disconnect()

Chương trình thực hiện:

1. Tạo MQTT Client
2. Kết nối Broker
3. Publish message
4. In thông báo
5. Ngắt kết nối
12. Subscriber
import paho.mqtt.client as mqtt

def on_message(client, userdata, msg):
    print("Nhan:", msg.payload.decode())

client = mqtt.Client()

client.on_message = on_message

client.connect("localhost", 1883)

client.subscribe("test/message")

client.loop_forever()

Subscriber sẽ đăng ký:

test/message

Khi Publisher gửi:

Hello MQTT!

Subscriber nhận:

Nhan: Hello MQTT!
13. Luồng Demo hoàn chỉnh
┌──────────────┐
│   Publisher  │
│    Python    │
└──────┬───────┘
       │
       │ Publish
       ↓
┌──────────────┐
│ MQTT Broker  │
│  Mosquitto   │
└──────┬───────┘
       │
       │ Message
       ↓
┌──────────────┐
│  Subscriber  │
│    Python    │
└──────────────┘

Ví dụ:

Publisher
    ↓
Topic: test/message
    ↓
Message: Hello MQTT!
    ↓
Broker
    ↓
Subscriber
    ↓
Nhan: Hello MQTT!
14. MQTT được sử dụng ở đâu?

MQTT phù hợp với những hệ thống cần truyền dữ liệu giữa nhiều thiết bị.

Ví dụ:

🌡️ Cảm biến nhiệt độ
💡 Nhà thông minh
🚗 Thiết bị IoT trên xe
🏭 Nhà máy thông minh
📡 Hệ thống cảm biến
📊 Thu thập dữ liệu từ thiết bị
15. Các thuật ngữ cần nhớ khi thuyết trình
Thuật ngữ	Ý nghĩa
MQTT	Giao thức truyền thông nhẹ
Client	Thiết bị/chương trình sử dụng MQTT
Broker	Máy chủ trung gian
Publisher	Client gửi message
Subscriber	Client nhận message
Topic	Kênh phân loại message
Message	Dữ liệu được truyền
Publish	Gửi message
Subscribe	Đăng ký nhận message
QoS	Mức độ đảm bảo truyền message
TCP	Giao thức vận chuyển thường được MQTT sử dụng
16. Câu hỏi có thể bị hỏi khi thuyết trình
MQTT là gì?

MQTT là giao thức truyền thông nhẹ, hoạt động theo mô hình Publish/Subscribe và thường được sử dụng trong các hệ thống IoT.

MQTT có mấy thành phần chính?

Ba thành phần chính là Client, Broker và Topic.

Broker có nhiệm vụ gì?

Broker nhận message từ Publisher và phân phối message đến các Subscriber phù hợp.

Publisher và Subscriber có kết nối trực tiếp không?

Không. Hai bên giao tiếp thông qua MQTT Broker.

MQTT thuộc tầng nào của OSI?

MQTT thuộc tầng ứng dụng, Layer 7.

MQTT thường sử dụng port nào?

MQTT thường sử dụng TCP port 1883; MQTT sử dụng TLS thường dùng port 8883.

QoS có mấy mức?

Có 3 mức: QoS 0, QoS 1 và QoS 2.

MQTT khác mô hình gửi trực tiếp như thế nào?

MQTT sử dụng Broker làm trung gian và mô hình Publish/Subscribe, giúp Publisher không cần biết trực tiếp Subscriber là ai.

17. Tài liệu/GitHub tham khảo

Có thể đưa vào cuối README:

Eclipse Paho MQTT:
GitHub – Eclipse Paho
MQTT Examples:
GitHub – MQTT Examples
