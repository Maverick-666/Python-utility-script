# 需要安装moviepy库
import os
import glob
from moviepy.editor import VideoFileClip


def batch_extract_audio(input_folder, output_folder):
    """
    批量从指定文件夹中的所有视频提取音频，并保存到输出文件夹。

    :param input_folder: 包含视频文件的输入文件夹路径。
    :param output_folder: 用于保存提取出的音频文件的输出文件夹路径。
    """
    # 1. 检查并创建输出文件夹
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"已创建输出文件夹: {output_folder}")

    # 2. 查找所有支持格式的视频文件
    supported_formats = ["*.mp4", "*.avi", "*.mov", "*.mkv", "*.webm"]
    video_files = []
    for fmt in supported_formats:
        # 使用glob查找匹配格式的视频文件并添加到列表
        video_files.extend(glob.glob(os.path.join(input_folder, fmt)))[3]

    if not video_files:
        print(f"在文件夹 '{input_folder}' 中未找到支持的视频文件。")
        return

    print(f"找到 {len(video_files)} 个视频文件，开始处理...")

    # 3. 遍历并处理每一个视频文件
    for index, video_path in enumerate(video_files):
        # 获取纯文件名（不含扩展名）
        base_name = os.path.basename(video_path)
        file_name_without_ext = os.path.splitext(base_name)[0]

        # 定义输出音频文件的完整路径，格式为mp3
        output_audio_path = os.path.join(output_folder, f"{file_name_without_ext}.mp3")

        print(f"--- ({index + 1}/{len(video_files)}) 正在处理: {base_name} ---")

        try:
            # 使用VideoFileClip打开视频文件
            with VideoFileClip(video_path) as video:
                # 检查视频是否包含音频轨道
                if video.audio is None:
                    print(f"警告: 视频 '{base_name}' 不包含音频轨道，已跳过。")
                    continue

                # 提取音频并写入文件
                video.audio.write_audiofile(output_audio_path, logger=None)[1]
                print(f"成功提取音频 -> {output_audio_path}")

        except Exception as e:
            print(f"处理视频 '{base_name}' 时发生错误: {e}")

    print("\n所有视频处理完成！")


# --- 使用示例 ---
if __name__ == "__main__":
    # 指定输入文件夹，存放你的视频文件
    input_directory = "input_videos" # <-- 修改这里

    # 指定输出文件夹，用于存放分离出的音频文件
    # 您可以修改为任何绝对或相对路径，例如: r'C:\Users\YourName\Desktop\Extracted_Audio'
    output_directory = "output_audio" # <-- 修改这里

    # 调用批量处理函数
    batch_extract_audio(input_directory, output_directory)
