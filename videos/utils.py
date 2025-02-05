import os

import av
from PIL import Image

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

def generate_classified_thumbnail(video_folder_path, output_image_path, max_width=None, max_height=None):
    """
    用于生成分类项的缩略图，来自该分类下的图片，默认将6张图图片进行合并

    :param video_folder_path: 需要进行处理的文件夹，将该文件夹下前若干个图片进行合并（由pictures控制合并的图片个数)
    :param output_image_path: 输出地址
    :param max_width: 生成出来的图片宽度
    :param max_height: 生成出来的图片高度
    """
    try:
        # 获取文件夹下所有图片文件
        image_files = [f for f in os.listdir(video_folder_path) if f.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif'))]
        pictures_num = len(image_files) if len(image_files) < 6 else 6
        print(pictures_num)

        image_files = image_files[:pictures_num]  # 选择前 `pictures_num` 张图片

        if len(image_files) == 0:
            raise ValueError("文件夹中没有找到图片文件。")

        # 打开所有图片
        images = []
        for image_file in image_files:
            img_path = os.path.join(video_folder_path, image_file)
            img = Image.open(img_path)

            # 如果指定了最大宽高，按比例调整大小
            if max_width and max_height:
                img = img.resize((max_width, max_height))

            images.append(img)

        # 以下用于计算合成图片的网格布局, 成的图片由多个小图像组成，这些小图像被按行列的方式排布在一个大的画布上。
        grid_size = int(pictures_num ** 0.5)  # 为何使用平方根： 因为合成后的图片是一个矩形，如果图片数为6，那么6的平方根为2.45左右，那么取 2 ，就会有2*3的图片排列。
        # 计算网格的行列数
        if grid_size ** 2 < pictures_num:
            grid_size += 1  # 如果网格不足以容纳所有图片，增加行数

        # 计算合成图像的尺寸
        rows = grid_size  # 网格行数
        cols = (pictures_num + rows - 1) // rows  # 计算列数，确保网格可以容纳所有图片

        # 计算合成图片的宽度和高度
        thumbnail_width = max_width * cols if max_width else sum(img.width for img in images[:cols])
        thumbnail_height = max_height * rows if max_height else sum(img.height for img in images[:rows])

        # 创建一个空白图像来合并这些图片
        thumbnail = Image.new('RGB', (thumbnail_width, thumbnail_height), (255, 255, 255))  # 白色背景

        # 将图片按网格方式放入空白图像中
        x_offset, y_offset = 0, 0
        for i, img in enumerate(images):
            # 计算当前图片的行列位置
            row = i // cols
            col = i % cols

            # 将图片粘贴到合适的位置
            thumbnail.paste(img, (col * max_width, row * max_height))

        # 保存最终生成的缩略图
        thumbnail.resize((max_width, max_height)).save(output_image_path)
        print(f"生成的缩略图保存至: {output_image_path}")

    except Exception as e:
        print(f"发生错误: {e}")


if __name__ == '__main__':
    # 示例调用
    video_path = "/Users/wangzirui/Documents/workdir/python_projects/local_video_viewer/media/thumbnails/test"
    output_image_path = "thumbnail.jpg"
    width, height = 320, 180  # 缩略图尺寸（可根据需求调整）

    generate_classified_thumbnail(video_path, output_image_path, max_width=width, max_height=height)
