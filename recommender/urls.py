from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from recommender import views

urlpatterns = [
    path('', views.index, name='index'),
    path('face_recognition/', views.face_recognition, name='face_recognition'),
    path('camera_window/', views.camera_window, name='camera_window'),
    path('capture_face/', views.capture_face, name='capture_face'),  
    path('my_emotions/', views.my_emotions, name='my_emotions'),  
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)