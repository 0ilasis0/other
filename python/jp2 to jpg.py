import os

from PIL import Image


def convert_jp2_to_jpg_pillow(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.jp2'):
            input_path = os.path.join(input_dir, filename)
            output_filename = os.path.splitext(filename)[0] + '.jpg'
            output_path = os.path.join(output_dir, output_filename)

            try:
                with Image.open(input_path) as img:
                    rgb_img = img.convert('RGB')  # 有些 JP2 是灰階或其他模式
                    rgb_img.save(output_path, 'JPEG')
                    print(f"✔ 轉換成功：{filename}")
            except Exception as e:
                print(f"✘ 轉換失敗：{filename}，錯誤：{e}")

# 📌 替換成你自己的資料夾路徑
input_folder = r'C:\Users\User\Downloads\1'
output_folder = r'C:\Users\User\Downloads'

convert_jp2_to_jpg_pillow(input_folder, output_folder)
