# 需要安装pillow库
from PIL import Image
import os
import glob


def batch_resize_images(input_folder, output_folder, max_width, max_height, output_format='jpg'):
    """
    批量调整文件夹中所有图片的尺寸，保持原始宽高比，并可指定输出格式。
    图片会被等比缩放，以适应 (max_width, max_height) 的边界框。

    :param input_folder: 包含原始图片的文件夹路径。
    :param output_folder: 保存调整后图片的文件夹路径。
    :param max_width: 目标宽度的最大值。
    :param max_height: 目标高度的最大值。
    :param output_format: 目标输出格式的后缀名 (例如 'png', 'jpeg')。
    """
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

    for index, file_path in enumerate(image_files):
        file_name = os.path.basename(file_path)
        try:
            with Image.open(file_path) as img:
                # --- 核心改进：保持宽高比进行缩放 ---
                img.thumbnail((max_width, max_height))
                img_resized = img

                # --- 文件名和路径处理 ---
                file_name_without_ext = os.path.splitext(file_name)[0]
                new_file_name = f"{file_name_without_ext}.{output_format.lower()}"
                output_path = os.path.join(output_folder, new_file_name)

                # --- 透明通道处理，现在更加健壮 ---
                # 如果原图有透明度('P'模式的透明或'RGBA')且要保存为JPG，则转换为RGB
                if output_format.lower() in ['jpg', 'jpeg']:
                    if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                        print(f"  (提示: {file_name} 包含透明通道, 已转换为RGB格式进行保存)")
                        # 使用一个白色背景进行填充
                        img_resized = Image.new("RGB", img.size, (255, 255, 255))
                        img_resized.paste(img, (0, 0), img.getchannel('A') if img.mode == 'RGBA' else None)

                # 保存为指定格式
                img_resized.save(output_path)
                print(
                    f"({index + 1}/{len(image_files)}) 已处理: {file_name} -> {new_file_name} (尺寸: {img_resized.size})")

        except Exception as e:
            print(f"处理文件 {file_name} 时出错: {e}")

    print("\n所有图片处理完成！")


# --- 使用示例 ---
if __name__ == "__main__":
    """
    提示：脚本会将图片等比例缩放，确保其宽度不超过 target_max_width，高度不超过 target_max_height。
    """
    input_directory = 'input_images'
    output_directory = 'output_images_resized'

    # 设置目标尺寸的最大边界
    target_max_width = 800
    target_max_height = 600

    # 定义你想要的输出格式
    target_format = 'png'

    batch_resize_images(input_directory, output_directory, target_max_width, target_max_height, target_format)