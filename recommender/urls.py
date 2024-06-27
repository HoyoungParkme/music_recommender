from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from recommender import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('face_recognition/', views.face_recognition, name='face_recognition'),
    path('camera_window/', views.camera_window, name='camera_window'),
    path('capture_face/', views.capture_face, name='capture_face'),  # 추가된 경로
    path('my_emotions/', views.my_emotions, name='my_emotions'),  # 새 페이지 경로 추가
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)