##################################################
'''
# 推荐直接运行本py程序

# 如果你非得用命令行，使用示例：
只复制种子文件
python main.py "git&github协作版本控制.md"

复制1层深度的关联文件
python main.py -n 1 "git&github协作版本控制.md"

复制所有关联文件
python main.py --all "git&github协作版本控制.md"

复制3层深度的多个种子文件
python main.py -n 3 "文件A.md" "文件B.md"
'''
##################################################


import sys
import re
import os
import shutil
import argparse

# 在文件操作前添加编码声明
sys.stdout.reconfigure(encoding='utf-8')  # Python 3.7+

VAULT_DIR = '../my_new_vault_dir'
notes_map = {}  # 存储文件名和路径的映射
all_files = []  # 存储所有文件的完整路径

def populate_notes_map():
    """构建完整的文件名-路径映射表"""
    global all_files
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 遍历所有文件和子目录
    for root, dirs, files in os.walk(base_dir):
        for name in files:
            # 获取文件完整路径
            full_path = os.path.join(root, name)
            # 获取文件相对路径
            rel_path = os.path.relpath(full_path, base_dir)
            
            # 存储文件路径
            all_files.append(full_path)
            
            # 存储多种映射方式
            notes_map[name] = rel_path  # 完整文件名映射
            notes_map[os.path.splitext(name)[0]] = rel_path  # 不带扩展名的映射
            notes_map[rel_path] = rel_path  # 相对路径映射
            notes_map[full_path] = rel_path  # 完整路径映射
            notes_map[os.path.normpath(full_path)] = rel_path  # 规范化路径映射

def get_connected_components(seeds, max_depth=None):
    """
    获取所有关联笔记
    :param seeds: 种子文件列表
    :param max_depth: 最大链接深度 (None 表示无限深度)
    :return: 所有关联笔记的列表
    """
    seen = set()
    # 使用元组 (文件路径, 当前深度)
    queue = [(seed, 0) for seed in seeds]
    
    while queue:
        fn, depth = queue.pop(0)
        
        # 检查是否达到深度限制
        if max_depth is not None and depth > max_depth:
            continue
            
        if fn in seen:
            continue
        
        # 尝试找到文件的真实路径
        real_path = None
        for possible_key in [fn, os.path.normpath(fn)]:
            if possible_key in notes_map:
                real_path = notes_map[possible_key]
                break
        
        if not real_path:
            print(f"⚠️ 警告: 无法找到文件 {fn} 的映射")
            continue
        
        # 添加到已访问集合
        seen.add(real_path)
        
        # 获取出站链接
        outgoing_links = get_links(real_path)
        
        # 将新链接加入队列
        for link in outgoing_links:
            if link not in seen:
                queue.append((link, depth + 1))
    
    return list(seen)

def get_links(filename: str):
    """获取文件中的所有链接，支持各种格式"""
    if not os.path.isfile(filename):
        return []
    
    # 新增文件类型过滤逻辑
    allowed_extensions = ['.md', '.txt']  # 允许处理的文件类型
    file_ext = os.path.splitext(filename)[1].lower()
    if file_ext not in allowed_extensions:
        return []  # 直接跳过非文本文件
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            note = f.read()
    except UnicodeDecodeError:
        try:
            with open(filename, 'r', encoding='gbk') as f:
                note = f.read()
        except:
            print(f"⚠️ 无法读取文件: {filename}")
            return []
    
    # 匹配所有 [[...]] 格式的链接
    pattern = r'\[\[(.*?)\]\]'
    raw_matches = re.findall(pattern, note)
    
    found_links = []
    for raw_link in raw_matches:
        # 提取基础文件名（去除锚点和块引用）
        base_name = re.sub(r'[\#\^].*$', '', raw_link).strip()
        
        # 处理带别名的链接 [[文件名|别名]]
        if '|' in base_name:
            base_name = base_name.split('|')[0].strip()
        
        # 跳过空文件名
        if not base_name:
            continue
            
        # 尝试多种可能的键值
        possible_keys = [
            base_name + '.md',          # 带扩展名
            base_name,                   # 不带扩展名
            os.path.normpath(base_name)  # 规范化路径
        ]
        
        matched = False
        for key in possible_keys:
            if key in notes_map:
                found_links.append(notes_map[key])
                matched = True
                break
        
        if not matched:
            print(f"⚠️ 未找到链接映射: {base_name} (来自链接: [[{raw_link}]])")
    
    return found_links

def make_new_vault(target_notes):
    """创建新的知识库，复制所有目标笔记"""
    if not os.path.exists(VAULT_DIR):
        os.makedirs(VAULT_DIR, exist_ok=True)  # 使用exist_ok更安全
    
    for note in target_notes:
        try:
            # 查找文件的真实路径
            real_path = None
            for possible_key in [note, os.path.normpath(note)]:
                if possible_key in notes_map:
                    real_path = notes_map[possible_key]
                    break
            
            if not real_path:
                print(f"⚠️ 警告: 无法找到文件 {note} 的映射")
                continue
                
            # 构建源路径
            script_dir = os.path.dirname(os.path.abspath(__file__))
            src_path = os.path.join(script_dir, real_path)
            
            if not os.path.exists(src_path):
                print(f"⚠️ 警告: 源文件不存在 - {src_path}")
                continue
                
            # 处理目标路径
            note_dir = os.path.dirname(real_path) or '.'  # 使用真实路径的目录
            rel_note_dir = os.path.relpath(note_dir, start='.')
            dest_dir = os.path.join(VAULT_DIR, rel_note_dir)
            
            # 创建目录
            os.makedirs(dest_dir, exist_ok=True)
            
            dest_path = os.path.join(dest_dir, os.path.basename(real_path))
            
            # 执行复制
            shutil.copy(src_path, dest_path)
            print(f"✅ 已复制: {os.path.basename(real_path)}")
            
        except Exception as e:
            # 增强的错误日志
            print(f"\n❌ 严重错误: 复制 {note} 失败")
            print(f"   源文件: {src_path}")
            print(f"   目标位置: {dest_path}")
            print(f"   错误类型: {type(e).__name__}")
            print(f"   错误详情: {str(e)}")
            print("   建议操作: 检查文件名特殊字符或路径权限")

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='复制Obsidian笔记及其链接')
    parser.add_argument('seeds', nargs='*', help='种子文件列表')
    parser.add_argument('-n', '--depth', type=int, default=None, 
                        help='复制深度 (默认: 无限深度)')
    parser.add_argument('--all', action='store_true', 
                        help='复制所有关联文件 (无限深度)')
    return parser.parse_args()

def interactive_mode():
    """交互模式：提示用户输入文件名和深度"""
    print("\n===== Obsidian笔记复制工具 =====")
    
    # 获取文件名 - 支持分号分隔
    files = []
    while not files:
        print("请输入文件名（多个文件用两个分号分隔，如：文件1.md；；文件2.md）")
        input_str = input("文件名: ").strip()
        
        if not input_str:
            print("⚠️ 输入不能为空，请重新输入")
            continue
            
        # 使用正则表达式分割输入，支持中英文分号（；;）和前后空格
        input_files = re.split(r'[；;]{2}', input_str)
        
        # 清理每个文件名：去除前后空格，过滤空值
        files = [f.strip() for f in input_files if f.strip()]
        
        if not files:
            print("⚠️ 至少需要一个有效的文件名，请重新输入")
    
    # 获取深度
    depth = None
    while True:  # 修改为无限循环，直到获取有效输入
        depth_input = input("深度（全部深度填a，数字表示层数，回车表示0）: ").strip().lower()
        
        if depth_input == 'a':
            depth = None  # 无限深度
            break  # 添加 break 跳出循环
        elif depth_input == '':
            depth = 0  # 默认深度0
            break  # 添加 break 跳出循环
        else:
            try:
                depth = int(depth_input)
                if depth < 0:
                    print("⚠️ 深度不能为负数，请重新输入")
                else:
                    break  # 有效数字，跳出循环
            except ValueError:
                print("⚠️ 请输入有效数字或'a'，请重新输入")
    
    return files, depth

if __name__ == '__main__':
    # 构建映射表
    populate_notes_map()
    print(f"找到 {len(all_files)} 个文件")
    
    # 检查是否有命令行参数
    if len(sys.argv) > 1:
        args = parse_arguments()
        seeds = args.seeds
        max_depth = args.depth
        
        if args.all:
            max_depth = None
            print("🔍 模式: 复制所有关联文件 (无限深度)")
        elif max_depth is not None:
            print(f"🔍 模式: 复制 {max_depth} 层深度的关联文件")
        else:
            print("🔍 模式: 只复制种子文件 (深度0)")
    else:
        # 进入交互模式
        seeds, max_depth = interactive_mode()
        depth_display = "无限深度" if max_depth is None else f"{max_depth}层深度"
        print(f"\n🔍 模式: 复制{depth_display}的关联文件")
    
    # 验证种子文件
    valid_seeds = []
    for seed in seeds:
        # 尝试多种方式查找文件
        found = False
        for key in [seed, os.path.normpath(seed), seed + '.md']:
            if key in notes_map:
                valid_seeds.append(notes_map[key])
                found = True
                break
        
        if not found:
            print(f"⚠️ 警告: 未找到种子文件 - {seed}")
    
    if not valid_seeds:
        print("❌ 错误: 没有有效的种子文件")
        sys.exit(1)
    
    print(f"使用种子文件: {valid_seeds}")
    target_notes = get_connected_components(valid_seeds, max_depth=max_depth)
    
    # 统计结果
    seed_count = len(valid_seeds)
    linked_count = len(target_notes) - seed_count
    print(f"📊 统计: {seed_count} 个种子文件 + {linked_count} 个关联文件")
    print(f'创建新知识库在: {VAULT_DIR}/')
    make_new_vault(target_notes)
