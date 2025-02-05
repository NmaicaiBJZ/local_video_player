# Create your views here.
import os
from os.path import exists

from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from .utils import generate_thumbnail_pyav


# /
def index(request):
    video_folders, video_files = file_processing("")

    return render(request, 'videos/index.html', {"video_folders": video_folders, "video_files": video_files})

def video_folder_view(request, file_path):
    video_folders, video_files = file_processing(file_path)

    return render(request, 'videos/index.html', {"video_folders": video_folders, "video_files": video_files})

def file_processing(file_location):
    """
    不再试图处理范围内，用于index与video_folder_view视图函数来调用
    将传入a标签中的ulr地址进行处理，如 localhost/video_folder_view/test/afs 这是个具体的url，其中传入的file_location为 /test/afs
    要做的就是获取 /media/videos/test/afs 文件夹中的内容，返回该文件夹下的文件夹列表和文件列表
    同时需要在 thumbnails的/test/afs 文件夹中创建相同的文件结构，如果是文件夹创建文件夹，如果是文件如 11.mp4 就需要创建相同的图片
    :param file_location: url文件夹路径
    :return: 返回两个参数，分别人文件夹 与文件 列表
    """
    file_location = file_location

    # 创建文件根目录，降低耦合
    base_video_dir = os.path.join(settings.MEDIA_ROOT, 'videos')
    base_thumbnail_dir = os.path.join(settings.MEDIA_ROOT, 'thumbnails')
    os.makedirs(base_video_dir, exist_ok=True)
    os.makedirs(base_thumbnail_dir, exist_ok=True)

    # 获取文件地址 如 /media/videos/test/afs
    folder_path = os.path.join(base_video_dir, file_location)
    # 获取相同的缩略图文件夹路径结构 /media/thumbnails/test/afs
    thumbnail_folder_path = os.path.join(base_thumbnail_dir, file_location)
    os.makedirs(thumbnail_folder_path, exist_ok=True)
    # print(folder_path)
    # print(thumbnail_folder_path)

    # 区分mp4与文件夹
    video_folders = []
    video_files = []
    for f in os.listdir(folder_path):
        # 遍历文件夹中的地址 如果是 mp4文件 /···/media/videos/test/afs/111.mp4
        f_path = os.path.join(folder_path, f)
        # 该文件的url地址 如 /test/afs/111.mp4 或者 /test/afs/aa
        url_path = os.path.join(file_location, f)

        if f.endswith('.mp4'):
            thumbnail_picture_path = os.path.join(thumbnail_folder_path, f.split('.')[0] + '.jpg')
            if not os.path.exists(thumbnail_picture_path):
                # print("执行！")
                generate_thumbnail_pyav(f_path, thumbnail_picture_path, 300, 200)
            insert_text = {
                "file_name": f.split('/')[-1],
                "file_path": url_path,
                "thumbnail_path": os.path.join(settings.MEDIA_URL, 'thumbnails', url_path.split('.')[0] + '.jpg')
            }
            video_files.append(insert_text)
        elif os.path.isdir(f_path):
            video_folders.append(url_path)

    return video_folders, video_files


# 显示视频页面
def play_video(request, filename):
    print(filename)
    return render(request, 'videos/play_video.html', {'video_path': filename, 'current_path': os.path.dirname(filename)})

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
