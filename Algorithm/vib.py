import cv2
import time
import RPi.GPIO as GPIO

vibration_pin = 14

GPIO.setmode(GPIO.BCM)
GPIO.setup(vibration_pin, GPIO.IN)

# 영상 촬영 설정
video_output = "output.mp4"  # 저장할 영상 파일명
video_duration = 10  # 영상 촬영 시간 (초)

# 진동 감지 시간 리스트
vibration_times = []

# 진동 감지 콜백 함수
def vibration_callback(channel):
    if GPIO.input(vibration_pin) == GPIO.HIGH:
        # 진동이 감지되었을 때 실행할 코드
        print("Vibration detected!")
        vibration_times.append(time.time())  # 진동 감지 시간 기록

# 진동 감지 이벤트 핸들링
GPIO.add_event_detect(vibration_pin, GPIO.BOTH, callback=vibration_callback, bouncetime=200)

# 영상 촬영
cap = cv2.VideoCapture(0)  # 카메라 장치 번호로 변경 가능
out = cv2.VideoWriter(video_output, cv2.VideoWriter_fourcc(*"mp4v"), 30, (640, 480))  # 해상도와 FPS 조정 가능

start_time = time.time()
while time.time() - start_time < video_duration:
    ret, frame = cap.read()
    out.write(frame)

cap.release()
out.release()

# 진동 감지된 시간을 기준으로 영상 편집
if len(vibration_times) > 0:
    start_time = vibration_times[0] - 15
    end_time = vibration_times[-1] + 15

    edited_output = "edited_output.mp4"  # 편집된 영상 파일명

    cap = cv2.VideoCapture(video_output)
    out = cv2.VideoWriter(edited_output, cv2.VideoWriter_fourcc(*"mp4v"), 30, (640, 480))  # 해상도와 FPS 조정 가능

    while cap.get(cv2.CAP_PROP_POS_MSEC) < start_time * 1000:
        ret, frame = cap.read()

    while cap.get(cv2.CAP_PROP_POS_MSEC) <= end_time * 1000:
        ret, frame = cap.read()
        out.write(frame)

    cap.release()
    out.release()

    print("Video edited successfully!")