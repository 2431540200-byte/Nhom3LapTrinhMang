"""Publish actual host metrics to MQTT. No remote command execution."""
import argparse
import json
import logging
import math
import os
import re
import signal
import socket
import ssl
import threading
import time
import uuid
from datetime import datetime, timezone
from urllib.parse import urlparse


def default_device():
    """Tên máy đã làm sạch để hợp lệ làm mã thiết bị."""
    name = re.sub(r'[^A-Za-z0-9_-]', '-', socket.gethostname())[:40]
    return name or 'PC01'


def parse_args():
    p = argparse.ArgumentParser(description='MQTT PC Monitor — Agent lấy số đo thật')
    p.add_argument('--room', required=True, help='Mã phòng trên website')
    p.add_argument('--device', default=default_device(), help='Mã máy: chữ, số, _ hoặc -')
    p.add_argument('--broker', default='wss://broker.hivemq.com:8884/mqtt')
    p.add_argument('--disk', default=os.path.abspath(os.sep), help='Phân vùng cần đo, ví dụ C:\\')
    p.add_argument('--interval', type=float, default=3)
    p.add_argument('--no-hostname', action='store_true',
                   help='Không gửi tên máy thật lên Broker')
    args = p.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_-]{6,40}', args.room):
        p.error('room cần 6–40 chữ, số, _ hoặc -')
    if not re.fullmatch(r'[A-Za-z0-9_-]{1,40}', args.device):
        p.error('device cần 1–40 chữ, số, _ hoặc -')
    if not math.isfinite(args.interval) or args.interval < 1:
        p.error('interval phải là số hữu hạn >= 1 giây')
    if args.interval > 10:
        p.error('interval nên <= 10 giây (Dashboard coi Offline sau 15 giây)')
    return args


def main():
    args = parse_args()
    try:
        import psutil
        import paho.mqtt.client as mqtt
    except ImportError as exc:
        raise SystemExit(
            f'Thiếu thư viện "{exc.name}". Chạy: python -m pip install -r agent/requirements.txt')
    url = urlparse(args.broker)
    if url.scheme not in ('wss', 'mqtts') or not url.hostname or url.username or url.password:
        raise SystemExit('Dùng URL wss:// hoặc mqtts://, không chứa tài khoản.')
    try:
        psutil.disk_usage(args.disk)
    except OSError as exc:
        raise SystemExit(f'Không đọc được phân vùng: {exc}')
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
    stop = threading.Event()
    connected = threading.Event()
    prefix = f'pcmon/v1/{args.room}/devices/{args.device}'
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,
                         client_id=f'agent_{uuid.uuid4().hex[:16]}',
                         transport='websockets' if url.scheme == 'wss' else 'tcp',
                         protocol=mqtt.MQTTv311)
    if url.scheme == 'wss':
        path = url.path or '/mqtt'
        if url.query:
            path += '?' + url.query
        client.ws_set_options(path=path)
    client.tls_set(tls_version=ssl.PROTOCOL_TLS_CLIENT)
    if os.environ.get('MQTT_USERNAME'):
        client.username_pw_set(os.environ['MQTT_USERNAME'], os.environ.get('MQTT_PASSWORD'))
    offline = json.dumps({'state': 'offline', 'source': 'agent'})
    client.will_set(prefix + '/status', offline, qos=1, retain=True)
    client.reconnect_delay_set(min_delay=1, max_delay=30)
    client.max_queued_messages_set(10)

    def on_connect(c, userdata, flags, reason_code, properties):
        if reason_code.is_failure:
            logging.error('Broker từ chối kết nối: %s', reason_code)
            return
        connected.set()
        c.publish(prefix + '/status', json.dumps({'state': 'online', 'source': 'agent'}), qos=1, retain=True)
        logging.info('Đã kết nối. Phòng %s / %s', args.room, args.device)

    def on_disconnect(c, userdata, flags, reason_code, properties):
        connected.clear()
        logging.info('Mất kết nối; sẽ thử lại nếu Agent chưa dừng.')

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, lambda *_: stop.set())
    port = url.port or (443 if url.scheme == 'wss' else 8883)
    client.connect_async(url.hostname, port, keepalive=15)
    client.loop_start()
    psutil.cpu_percent(interval=None)
    logging.info('Đang kết nối. Ctrl+C để dừng. Không gửi dữ liệu riêng tư lên Broker công cộng.')
    try:
        while not stop.wait(args.interval):
            cpu = psutil.cpu_percent(interval=None)
            if not connected.is_set():
                continue
            try:
                disk = psutil.disk_usage(args.disk).percent
            except OSError as exc:
                logging.warning('Không đọc được phân vùng, bỏ qua lượt này: %s', exc)
                continue
            data = {'cpu': cpu, 'ram': psutil.virtual_memory().percent,
                    'disk': disk, 'source': 'agent',
                    'timestamp': datetime.now(timezone.utc).isoformat()}
            if not args.no_hostname:
                data['hostname'] = socket.gethostname()
            result = client.publish(prefix + '/metrics', json.dumps(data), qos=1, retain=False)
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                logging.info('CPU %.1f%% | RAM %.1f%% | Disk %.1f%%', data['cpu'], data['ram'], data['disk'])
    finally:
        if connected.is_set():
            result = client.publish(prefix + '/status', offline, qos=1, retain=True)
            try:
                result.wait_for_publish(timeout=3)
            except (RuntimeError, ValueError):
                pass
        client.disconnect()
        client.loop_stop()


if __name__ == '__main__':
    main()
