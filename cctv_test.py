import time
import paho.mqtt.client as mqtt
import cv2
import os

flag = False

def on_connect(client, userdata, flags, rc):
    print("connect")
    client.subscribe("action", qos=0)

def on_message(client, userdata, msg):
    global flag

    command = msg.payload.decode("utf-8")
    if command == "goStop":
        flag = not flag


# MQTT 브로커 ip
mqtt_broker = ""    # 서버 MQTT broker ip address 입력
# topic 설정
mqtt_topic = ""     # "cctv_n(숫자)" 형식으로 설정
# test 영상 파일 경로
video_path = ''

"""
Ex)
mqtt_broker = "172.30.1.20"
mqtt_topic = "cctv_1"
video_path = "mud.mp4"
"""

# MQTT 객체 생성
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# 브로커 연결
client.connect(mqtt_broker, 1883)
client.loop_start()

# 크롭할 위치와 크기 설정
crop_x = 
crop_y = 
crop_width = 
crop_height =

"""
Ex) 시연영상 설정
crop_x = 365
crop_y = 684
crop_width = 110
crop_height = 110
"""

# 영상 캡처 및 크롭 후 MQTT 통신
def capture_and_publish(interval):
    print("working--")
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break


        print(mqtt_topic, "  image send")
        # 이미지 크롭
        cropped_img = frame[crop_y:crop_y+crop_height, crop_x:crop_x+crop_width]

        # 서버로 이미지 송신
        _, img_encoded = cv2.imencode('.jpg', cropped_img)
        img_bytes = img_encoded.tobytes()

        client.publish(mqtt_topic, payload=img_bytes, qos=0)

        time.sleep(interval)

        # 프레임 넘기기
        """
        range(fps * 넘길 시간(sec) - 1)
        Ex) 30 fps & 5초 넘기기 : 149
        """
        for _ in range(149):
            cap.read()

    cap.release()

try:
    # 4+a초 간격으로 영상 캡처 및 크롭 후 MQTT 통신
    capture_and_publish(interval=4)

except KeyboardInterrupt:
    print("Interrupted by user. Cleaning up")
except Exception as e:
    print("An error occurred: ", e)
finally:
    client.loop_stop()
    client.disconnect()
