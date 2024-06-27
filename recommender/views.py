import os
import cv2
import numpy as np
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from tensorflow.keras.models import load_model

# 감정 예측 모델 로드
model = load_model(settings.MODEL_PATH)
emotion_labels = ['분노', '당황', '불안', '기쁨', '슬픔', '상처', '평범'] 

def index(request):
    return render(request, 'index.html')

def face_recognition(request):
    return render(request, 'face_recognition.html')

def camera_window(request):
    return render(request, 'camera_window.html')

def capture_face(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        image_path = os.path.join(settings.BASE_DIR, 'static/captured_image.jpg')

        # 이미지 파일 저장
        with open(image_path, 'wb+') as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)

        # 이미지 파일 읽기
        img = cv2.imread(image_path)
        if img is None:
            return JsonResponse({'success': False, 'error': '이미지를 읽을 수 없습니다.'})

        # 이미지 크기를 224x224로 조정하고, RGB로 변환
        resized_img = cv2.resize(img, (224, 224))
        rgb_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)

        # 모델 입력 형태로 변환
        face_img = rgb_img.astype('float32') / 255.0
        face_img = np.expand_dims(face_img, axis=0) 

        # 감정 예측 수행
        predictions = model.predict(face_img)
        emotion = emotion_labels[np.argmax(predictions)]

        return JsonResponse({'success': True, 'emotion': emotion, 'image_path': '/static/captured_image.jpg'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

def my_emotions(request):
    emotion = request.GET.get('emotion', 'unknown')
    image_path = request.GET.get('image_path', '')
    emotion_labels = ['분노', '당황', '불안', '기쁨', '슬픔', '상처', '평범']  
    return render(request, 'my_emotions.html', {'emotion': emotion, 'emotion_labels': emotion_labels, 'image_path': image_path})