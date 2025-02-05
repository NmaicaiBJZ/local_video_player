import os

import av

from local_video_viewer import settings


def generate_thumbnail_pyav(video_path, output_image_path, max_width=None, max_height=None):
    """
    使用 PyAV 从视频中提取中间帧，并生成缩略图

    参数:
    - video_path (str): 视频文件路径
    - output_image_path (str): 输出图片路径
    - width (int): 缩略图的宽度（可选）
    - height (int): 缩略图的高度（可选）
    """
    try:
        # 打开视频文件
        container = av.open(video_path)
        # 获取该视频的视频流，视频文件不止有视频还有音频
        video_stream = container.streams.video[0]

        # print(video_stream.duration, video_stream.time_base)
        duration = video_stream.duration * video_stream.time_base  # PyAV 的时间基（time_base）
        middle_time = duration / 2  # 取视频中间时间点
        # print(middle_frame_number)
        # print(total_frames)

        # 跳到中间帧,需要告诉container要处理的是视频流
        container.seek(int(middle_time / video_stream.time_base), stream=video_stream)

        # 提取中间帧，container 是一个容器，通常包含多个流，decode将容器解码，对于视频流回返回一个帧对象，video 表示解码视频流第一个对象
        for frame in container.decode(video=0):
            # 将帧转换为图像
            image = frame.to_image()

            # 如果指定了缩略图尺寸，调整图像大小
            if max_width and max_height:
                # 按照最大尺寸等比缩放
                original_width, original_height = image.size
                # 计算缩放比例，确保宽度或高度不超过最大值
                scale_factor = min(max_width / original_width, max_height / original_height)
                new_width = int(original_width * scale_factor)
                new_height = int(original_height * scale_factor)
                image = image.resize((new_width, new_height))

            # 保存图像
            image.save(output_image_path)
            print(f"成功生成缩略图: {output_image_path}")
            break  # 只提取一帧
    except Exception as e:
        print(f"生成缩略图失败: {e}")

if __name__ == '__main__':
    # 示例调用
    video_path = "../media/videos/test/27771797894-1-192.mp4"
    output_image_path = "thumbnail.jpg"
    width, height = 320, 180  # 缩略图尺寸（可根据需求调整）

    generate_thumbnail_pyav(video_path, output_image_path)
