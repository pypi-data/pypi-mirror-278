from datetime import datetime
import time

import IndyCareConfig
import cv2

# RTSP 스트리밍 주소 설정
config = IndyCareConfig.load_config()
url = config[IndyCareConfig.RTSP]

VIDEO_FILE_DIR_PATH = "/home/user/IndyCare_Log/videos2/"

# 비디오 캡처 객체 생성
cap = cv2.VideoCapture(url)
rtsp_frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
rtsp_frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# time.sleep(1)
# cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
# cap.set(cv2.CAP_PROP_FPS, 20)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# 캡처 객체가 정상적으로 열렸는지 확인
if not cap.isOpened():
    print("RTSP 스트리밍 비디오를 불러올 수 없습니다.")
    exit()

new_record = True
codec = cv2.VideoWriter_fourcc(*'mp4v')  # *'xdiv' *'mp4v'
output_video = None
start_time = 0

# 비디오 캡처 루프 시작
while True:
    # 비디오 프레임 읽기
    ret, frame = cap.read()

    if new_record:
        now = datetime.now()
        video_name = VIDEO_FILE_DIR_PATH + now.strftime("%b_%d_%Y-%H_%M_%S.mp4")
        output_video = cv2.VideoWriter(video_name, codec, 24, (rtsp_frame_width, rtsp_frame_height))
        start_time = time.time()
        print("영상 기록 시작")
        new_record = False

    if time.time() - start_time <= 10:
        output_video.write(frame)
    else:
        output_video.release()
        new_record = True
        print("영상 저장 완료")
        break

    # 비디오 프레임이 제대로 읽혔는지 확인
    if not ret:
        print("비디오 프레임을 읽을 수 없습니다.")
        break

    # # 비디오 프레임 표시
    # cv2.imshow("RTSP Video", frame)
    #
    # # q 키를 누르면 종료
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

    time.sleep(1/2) if not True else time.sleep(1/200)

# 비디오 캡처 객체와 모든 창 닫기
cap.release()
cv2.destroyAllWindows()
