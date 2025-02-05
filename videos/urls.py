from django.urls import path
from . import views

urlpatterns = [
    # /
    path('', views.index, name='index'),
    # /video_folder_view/<文件路径名>
    path('video_folder_view/<path:file_path>', views.video_folder_view, name='video_folder_view'),
    # /play/<文件名>
    path('play/<path:filename>/', views.play_video, name='play_video'),
    # /stream/<文件名> 用于对视频流文件进行动态传递
    path('stream/<path:filename>/', views.stream_video, name='stream_video'),
]
