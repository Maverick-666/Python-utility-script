# 需要安装moviepy库
import os
import glob
from moviepy import VideoFileClip


def batch_extract_audio(input_folder, output_folder, output_format="mp3"):
    """
    批量从指定文件夹中的所有视频提取音频，并保存到输出文件夹。

    :param input_folder: 包含视频文件的输入文件夹路径。
    :param output_folder: 用于保存提取出的音频文件的输出文件夹路径。
    :param output_format: 输出音频的格式, 如 'mp3', 'wav', 'ogg'。
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"已创建输出文件夹: {output_folder}")

    supported_formats = ["*.mp4", "*.avi", "*.mov", "*.mkv", "*.webm"]
    video_files = []
    for fmt in supported_formats:
        video_files.extend(glob.glob(os.path.join(input_folder, fmt)))

    if not video_files:
        print(f"在文件夹 '{input_folder}' 中未找到支持的视频文件。")
        return

    print(f"找到 {len(video_files)} 个视频文件，开始处理...")

    for index, video_path in enumerate(video_files):
        base_name = os.path.basename(video_path)
        file_name_without_ext = os.path.splitext(base_name)[0]

        # --- 核心改进：使用可配置的输出格式 ---
        output_audio_path = os.path.join(output_folder, f"{file_name_without_ext}.{output_format}")

        print(f"--- ({index + 1}/{len(video_files)}) 正在处理: {base_name} ---")

        try:
            with VideoFileClip(video_path) as video:
                if video.audio is None:
                    print(f"警告: 视频 '{base_name}' 不包含音频轨道，已跳过。")
                    continue

                # 提取音频并写入文件
                video.audio.write_audiofile(output_audio_path, logger=None)
                print(f"成功提取音频 -> {output_audio_path}")

        except Exception as e:
            print(f"处理视频 '{base_name}' 时发生错误: {e}")

    print("\n所有视频处理完成！")


# --- 使用示例 ---
if __name__ == "__main__":
    input_directory = "input_videos"
    output_directory = "output_audio"

    # --- 新增：在这里定义你想要的输出音频格式 ---
    target_audio_format = "mp3"  # 或者 "wav", "ogg"

    # 调用批量处理函数
    batch_extract_audio(input_directory, output_directory, target_audio_format)