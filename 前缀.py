import os
import re


def remove_existing_prefix(filename):
    """
    移除文件名中的现有数字前缀
    """
    # 使用正则表达式匹配数字前缀，假设格式为 "数字_"
    new_filename = re.sub(r'^\d+_', '', filename)
    return new_filename


def add_number_prefix(directory):
    # 获取目录中的所有文件
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    # 移除现有前缀并重新排序
    files = [remove_existing_prefix(f) for f in files]
    files.sort()

    # 遍历文件并添加新的编号
    for index, filename in enumerate(files, start=1):
        # 构造新的文件名
        new_filename = f"{index:03d}_{filename}"

        # 获取完整的文件路径
        old_file = os.path.join(directory, filename)
        new_file = os.path.join(directory, new_filename)

        # 重命名文件
        os.rename(old_file, new_file)

        print(f"Renamed: {old_file} -> {new_file}")


# 使用示例
directory = "F:\WebDownload\music"
add_number_prefix(directory)
