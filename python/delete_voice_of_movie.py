import os

from moviepy.editor import VideoFileClip

# 指定資料夾路徑（例如：下載資料夾）
folder_path = r"C:\Users\User\Downloads"  # ← 改成你自己的下載資料夾路徑

# 逐一處理資料夾中所有 mp4
for file in os.listdir(folder_path):
    if file.lower().endswith(".mp4"):
        input_path = os.path.join(folder_path, file)
        output_path = os.path.join(folder_path, f"no_audio_{file}")

        print(f"正在處理：{file}")
        clip = VideoFileClip(input_path)
        clip_no_audio = clip.without_audio()
        clip_no_audio.write_videofile(output_path, codec="libx264")
        print(f"完成：{output_path}\n")

print("✅ 全部影片音訊已移除完成！")
