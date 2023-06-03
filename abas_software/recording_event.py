import cv2
import time
import Jetson.GPIO as GPIO
from playsound import playsound


vibration_pin = 16

GPIO.setmode(GPIO.BOARD)
GPIO.setup(vibration_pin, GPIO.IN)
event = 0
flag = False

# 영상 촬영 설정
video_output = "/home/jetson/catkin_ws/src/darknet/Record_KIOO/output.mp4"  # 저장할 영상 파일명
video_duration = 100  # 영상 촬영 시간 (초)

# 진동 감지 시간 리스트

# 진동 감지 콜백 함수
def vibration_callback(channel):
    global flag
    if GPIO.input(vibration_pin) == GPIO.HIGH and not flag:
        # 진동이 감지되었을 때 실행할 코드
        print("Vibration detected!")
        current_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
        vibration_frames.append(current_frame)
        print(vibration_frames)
        playsound("mp3/collison_detect.mp3")
        flag = True

# 진동 감지 이벤트 핸들링
GPIO.add_event_detect(vibration_pin, GPIO.BOTH, callback=vibration_callback, bouncetime=200)

# 영상 촬영
try:
    while True:
        vibration_frames = []
        cap = cv2.VideoCapture('nvarguscamerasrc ! video/x-raw(memory:NVMM), width=640, height=480, format=(string)NV12, framerate=(fraction)20/1 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink', cv2.CAP_GSTREAMER)  # 카메라 장치 번호로 변경 가능
        out = cv2.VideoWriter(video_output, cv2.VideoWriter_fourcc(*"mp4v"), 20, (640, 480))  # 해상도와 FPS 조정 가능

        start_time = time.time()
        while time.time() - start_time < video_duration:
            ret, frame = cap.read()
            cv2.imshow('video',frame)

            key = cv2.waitKey(1)
            out.write(frame)

        cap.release()
        out.release()


        # 진동 감지된 시간을 기준으로 영상 편집
        if len(vibration_frames) > 0:
            event+=1
            edited_output = f"/home/jetson/catkin_ws/src/darknet/Record_KIOO/event/event{str(event)}.mp4"  # 편집된 영상 파일명

            cap = cv2.VideoCapture(video_output) 
            out = cv2.VideoWriter(edited_output, cv2.VideoWriter_fourcc(*"mp4v"), 20, (640, 480))  # 해상도와 FPS 조정 가능

            frame_rate = cap.get(cv2.CAP_PROP_FPS)

            start_frame = vibration_frames[0] - int(2*frame_rate)
            end_frame = vibration_frames[0] + int(2*frame_rate)


            print(start_frame)
            print(end_frame)

            cap.set(cv2.CAP_PROP_POS_FRAMES,start_frame)

            while cap.get(cv2.CAP_PROP_POS_FRAMES) <= end_frame:
                ret, frame = cap.read()
                if not ret:
                    break
                out.write(frame)

            cap.release()
            out.release()

            print("Video edited successfully!")
except KeyboardInterrupt:
    cap.release()
    out.release()
    cv2.destroyAllWindows()
