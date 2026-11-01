# MQTT / PC Monitor

Website tiếng Việt để thực hành MQTT qua mạng và giám sát tài nguyên máy tính.

## Có gì trong bản 1.0?

- MQTT thật qua WSS giữa nhiều trình duyệt, sử dụng MQTT.js.
- Tạo mã phòng, chia sẻ link; Publish / Subscribe; QoS 0/1/2; retained; unsubscribe.
- Thiết bị thử: chỉnh CPU/RAM/Disk rồi gửi định kỳ 3 giây.
- Dashboard nhiều máy, tìm kiếm, ngưỡng cảnh báo, Offline sau 15 giây không có số đo.
- Agent Python dùng psutil lấy CPU/RAM/Disk thật, Paho MQTT và TLS.
- Last Will cho Agent; kết nối lại tự động; nhật ký message.
- Biểu đồ 60 mẫu gần nhất theo máy; lịch sử 2.000 mẫu/phòng trên trình duyệt; xuất CSV.
- Responsive, không cần build hoặc cài Node để sử dụng website.

**Chưa có:** tài khoản, phân quyền phòng, database/backend tập trung, bộ cài EXE. Không điều khiển máy từ xa.

## 1. Chạy website trên Windows

Cài Python, giải nén project, mở Terminal tại thư mục có `index.html`:

```powershell
python -m http.server 8080
```

Mở **http://localhost:8080**. Không mở index.html bằng file:// vì trang dùng JavaScript modules.

Website cần Internet để tải MQTT.js và kết nối Broker. Font có dự phòng hệ thống.
Nếu báo chưa tải thư viện MQTT, kiểm tra kết nối đến unpkg.com rồi tải lại trang.

## 2. Thử hai trình duyệt / hai máy

1. Mở web, giữ Broker mặc định `wss://test.mosquitto.org:8081/mqtt` hoặc nhập Broker WSS riêng.
2. Tạo mã phòng, bấm **Kết nối MQTT**. Chờ trạng thái Đã kết nối.
3. Sao chép link sang trình duyệt khác; cả hai phải dùng cùng Broker và phòng.
4. Trình duyệt A theo dõi Dashboard; B chọn PC01 và **Phát mỗi 3 giây**.
5. Thay thanh CPU lên 95: A nhận số đo, thấy cảnh báo nếu ngưỡng là 90.
6. Dừng thiết bị: A thấy Offline. Đóng đột ngột tab B: A đánh dấu Offline sau 15 giây không có số đo.
7. Chọn thẻ PC01 để xem biểu đồ, bấm Xuất CSV để tải lịch sử.

Link localhost chỉ hoạt động trên máy đang chạy server. Để chia sẻ qua LAN, dùng `http://IP-MAY-CHU:8080/?room=MA_PHONG` và mở cổng 8080 trong mạng riêng; hoặc đưa lên GitHub Pages.
Mỗi tab/Agent phải có mã thiết bị khác nhau để tránh trộn dữ liệu.

## 3. Thực hành Publish / Subscribe

- Hai tab cùng phòng và Broker; mở **Thực hành MQTT**.
- A Subscribe `classroom/temperature`.
- B Publish `{"temperature":28}` vào `classroom/temperature`.
- A thấy message trong nhật ký. Topic khác sẽ không khớp.
- Thử `classroom/+` và `classroom/#`.
- B bật retained và gửi; một tab mới Subscribe sẽ nhận lại giá trị đã giữ.
- Bấm **Xóa retained tại Topic này** để xóa retained trên Broker.
- QoS áp dụng cho từng chặng MQTT; QoS phía Subscriber là giới hạn yêu cầu và Broker có thể cấp thấp hơn. QoS 2 không đảm bảo tác vụ database được thực hiện duy nhất một lần.

## 4. Giám sát máy thật bằng Agent

Tại thư mục project:

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r agent\requirements.txt
.venv\Scripts\python agent\agent.py --room MA_PHONG --device PC01
```

Thay `MA_PHONG` bằng mã phòng trên website (6–40 chữ/số/_/-). Máy thứ hai dùng PC02.
Mặc định đo phân vùng hệ thống. Có thể chọn bằng `--disk C:\` (Windows) hoặc `--disk /` (Linux).
Ctrl+C dừng Agent bình thường. Ngắt mạng đột ngột sẽ dựa vào Last Will và timeout.
Agent gửi hostname thật; chỉ chạy khi người dùng đồng ý chia sẻ thông tin máy.

Broker riêng:

```powershell
$env:MQTT_USERNAME="your-user"
$env:MQTT_PASSWORD="your-password"
.venv\Scripts\python agent\agent.py --room MA_PHONG --device PC01 --broker wss://broker.example.com/mqtt
```

Nhập cùng Broker và tài khoản tương ứng trên web. Không commit tài khoản lên GitHub.
Agent cũng hỗ trợ `mqtts://host:8883`; web luôn cần endpoint WSS của cùng Broker.

## 5. Push GitHub và bật Pages

1. Tạo repository mới trên GitHub, ví dụ `mqtt-pc-monitor`.
2. Upload **nội dung bên trong thư mục project** lên repository để index.html ở gốc. Có thể dùng Add file → Upload files; giữ cấu trúc assets và agent.
3. Hoặc dùng Git:

```bash
git init
git add .
git commit -m "Initial MQTT PC Monitor"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/mqtt-pc-monitor.git
git push -u origin main
```

4. Repository → Settings → Pages → Deploy from a branch → `main` / `(root)` → Save.
5. Sau khi GitHub triển khai thành công, mở URL được Pages hiển thị, thường là `https://YOUR_USERNAME.github.io/mqtt-pc-monitor/`.
6. Thử lại trên hai thiết bị bằng link công khai.

Chưa có link công khai được triển khai sẵn trong bộ file này. GitHub Pages chỉ host web; Broker chạy ở dịch vụ khác.

## Broker công cộng và bảo mật

Broker mặc định là dịch vụ thử nghiệm của Mosquitto, có thể mất kết nối, hạn chế hoặc thay đổi endpoint. Không có cam kết vận hành; người dùng có thể thay WSS URL.
Mọi người có thể đọc/ghi Topic trên Broker công cộng. Mã phòng ngẫu nhiên chỉ hạn chế đụng Topic, KHÔNG xác thực người dùng và không chứng minh dữ liệu là từ Agent đáng tin cậy.
Không truyền dữ liệu nhạy cảm. Không nhúng tài khoản quản trị Broker vào mã web. Muốn dịch vụ riêng tư cần Broker riêng, TLS, tài khoản, ACL và cơ chế cấp quyền phía server.
Tên Topic được giới hạn trong prefix của phòng bởi giao diện, không phải lớp bảo mật chống client bên ngoài.

## Lịch sử và trạng thái

Số đo không retained để tránh hiển thị số đo cũ như mới. Agent giữ status Online/Offline; Dashboard chỉ coi máy Online khi nhận số đo mới. Sau reload, số đo cục bộ hiển thị Offline cho tới khi có dữ liệu mới.
Khi web mất Broker, tất cả máy hiển thị Offline; điều đó cũng có thể là đường kết nối của Dashboard bị gián đoạn, chưa chứng minh các máy đã tắt.
Ngưỡng áp dụng chung, cảnh báo khi bất kỳ chỉ số nào > ngưỡng. Disk là % dung lượng đã dùng, không phải tốc độ I/O.
Đồng hồ biểu đồ dùng thời gian nhận tại trình duyệt. Tab nền có thể bị trình duyệt làm chậm; Agent Python phù hợp giám sát liên tục hơn thiết bị thử trên web.

## Kiểm tra mã nguồn

Cần Node 22+ để chạy test, không cần npm install:

```bash
npm test
node --check assets/app.js
python -m py_compile agent/agent.py
```

Xem `docs/TESTING.md` cho kiểm thử tích hợp và `docs/ARCHITECTURE.md` cho luồng dữ liệu.

## Cấu trúc

```text
index.html               Website, các panel tiếng Việt
assets/app.js            Kết nối, thiết bị, Dashboard, lịch sử
assets/core.js           Quy tắc Topic, kiểm tra số đo, CSV
assets/style.css         Giao diện pastel, responsive
agent/agent.py           Thu thập và gửi số đo thật
agent/requirements.txt   Thư viện Agent
 tests/                  Kiểm thử logic
 docs/                   Kiến trúc và kiểm thử
```

Mã nguồn theo MIT License. MQTT.js, Paho và psutil tuân theo giấy phép riêng của từng dự án.
