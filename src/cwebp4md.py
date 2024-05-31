import os
import re
import sys
from glob import glob
from PIL import Image, ImageSequence
import multiprocessing


def find_md_files(pattern):
    return glob(pattern)


def find_md_files_in_directory(directory, recursive=False):
    if recursive:
        pattern = os.path.join(directory, "**", "*.md")
    else:
        pattern = os.path.join(directory, "*.md")
    return glob(pattern, recursive=recursive)


def find_local_images(md_content):

    # 使用正则表达式找到所有图片路径，并排除 http 和 .webp
    pattern = r"((?<!<!-- )!\[(.*?)\]\((?!http[s]?:)(?!.*\.webp\))(.*?)\))(?!.*-->)"
    all_images = re.findall(pattern, md_content)
    return all_images


def convert_image_to_webp(image_path, md_file, quality=80):

    if not os.path.isabs(image_path):
        # 获取图片的绝对路径
        abs_image_path = os.path.join(os.path.dirname(md_file), image_path)
    else:
        abs_image_path = image_path
    # 检查图片是否存在
    abs_image_path = os.path.normpath(abs_image_path)

    if not os.path.exists(abs_image_path):
        print(f"Warning: Image '{abs_image_path}' not found. Skipping...")
        return False

    # 获取文件路径、文件名和扩展名
    dirname = os.path.dirname(abs_image_path)
    basename = os.path.basename(abs_image_path)
    filename, ext = os.path.splitext(basename)
    output_path = os.path.join(dirname, f"{filename}.webp")
    output_path = os.path.normpath(output_path)

    # 判断webp是否已经存在
    if ext.lower() != ".webp" and not os.path.exists(output_path):
        if ext.lower() == ".gif":
            with Image.open(abs_image_path) as img:
                frames = [frame.copy() for frame in ImageSequence.Iterator(img)]
                frames[0].save(
                    output_path, format="WEBP", save_all=True, append_images=frames[1:], loop=0, duration=img.info["duration"], quality=quality, method=6
                )
        else:
            with Image.open(abs_image_path) as img:
                img.save(output_path, "WEBP", quality=quality, method=6)
        print(f"  Converted '{abs_image_path}' ---> '{output_path}'")

    # 获取新的相对路径，并保留 ./ 前缀
    output_path = os.path.relpath(output_path, os.path.dirname(md_file))
    output_path = os.path.normpath(output_path)
    output_path = output_path.replace("\\", "/")
    if not output_path.startswith("./"):
        output_path = "./" + output_path
    return output_path


def process_markdown(md_file):
    with open(md_file, "r", encoding="utf-8") as file:
        md_content = file.read()

    all_images = find_local_images(md_content)
    # print(all_images)

    for full_match, alt_text, image_path in all_images:
        new_image_path = convert_image_to_webp(image_path, md_file)
        md_content = md_content.replace(full_match, f"<!-- {full_match} -->\n![{alt_text}]({new_image_path})")

    # 写回Markdown文件
    with open(md_file, "w", encoding="utf-8") as file:
        file.write(md_content)


def process_markdown_file(md_file, current_directory):
    print(f"Processing '{md_file}'...")
    # 判断路径是否是绝对路径
    if os.path.isabs(md_file):
        pass
    else:
        # 如果是相对路径，则将其与当前工作目录拼接
        md_file = os.path.join(current_directory, md_file)

    if not os.path.isfile(md_file):
        print(f"Warning: File '{md_file}' not found. Skipping...")
        return

    process_markdown(md_file)


def print_help():
    help_message = """
    Usage: python cwebp4md.py <input_file_pattern> [-r <directory>] [-d <directory>] [-h | --help]

    Options:
        <input_file_pattern>    Pattern to match markdown files (e.g., "*.md").
        -r <directory>          Specify directory to search for markdown files recursively.
        -d <directory>          Specify directory to search for markdown files non-recursively.
        -h, --help              Show this help message and exit.

    Example:
        python cwebp4md.py "*.md" -r ./docs -d ./notes
    """
    print(help_message)


if __name__ == "__main__":
    multiprocessing.freeze_support()
    if len(sys.argv) < 2 or "-h" in sys.argv or "--help" in sys.argv:
        print_help()
        sys.exit(0)

    input_patterns = []
    directories = []
    recursive_search = False

    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "-r" and i + 1 < len(sys.argv):
            directories.append((sys.argv[i + 1], True))
            i += 1
        elif sys.argv[i] == "-d" and i + 1 < len(sys.argv):
            directories.append((sys.argv[i + 1], False))
            i += 1
        else:
            input_patterns.append(sys.argv[i])
        i += 1

    current_directory = os.getcwd()
    print("工作路径：", current_directory)

    md_files = []

    for pattern in input_patterns:
        md_files.extend(find_md_files(pattern))

    for directory, recursive in directories:
        md_files.extend(find_md_files_in_directory(directory, recursive))

    print("找到的 .md 文件：", md_files)

    if not md_files:
        print(f"Error: No files matched the pattern '{input_patterns}'")
        sys.exit(1)

    # 使用 multiprocessing.Pool 创建一个进程池
    with multiprocessing.Pool() as pool:
        # 将 md_files 和 current_directory 作为参数传递给 process_markdown_file 函数
        pool.starmap(process_markdown_file, [(md_file, current_directory) for md_file in md_files])

    print("Markdown files updated successfully.")
