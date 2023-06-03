import socket
import Jetson.GPIO as GPIO
import time

host = 'localhost'
port = 8888

button_pin = 18
motor_pin = 12

GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(motor_pin, GPIO.OUT)
pwm = GPIO.PWM(motor_pin, 100)

prev_button_state = GPIO.HIGH


def run_vibration_motor(duration):
    pwm.start(50)
    time.sleep(duration)
    pwm.stop()


def check_button_status():
    button_state = GPIO.input(button_pin)

    if button_state == GPIO.LOW and prev_button_state == GPIO.HIGH:
        return True
    
    return False


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(2)

print('Server started. Waiting for connections...')

clientA_socket, addrA = server_socket.accept()
print('Client A connected:', addrA)

clientB_socket, addrB = server_socket.accept()
print('Client B connected:', addrB)

current_model = 'A'
clientA_socket.send('A'.encode())
clientB_socket.send('A'.encode())

try:
    while True:
        if check_button_status():
            if current_model == 'A':
                print('Button pressed! Changing to model B')
                run_vibration_motor(1.0)
                current_model = 'B'
                clientA_socket.send('B'.encode())
                print('B')
                clientB_socket.send('B'.encode())
            else:
                print('Button pressed! Changing to model A')
                run_vibration_motor(1.0)
                current_model = 'A'
                clientA_socket.send('A'.encode())
                print("A")
                clientB_socket.send('A'.encode())
        
        prev_button_state = GPIO.input(button_pin)

        time.sleep(0.2)
                
except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
    clientA_socket.close()
    clientB_socket.close()
    server_socket.close()
