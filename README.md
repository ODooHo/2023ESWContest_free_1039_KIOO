# ABAS Project : Adavanced Blind Assistance System

운전자가 안전하고 편리한 주행을 할 수 있도록 하는 전방 충돌방지 보조, 차선이탈방지 보조 등의 기능을 **ADAS**, 첨단 운전자 보조 시스템이라고 합니다.

이 보조시스템에 착안하여 보행하는 시각장애인에게 적용하면 어떨까라는 생각으로 시작됐습니다.

따라서 상품 인지 보조, 보행 보조 기능을 하는 **ABAS**, 첨단 시각장애인 보행 보조 시스템을 개발하게 되었습니다.

<img width="322" alt="image" src="https://github.com/yhoons/2023ESWContest_free/assets/79200729/4f233bae-9242-4d93-9d19-6f72980ab210">


## Contents

1. Key Actions

2. Requirements

3. Repository Tree
4. Docker
5. Team
6. Reference



## Key Actions

Object Detection

Semantic Segmentation

Application

- Product Registration
- Gait record
![process drawio](https://github.com/yhoons/2023ESWContest_free/assets/79200729/c99b9df6-d160-4856-8ff1-3db4b701e6e0)



## Requirements

##### Jetson nano (Local)

- Ubuntu 20.04(aarch64)
- Jetpack 4.6.1

##### Dell 5521 G15 (Server)

- Ubuntu 20.04
- Docker(more details)



## Repository Tree

```
📦2023ESWContest_free_1039_KIOO
 ┣ 📂Algorithm												//개별 기능 구현 테스트 폴더
 ┃ ┣ 📜.DS_Store
 ┃ ┣ 📜button.py
 ┃ ┣ 📜recording_video.py
 ┃ ┣ 📜sftp_to_server.py
 ┃ ┗ 📜vib.py
 ┣ 📂Architecture											//상품 등록 시각화 폴더
 ┃ ┣ 📜.$상품등록:상세:수정 폼.drawio.bkp
 ┃ ┣ 📜.$영상 상세.drawio.bkp
 ┃ ┣ 📜.DS_Store
 ┃ ┣ 📜상품 저장 성공(검증 과정).drawio
 ┃ ┣ 📜상품 저장 실패(검증 과정).drawio
 ┃ ┣ 📜상품등록:상세:수정 폼 + 영상.drawio
 ┃ ┣ 📜영상 상세.drawio
 ┃ ┗ 📜웹 기술구성도.drawio
 ┣ 📂KIOO_Application									//KIOO앱 구현
 ┃ ┣ 📂.idea
 ┃ ┃ ┣ 📜KIOO_Application.iml
 ┃ ┃ ┣ 📜modules.xml
 ┃ ┃ ┗ 📜workspace.xml
 ┃ ┣ 📂Event
 ┃ ┃ ┣ 📜.DS_Store
 ┃ ┃ ┗ 📜event1.mp4
 ┃ ┣ 📂KIOO
 ┃ ┃ ┣ 📂gradle
 ┃ ┃ ┃ ┗ 📂wrapper
 ┃ ┃ ┃ ┃ ┣ 📜gradle-wrapper.jar
 ┃ ┃ ┃ ┃ ┗ 📜gradle-wrapper.properties
 ┣ 📂abas_software									//ABAS 작동 코드
 ┃ ┣ 📜clientA.py
 ┃ ┣ 📜clientB.py
 ┃ ┣ 📜darknet_video_test.py
 ┃ ┣ 📜prac_model_switch.py
 ┃ ┣ 📜prac_model_v3.py
 ┃ ┣ 📜recording_event.py
 ┃ ┣ 📜server.py
```



## Team

|             [오두호](https://github.com/ODooHo)              |             [서영훈](https://github.com/yhoons)              |
| :----------------------------------------------------------: | :----------------------------------------------------------: |
| <img src="https://avatars.githubusercontent.com/u/57125819?v=4" alt="img" style="zoom:20%"/> | <img src="https://avatars.githubusercontent.com/u/79200729?v=4" alt="img" style="zoom:20%"/> |

## Reference

- [yolov3 paper](https://arxiv.org/abs/1804.02767)
- [Object-Detection](https://github.com/2damin/yolov3-pytorch) - yolov3 training

- [Segmentation](https://github.com/PaddlePaddle/PaddleSeg) - Paddleseg
- [KITTI Data](https://www.cvlibs.net/datasets/kitti/eval_object.php?obj_benchmark=2d)
