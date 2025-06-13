# Python 实用工具脚本合集 (Python Utility Scripts)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

这是一个用于存放和分享各类实用Python脚本的仓库，专注于通过自动化脚本解决常见的数字媒体处理任务，例如图像处理、音视频下载与编辑等。

## 功能脚本列表

| 脚本文件名 | 功能描述 | 主要依赖 |
| :--- | :--- | :--- |
| `修改照片大小.py` | 批量修改指定文件夹内所有图片的尺寸，并可统一输出为指定格式。 | `Pillow` |
| `视频声音分离.py` | 批量从指定文件夹的视频文件中提取音轨，并保存为独立的MP3音频文件。 | `moviepy` |
| `下载B站视频.py` | 下载指定的Bilibili视频，可选择性地抓取并内嵌官方字幕。 | `yt-dlp`, **FFmpeg** |

---

## 快速上手：环境准备与安装

在运行这些脚本前，请确保您的电脑已安装 **Python 3.8 或更高版本**。

### 步骤 1: 克隆项目

将整个项目克隆到您的本地：
```bash
git clone https://github.com/Maverick-666/Python-utility-script.git
cd Python-utility-script
```

### 步骤 2: (推荐) 创建虚拟环境

为了不污染您的主Python环境，强烈建议您创建一个虚拟环境。

```bash
# 创建一个名为 venv 的虚拟环境
python -m venv venv

# 激活虚拟环境
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 步骤 3: 安装所有Python依赖

本项目的所有Python库依赖已记录在 `requirements.txt` 文件中。使用以下命令一键安装：

```bash
pip install -r requirements.txt
```

---

## 脚本使用指南

### 1. `下载B站视频.py`

此脚本用于下载B站视频，并能自动合并音视频、内嵌字幕。

#### **⚠️ 最重要的外部依赖：FFmpeg**

此脚本**强依赖** `FFmpeg` 来合并B站下载的高清音视频流和字幕。**必须先在您的系统中正确安装FFmpeg。**

1.  **不要**下载源代码，请直接下载**预编译好的程序 (Executable/Binary)**。
2.  **推荐下载地址**: [Gyan.dev](https://www.gyan.dev/ffmpeg/builds/) (下载 `ffmpeg-release-full.zip`)。
3.  **安装方法**:
    *   解压下载的 `.zip` 文件。
    *   进入解压后的文件夹，找到 `bin` 目录。
    *   将这个 `bin` 目录的**完整路径**添加到您操作系统的**系统环境变量 `Path`** 中。
    *   **验证安装**: **重启**你的命令行工具或IDE，输入 `ffmpeg -version`，如果能看到版本信息，则表示安装成功。

#### **使用方法:**

1.  **打开** `下载B站视频.py` 文件。
2.  **修改**文件末尾 `if __name__ == "__main__":` 部分的参数：
    *   `target_video_url`: 将其值替换为您想下载的B站视频的完整URL。
    *   `save_path`: 指定视频的保存路径，默认为 `./` (当前目录)。
    *   `download_subtitle`:
        *   设置为 `True`：会尝试下载官方中文字幕并内嵌到视频中。
        *   设置为 `True`：只下载纯净的音视频。
3.  **运行脚本**:
    ```bash
    python 下载B站视频.py
    ```
4.  **提示**: 对于需要登录或VIP才能观看的高清视频，您可能需要配置Cookie。请参考`yt-dlp`文档中的 `cookiefile` 选项。

### 2. `修改照片大小.py`

此脚本用于批量处理图片尺寸和格式。

#### **使用方法:**

1.  **创建输入文件夹**: 在项目根目录创建一个名为 `input_images` 的文件夹，并将您所有待处理的图片放入其中。
2.  **打开** `修改照片大小.py` 文件。
3.  **修改**文件末尾 `if __name__ == "__main__":` 部分的参数：
    *   `input_directory`: 确认其值为 `'input_images'` 或您自定义的输入文件夹名。
    *   `output_directory`: 指定处理后的图片存放的文件夹名（脚本会自动创建）。
    *   `target_width` 和 `target_height`: 设置您想要的目标宽度和高度。
    *   `target_format`: 设置输出图片的格式，例如 `'png'`, `'jpg'`, `'bmp'`。
4.  **运行脚本**:
    ```bash
    python 修改照片大小.py
    ```
    处理完成的图片将保存在您指定的输出文件夹中。

### 3. `视频声音分离.py`

此脚本用于批量从视频中提取音频并存为MP3。

#### **使用方法:**

1.  **创建输入文件夹**: 在项目根目录创建一个名为 `input_videos` 的文件夹，并将您的视频文件（如.mp4, .mkv）放入其中。
2.  **打开** `视频声音分离.py` 文件。
3.  **修改**文件末尾 `if __name__ == "__main__":` 部分的参数：
    *   `input_directory`: 确认其值为 `'input_videos'` 或您自定义的输入文件夹名。
    *   `output_directory`: 指定提取出的音频存放的文件夹名（脚本会自动创建）。
4.  **运行脚本**:
    ```bash
    python 视频声音分离.py
    ```
    提取出的 `.mp3` 文件将保存在您指定的输出文件夹中。

---

## 如何贡献

欢迎您为这个项目贡献代码！如果您有好的脚本想法或发现了问题，请随时：
1.  在本仓库提交一个 **Issue** 进行讨论。
2.  **Fork** 本仓库，完成修改后提交 **Pull Request**。

## 许可证

本项目采用 [MIT License](https://opensource.org/licenses/MIT) 许可证。