import os
import shutil

source_root = r'C:\Users\User\Downloads'
destination = r'C:\Users\User\Downloads'

os.makedirs(destination, exist_ok=True)

for subfolder in os.listdir(source_root):
    subfolder_path = os.path.join(source_root, subfolder)

    if os.path.isdir(subfolder_path):
        png_path = os.path.join(subfolder_path, 'p.png')

        if os.path.isfile(png_path):
            # 移動 p.png 並改名為子資料夾名稱.png
            new_filename = f'{subfolder}.png'
            destination_path = os.path.join(destination, new_filename)
            shutil.move(png_path, destination_path)

            # 刪除整個子資料夾（包含其他檔案）
            shutil.rmtree(subfolder_path)
            print(f"已搬移 {new_filename} 並刪除資料夾：{subfolder_path}")
