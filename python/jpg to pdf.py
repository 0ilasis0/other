import glob
import os

from PIL import Image


def jpgs_to_pdf(folder_path, output_pdf):
    # 抓取指定資料夾內所有 JPG 檔案 (依檔名排序)
    files = sorted(glob.glob(os.path.join(folder_path, "*.jpg")))

    if not files:
        print("❌ 找不到 JPG 檔案")
        return

    # 轉成 RGB 並存成清單
    images = [Image.open(f).convert("RGB") for f in files]

    # 第一張當作起始頁，其餘加在後面
    images[0].save(output_pdf, save_all=True, append_images=images[1:])
    print(f"✅ PDF 已完成：{output_pdf}")

if __name__ == "__main__":
    # 修改這裡的資料夾路徑 & 輸出檔名
    folder = r"C:\Users\User\Downloads"
    output = r"C:\Users\User\Downloads\output.pdf"

    jpgs_to_pdf(folder, output)
