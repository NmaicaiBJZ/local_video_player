from django.urls import path
from . import views

urlpatterns = [
    # /index
    path('', views.index, name='index'),
    # /play/<文件名>
    path('play/<str:filename>/', views.play_video, name='play_video'),
    # /stream/<文件名> 用于对视频流文件进行动态传递
    path('stream/<str:filename>/', views.stream_video, name='stream_video'),
]
