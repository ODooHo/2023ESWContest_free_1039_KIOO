import RPi.GPIO as GPIO

#딥러닝 모델을 두가지 함수로 정의해야할듯, def deep_obj_detection / def deep_road_detection 
#이런식으로 해서, 버튼이 눌렸을 때, 안눌렸을 때 잘 되는지 확인 해보긴 해야하는데 좀 많이 어려울지도,,
#그냥 내가 생각한대로만 짠거라 많이 수정하긴 해야할듯

button_pin = 12  

GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# 버튼 상태 감지 함수
def button_callback(channel):
    if GPIO.input(button_pin) == GPIO.LOW:
        # 버튼이 눌렸을 때 실행할 코드
        print("Button pressed!")
        # 딥러닝 모델 전환 및 실행 코드 작성

# 버튼 이벤트 핸들링
GPIO.add_event_detect(button_pin, GPIO.BOTH, callback=button_callback, bouncetime=200)

# 프로그램 실행 유지
while True:
    pass
