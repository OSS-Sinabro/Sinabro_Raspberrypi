import time
import paho.mqtt.client as mqtt
from camera import init, capture_image, finalize
import cv2

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

"""
Ex)
mqtt_broker = "172.30.1.20"
mqtt_topic = "cctv_1"
"""

# MQTT 객체 생성
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# 브로커 연결
client.connect(mqtt_broker, 1883)
client.loop_start()

try:
    # 특정 시간 간격으로 이미지를 촬영하고 크롭하여 MQTT 통신
    def capture_and_publish(interval, x, y, width, height):
        init()

        while True:
            print("working--")
            start_time = time.time()

            frame = capture_image()
            cropped_img = frame[y:y+height, x:x+width]

            _, img_encoded = cv2.imencode('.jpg', cropped_img)
            img_bytes = img_encoded.tobytes()

            if flag:  # flag가 True일 때만 MQTT로 보냄
                client.publish(mqtt_topic, payload=img_bytes, qos=0)
                print(mqtt_topic, " 이미지 전송")

            elapsed_time = time.time() - start_time
            sleep_time = interval - elapsed_time

            if sleep_time > 0:
                time.sleep(sleep_time)

        finalize()

    if __name__ == "__main__":
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

        # 이미지 촬영 및 크롭 후 MQTT 전송 (5초 간격으로 촬영)
        capture_and_publish(interval=5, x=crop_x, y=crop_y, width=crop_width, height=crop_height)

except KeyboardInterrupt:
    print("Interrupted by user. Cleaning up")
except Exception as e:
    print("An error occurred: ", e)
finally:
    client.loop_stop()
    client.disconnect()
