# 카메라 촬영 코드
import cv2

# 카메라 객체
camera = None
fps = 3

# 카메라 초기화
def init(camera_id=0, width=640, height=480, fps=fps):
    global camera
    # 카메라 설정
    camera = cv2.VideoCapture(camera_id)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    camera.set(cv2.CAP_PROP_FPS, fps)

    if not camera.isOpened():
        print("카메라를 열 수 없습니다.")

# 이미지 촬영
def capture_image():
    success, frame = camera.read()
    return frame

# 카메라 해제
def finalize():
    global camera
    if camera is not None:
        camera.release()
    camera = None
