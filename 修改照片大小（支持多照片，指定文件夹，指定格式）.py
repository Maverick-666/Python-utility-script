# 需要安装pillow库

from PIL import Image
import os
import glob


def batch_resize_images(input_folder, output_folder, width, height, output_format='jpg'):
    """
    批量调整文件夹中所有图片的尺寸，并可以指定输出格式。

    :param input_folder: 包含原始图片的文件夹路径。
    :param output_folder: 保存调整后图片的文件夹路径。
    :param width: 目标宽度 (a)。
    :param height: 目标高度 (b)。
    :param output_format: 目标输出格式的后缀名 (例如 'png', 'jpeg')。
    """
    # 1. 检查并创建输出文件夹
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"已创建输出文件夹: {output_folder}")

    supported_formats = ["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.gif"]
    image_files = []
    for fmt in supported_formats:
        image_files.extend(glob.glob(os.path.join(input_folder, fmt)))

    if not image_files:
        print(f"在文件夹 '{input_folder}' 中未找到支持的图片文件。")
        return

    print(f"找到 {len(image_files)} 张图片，开始处理...")

    # 2. 遍历所有找到的图片文件
    for index, file_path in enumerate(image_files):
        file_name = os.path.basename(file_path)
        try:
            with Image.open(file_path) as img:
                # 调整图片尺寸
                img_resized = img.resize((width, height))

                # --- 主要改动点 ---
                # 获取不带后缀的文件名
                file_name_without_ext = os.path.splitext(file_name)[0]
                # 构建新的、带指定后缀的文件名
                new_file_name = f"{file_name_without_ext}.{output_format}"
                output_path = os.path.join(output_folder, new_file_name)

                # 特殊处理：如果输出格式为jpg/jpeg，且原图有透明通道(RGBA)，则转换为RGB
                if output_format.lower() in ['jpg', 'jpeg']:
                    if img_resized.mode == 'RGBA':
                        print(f"  (提示: {file_name} 包含透明通道, 已转换为RGB格式进行保存)")
                        img_resized = img_resized.convert('RGB')

                # 保存为指定格式
                img_resized.save(output_path)
                print(f"({index + 1}/{len(image_files)}) 已处理: {file_name} -> {new_file_name}")

        except Exception as e:
            print(f"处理文件 {file_name} 时出错: {e}")

    print("所有图片处理完成！")


# --- 使用示例 ---
if __name__ == "__main__":
    """
    别忘了在下面改路径前加r，例如r'C:\Users\YourName\Desktop\1'
    """
    # 1. 设置输入文件夹
    input_directory = 'input_images' # <-- 修改这里

    # 2. 指定你的输出文件夹路径
    output_directory = 'output_images_converted' # <-- 修改这里

    # 3. 设置目标尺寸
    target_width = 800 # <-- 修改这里
    target_height = 600 # <-- 修改这里

    # 4. 新增：在这里定义你想要的输出格式 (例如 'png', 'jpeg', 'bmp', 'gif')
    target_format = 'png'  # <--- 修改这里来改变输出格式

    # 调用批量处理函数，并传入新的格式参数
    batch_resize_images(input_directory, output_directory, target_width, target_height, target_format)