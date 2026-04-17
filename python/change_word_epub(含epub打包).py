import os
import shutil
import uuid
import zipfile

from bs4 import BeautifulSoup

path = r'C:\Users\User\Downloads'

# 替換文字規則
REPLACEMENTS = [
    # ('他', '她'),
    # ('其她', '其他'),
]

# 文字替換函式
def replace_text_in_folder(folder_path, replacements):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.xhtml'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    soup = BeautifulSoup(f, features='xml')

                changed = False
                for text_node in soup.find_all(string=True):
                    original = str(text_node)
                    modified = original
                    for old_str, new_str in replacements:
                        modified = modified.replace(old_str, new_str)
                    if modified != original:
                        text_node.replace_with(modified)
                        changed = True

                if changed:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(str(soup))
                    print(f"✅ 已替換文字: {file_path}")

# 打包成 epub
def folder_to_epub(folder_path, output_epub):
    mimetype_path = os.path.join(folder_path, "mimetype")
    if not os.path.isfile(mimetype_path):
        print("⚠️ 忽略：缺少 mimetype")
        return

    with zipfile.ZipFile(output_epub, 'w') as epub:
        epub.write(mimetype_path, "mimetype", compress_type=zipfile.ZIP_STORED)
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                if full_path == mimetype_path:
                    continue
                relative_path = os.path.relpath(full_path, folder_path)
                epub.write(full_path, relative_path, compress_type=zipfile.ZIP_DEFLATED)

    print(f"📘 完成：{output_epub}")

# 處理單一 epub
def process_epub(epub_path, output_folder, replacements):
    basename = os.path.basename(epub_path)
    name, _ = os.path.splitext(basename)
    temp_dir = os.path.join(output_folder, f"temp_{uuid.uuid4().hex[:8]}")

    try:
        # 解壓
        with zipfile.ZipFile(epub_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # 找到 OEBPS/Text 或其他 .xhtml 路徑
        replace_text_in_folder(temp_dir, replacements)

        # 輸出新 epub
        output_epub = os.path.join(output_folder, f"{name}_converted.epub")
        folder_to_epub(temp_dir, output_epub)

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

# 處理整個資料夾
def batch_process_epubs(folder_path):
    for file in os.listdir(folder_path):
        if file.lower().endswith(".epub"):
            epub_path = os.path.join(folder_path, file)
            print(f"🔧 處理檔案：{epub_path}")
            process_epub(epub_path, folder_path, REPLACEMENTS)

# 🔁 批次執行
batch_process_epubs(path)
