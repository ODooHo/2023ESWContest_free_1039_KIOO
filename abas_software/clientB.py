import socket
import time
from ctypes import *
import random
import os
import cv2
import time
import darknet
import argparse
from threading import Thread, enumerate, Event
import threading
import Jetson.GPIO as GPIO
import paddle
from paddleseg.cvlibs import manager, Config
from paddleseg.utils import get_sys_env, logger, get_image_list
from paddleseg.core import predict
from paddleseg.transforms import Compose
from playsound import playsound



HOST = 'localhost'
PORT = 8888


exit_flag = False


vibration_frames = []
vibration_pin = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(vibration_pin, GPIO.IN)
event = 0

# 영상 촬영 설정
video_output = "/home/jetson/catkin_ws/src/darknet/Record_KIOO/output.mp4"  # 저장할 영상 파일명
video_duration = 10  # 영상 촬영 시간 (초)




# 진동 감지 콜백 함수
def vibration_callback(channel):
    if GPIO.input(vibration_pin) == GPIO.HIGH:
        # 진동이 감지되었을 때 실행할 코드
        print("Vibration detected!")
        current_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
        vibration_frames.append(current_frame)
        print(vibration_frames)


# 진동 감지 이벤트 핸들링
GPIO.add_event_detect(vibration_pin, GPIO.BOTH, callback=vibration_callback, bouncetime=200)


def run_model_B():
    def parse_args():
        parser = argparse.ArgumentParser(description='Model prediction')
        # params of prediction
        parser.add_argument(
            "--config", dest="cfg", help="The config file.", default=None, type=str)
        parser.add_argument(
            '--model_path',
            dest='model_path',
            help='The path of model for prediction',
            type=str,
            default=None)
        parser.add_argument(
            '--image_path',
            dest='image_path',
            help='The image to predict, which can be a path of image, or a file list containing image paths, or a directory including images',
            type=str,
            default=None)
        parser.add_argument(
            '--save_dir',
            dest='save_dir',
            help='The directory for saving the predicted results',
            type=str,
            default='./output/result')
        # augment for prediction
        parser.add_argument(
            '--aug_pred',
            dest='aug_pred',
            help='Whether to use mulit-scales and flip augment for prediction',
            action='store_true')
        parser.add_argument(
            '--scales',
            dest='scales',
            nargs='+',
            help='Scales for augment',
            type=float,
            default=1.0)
        parser.add_argument(
            '--flip_horizontal',
            dest='flip_horizontal',
            help='Whether to use flip horizontally augment',
            action='store_true')
        parser.add_argument(
            '--flip_vertical',
            dest='flip_vertical',
            help='Whether to use flip vertically augment',
            action='store_true')
        # sliding window prediction
        parser.add_argument(
            '--is_slide',
            dest='is_slide',
            help='Whether to prediction by sliding window',
            action='store_true')
        parser.add_argument(
            '--crop_size',
            dest='crop_size',
            nargs=2,
            help='The crop size of sliding window, the first is width and the second is height.',
            type=int,
            default=None)
        parser.add_argument(
            '--stride',
            dest='stride',
            nargs=2,
            help='The stride of sliding window, the first is width and the second is height.',
            type=int,
            default=None)
        # custom color map
        parser.add_argument(
            '--custom_color',
            dest='custom_color',
            nargs='+',
            help='Save images with a custom color map. Default: None, use paddleseg\'s default color map.',
            type=int,
            default=None)
        # set device
        parser.add_argument(
            '--device',
            dest='device',
            help='Device place to be set, which can be GPU, XPU, NPU, CPU',
            default='gpu',
            type=str)
        return parser.parse_args()
    def get_test_config(cfg, args):
        test_config = cfg.test_config
        if 'aug_eval' in test_config:
            test_config.pop('aug_eval')
        if args.aug_pred:
            test_config['aug_pred'] = args.aug_pred
            test_config['scales'] = args.scales
        if args.flip_horizontal:
            test_config['flip_horizontal'] = args.flip_horizontal
        if args.flip_vertical:
            test_config['flip_vertical'] = args.flip_vertical
        if args.is_slide:
            test_config['is_slide'] = args.is_slide
            test_config['crop_size'] = args.crop_size
            test_config['stride'] = args.stride
        if args.custom_color:
            test_config['custom_color'] = args.custom_color
        return test_config


    try:
        while not exit_flag:
            #1분간 영상을 촬영하고, 충격감지 이벤트를 기록
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
            
            #저장한 1분간의 영상에 대한 추론(Semantic Segmentation)

            args = parse_args()
            env_info = get_sys_env()
            if args.device == 'gpu' and env_info[
                    'Paddle compiled with cuda'] and env_info['GPUs used']:
                place = 'gpu'
            elif args.device == 'xpu' and paddle.is_compiled_with_xpu():
                place = 'xpu'
            elif args.device == 'npu' and paddle.is_compiled_with_npu():
                place = 'npu'
            else:
                place = 'cpu'
            paddle.set_device(place)
            if not args.cfg:
                raise RuntimeError('No configuration file specified.')
            cfg = Config(args.cfg)
            msg = '\n---------------Config Information---------------\n'
            msg += str(cfg)
            msg += '------------------------------------------------'
            logger.info(msg)
            model = cfg.model
            transforms = Compose(cfg.val_transforms)
            image_list, image_dir = get_image_list(args.image_path)
            logger.info('Number of predict images = {}'.format(len(image_list)))
            test_config = get_test_config(cfg, args)
            predict(
                model,
                model_path=args.model_path,
                transforms=transforms,
                image_list=image_list,
                image_dir=image_dir,
                save_dir=args.save_dir,
                **test_config)



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




def test():
    global exit_flag
    while not exit_flag:
        temp = input()
        if temp == "a":
            playsound("mp3/Street_danger_left.mp3")
        elif temp == 'b':
            playsound("mp3/obstacle_left.mp3")
        elif temp == 'c':
            playsound("mp3/collison_detect.mp3")
        


        


def main():
    global exit_flag
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST,PORT))

    modelA_process = None


    while True:
        signal = client_socket.recv(1024).decode()

        if signal =="B":
            exit_flag = False
            print("Starting Model A")

            if modelA_process is None or not modelA_process.is_alive():
                modelA_process = Thread(target=test())
                modelA_process.start()
            else:
                print("model A is already running")
        elif signal == 'A':
            exit_flag = True
            print("Model B Terminated!")
        elif signal == 'Q':
            client_socket.close()
 


    client_socket.close()

if __name__ == '__main__':
    main()


        


