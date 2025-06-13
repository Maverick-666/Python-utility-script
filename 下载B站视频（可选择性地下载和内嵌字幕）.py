"""
使用指南：------------------------------------------------------------------------
pip install yt-dlp
ffmpeg部分请查看README文档
----------------------------------------------------------------------------------
"""

import yt_dlp
import sys


def download_bilibili_video(video_url, output_path='./', download_subtitle=False):
    """
    使用 yt-dlp 下载B站视频，并可选择性地下载和内嵌字幕。

    :param video_url: B站视频的URL。
    :param output_path: 视频保存的路径。
    :param download_subtitle: 布尔值。如果为True，则尝试下载中文字幕并内嵌到视频文件中。
    """
    # --- yt-dlp 基础配置选项 ---
    ydl_opts = {
        # 选择最佳画质的mp4视频和最佳音质的m4a音频进行合并
        # 'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        # 输出文件名模板，包含标题和UP主
        'outtmpl': f'{output_path}%(title)s - %(uploader)s.%(ext)s',
        # 对于需要登录才能观看高清视频或有地区限制的视频，需要配置cookie
        # 'cookiefile': 'path/to/your/cookies.txt',
        # 设置进度回调函数
        'progress_hooks': [progress_hook],
    }

    # --- 根据需求，动态添加字幕配置 ---
    if download_subtitle:
        print("-> 已启用字幕下载功能，将尝试下载并内嵌中文字幕。")
        subtitle_options = {
            'writesubtitles': True,  # 开启字幕下载
            'subtitleslangs': ['zh-Hans', 'zh-CN', 'zh'],  # 尝试的字幕语言列表（简体中文的多种代码）
            'writeautomaticsub': False,  # 不下载自动生成的字幕
            'embedsubtitles': True,  # **关键：将字幕内嵌到视频文件中**
        }
        # 将字幕选项更新到主配置中
        ydl_opts.update(subtitle_options)
    else:
        print("-> 未启用字幕下载功能。")

    print(f"准备下载: {video_url}")
    print(f"保存至: {output_path}")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print("\n下载完成!")
    except Exception as e:
        print(f"\n下载出错: {e}")
        # 在调试时，可以取消下面这行注释来查看完整的错误信息
        # traceback.print_exc()


def progress_hook(d):
    """进度条回调函数"""
    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
        downloaded_bytes = d.get('downloaded_bytes')

        if total_bytes and downloaded_bytes is not None:
            percent = downloaded_bytes / total_bytes * 100
            speed = d.get('speed')
            speed_str = f"{speed / 1024 / 1024:.2f} MiB/s" if speed else "N/A"
            eta = d.get('eta')
            eta_str = f"{int(eta)}s" if eta else "N/A"

            sys.stdout.write(
                f"\r -> 进度: {percent:.1f}% | "
                f"大小: {downloaded_bytes / 1024 / 1024:.2f}/{total_bytes / 1024 / 1024:.2f} MiB | "
                f"速度: {speed_str} | "
                f"ETA: {eta_str}"
            )
            sys.stdout.flush()

    elif d['status'] == 'finished':
        # 当下载完成后，yt-dlp会自动处理合并等后期工作
        if d.get('postprocessor') == 'Merger':
            print(f"\n音视频下载完成，正在合并...")
        elif d.get('postprocessor') == 'EmbedSubtitle':
            print(f"\n音视频已合并，正在内嵌字幕...")
        else:
            print(f"\n文件 {d['filename']} 处理完成。")


# --- 使用示例 ---
if __name__ == "__main__":
    # 请将下面的URL替换为你想下载的B站视频URL
    target_video_url = "https://www.bilibili.com/video/BV1Y3TTzCETb/?spm_id_from=333.1007.tianma.6-4-22.click"  # 示例URL

    # 指定保存视频的文件夹，'.' 表示当前文件夹
    save_path = './'

   # 确保视频本身有提供字幕，否则此功能无效
    print("\n" + "="*50)
    print("--- 开始下载任务（尝试内嵌字幕）---")
    # 你可以修改这里的 download_subtitle=False 来关闭字幕下载
    download_bilibili_video(target_video_url, save_path, download_subtitle=True)
    print("="*50)
