import cv2

video_name = "output"
cap = cv2.VideoCapture('nvarguscamerasrc ! video/x-raw(memory:NVMM), width=640, height=480, format=(string)NV12, framerate=(fraction)20/1 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink', cv2.CAP_GSTREAMER)
tmp = 0
fourcc = cv2.VideoWriter_fourcc(*'mp4v')



recording = False

while(cap):
    
    ret, frame = cap.read()
    
    if not ret:
        break

    cv2.imshow('Video', frame)


    key = cv2.waitKey(1)

    # 'r' 키를 누르면 녹화 시작
    if key == ord('r') and not recording:
        out = cv2.VideoWriter("./output/"+ video_name + str(tmp) + ".mp4", fourcc, 20.0, (640, 480))
        recording = True
        
        
        print("녹화 시작")


    if recording:     
        out.write(frame)

    # 'q' 키를 누르면 녹화 종료
    if key == ord('q') and recording:
        recording = False
        tmp = tmp +1
        print("녹화종료")
        out.release()

    #프로그램 종
    if key == ord('z'):
        break  
cap.release()



cv2.destroyAllWindows()
