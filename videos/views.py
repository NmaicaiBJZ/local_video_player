from django.shortcuts import render

# Create your views here.

import os
from django.shortcuts import render
from django.conf import settings


def index(request):
    video_dir = os.path.join(settings.MEDIA_ROOT, 'videos')
    video_files = [f for f in os.listdir(video_dir) if f.endswith(('mp4', 'avi', 'mkv'))]
    # print(video_files)
    return render(request, 'videos/index.html', {'videos': video_files})


def play_video(request, filename):
    video_path = os.path.join(settings.MEDIA_URL, 'videos', filename)
    # print(video_path)
    return render(request, 'videos/play_video.html', {'video_path': video_path})