# Create your views here.
import os
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse

# /index
def index(request):
    video_dir = os.path.join(settings.MEDIA_ROOT, 'videos')
    video_files = [f for f in os.listdir(video_dir) if f.endswith(('mp4', 'avi', 'mkv'))]
    # print(video_files)
    return render(request, 'videos/index.html', {'videos': video_files})

# 显示视频页面
def play_video(request, filename):
    # video_path = os.path.join(settings.MEDIA_URL, 'videos', filename)
    # print(video_path)
    return render(request, 'videos/play_video.html', {'video_path': filename})

# 返回视频流文件
def stream_video(request, filename):
    video_path = os.path.join(settings.MEDIA_ROOT, 'videos', filename)
    video_file = open(video_path, 'rb')

    # 获取 Range 请求头（例如，Range: bytes=0-99999
    # 这个请求头用于网页内置的视频播放，当拖动进度条时，会返回 bytes=num1-num2
    # num1 为视频流开始的文件指针位置， num2 为文件指针的末尾, 一般来说 num2 基本上为空
    range_header = request.META.get('HTTP_RANGE', None)
    # print(range_header)
    if range_header:
        # 解析 Range 头部
        byte1, byte2 = range_header.split('=')[1].split('-')
        byte1 = int(byte1)
        byte2 = int(byte2) if byte2 else byte1 + 1024 * 1024  # 默认 1MB
        # 二进制文件对象.seek() 用与返回从指定文件指针开始的二进制文件
        video_file.seek(byte1)
        data = video_file.read(byte2 - byte1)
        response = HttpResponse(data, content_type='video/mp4')
        response['Content-Range'] = f'bytes {byte1}-{byte2}/{os.path.getsize(video_path)}'
        response.status_code = 206
    else:
        # 没有 Range 头时就返回整个文件
        video_file.seek(0)
        response = HttpResponse(video_file.read(), content_type='video/mp4')

    video_file.close()
    return response