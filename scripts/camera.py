import cv2
import os

def capture_face(save_path='data/camera/'):
    # 얼굴 검출을 위한 haarcascade 로드
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # 카메라 시작
    cap = cv2.VideoCapture(0)

    # 화면 크기 설정
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    center_x, center_y = frame_width // 2, frame_height // 2

    # 얼굴 틀 크기 설정
    box_width, box_height = 200, 200

    while True:
        # 프레임 읽기
        ret, frame = cap.read()

        # 흑백으로 변환
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 얼굴 검출
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # 얼굴에 사각형 그리기
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # 중앙에 얼굴 틀 그리기
        cv2.rectangle(frame, 
                      (center_x - box_width // 2, center_y - box_height // 2), 
                      (center_x + box_width // 2, center_y + box_height // 2), 
                      (0, 255, 0), 2)

        # 안내 문구 표시
        cv2.putText(frame, 'Please look at the camera', 
                    (center_x - box_width // 2, center_y - box_height // 2 - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

        # 결과 프레임 표시
        cv2.imshow('Face Detection', frame)

        # 'q' 키를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # 얼굴이 중앙에 위치하면 사진 저장
        for (x, y, w, h) in faces:
            if (center_x - box_width // 2 < x < center_x + box_width // 2 and 
                center_y - box_height // 2 < y < center_y + box_height // 2):
                face_img = frame[y:y+h, x:x+w]
                if not os.path.exists(save_path):
                    os.makedirs(save_path)
                img_path = os.path.join(save_path, 'detected_face.jpg')
                cv2.imwrite(img_path, face_img)
                print(f"Face detected and saved as '{img_path}'")

                # 찍힌 사진을 보여줌
                cv2.imshow('Captured Face', face_img)
                cv2.putText(face_img, 'Press "s" to save or "r" to retake', (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.imshow('Captured Face', face_img)

                key = cv2.waitKey(0) & 0xFF
                if key == ord('s'):
                    # 저장하고 종료
                    print(f"Photo saved as '{img_path}'")
                    cap.release()
                    cv2.destroyAllWindows()
                    return
                elif key == ord('r'):
                    # 다시 찍기
                    print("Retaking photo...")
                    break

    # 카메라 해제 및 창 닫기
    cap.release()
    cv2.destroyAllWindows()

capture_face()