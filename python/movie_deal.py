import os
import subprocess
import sys
import tkinter as tk
from tkinter import filedialog, messagebox

import imageio_ffmpeg


def select_file():
    path = filedialog.askopenfilename(filetypes=[("影片檔案", "*.mp4 *.mkv")])
    file_path.set(path)


def cut_video_ffmpeg(input_path, start_time, end_time, output_path):
    duration = end_time - start_time
    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [
        ffmpeg_path,
        '-ss', str(start_time),
        '-i', input_path,
        '-t', str(duration),
        '-c', 'copy',      # 保留影片、音訊、字幕等資料不重新編碼
        output_path
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"ffmpeg 執行失敗:\n{e.stderr.decode('utf-8')}")


def cut_video():
    input_path = file_path.get()
    if not os.path.isfile(input_path):
        messagebox.showerror("錯誤", "請先選擇有效的影片檔案")
        return

    try:
        start_min = int(start_min_entry.get())
        start_sec = int(start_sec_entry.get())
        end_min = int(end_min_entry.get())
        end_sec = int(end_sec_entry.get())
    except ValueError:
        messagebox.showerror("錯誤", "請輸入有效的整數分秒")
        return

    start_time = start_min * 60 + start_sec
    end_time = end_min * 60 + end_sec

    if start_time >= end_time:
        messagebox.showerror("錯誤", "開始時間必須小於結束時間")
        return

    # 產生輸出檔名，避免覆蓋
    ext = os.path.splitext(input_path)[1]
    output_path = input_path.replace(ext, f"_cut_{start_min}m{start_sec}s_{end_min}m{end_sec}s{ext}")

    try:
        cut_video_ffmpeg(input_path, start_time, end_time, output_path)
        messagebox.showinfo("完成", f"影片已儲存：\n{output_path}")
    except Exception as e:
        messagebox.showerror("錯誤", str(e))


def preview_video():
    path = file_path.get()
    if not os.path.isfile(path):
        messagebox.showerror("錯誤", "請先選擇一個有效的影片檔案")
        return

    try:
        if sys.platform == "win32":
            os.startfile(path)
        elif sys.platform == "darwin":
            subprocess.call(["open", path])
        else:
            subprocess.call(["xdg-open", path])
    except Exception as e:
        messagebox.showerror("錯誤", f"無法開啟影片：{e}")


# GUI 建立
root = tk.Tk()
root.title("影片剪輯工具（支援 mp4 / mkv，保留字幕）")

file_path = tk.StringVar()

tk.Label(root, text="選擇影片：").grid(row=0, column=0, padx=5, pady=5, sticky="e")
tk.Entry(root, textvariable=file_path, width=50).grid(row=0, column=1, padx=5)
tk.Button(root, text="瀏覽", command=select_file).grid(row=0, column=2, padx=5)

# 開始時間輸入
tk.Label(root, text="開始時間 分:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
start_min_entry = tk.Entry(root, width=5)
start_min_entry.grid(row=1, column=1, sticky="w", padx=(0, 2))
tk.Label(root, text="秒:").grid(row=1, column=1, padx=(50, 0), sticky="w")
start_sec_entry = tk.Entry(root, width=5)
start_sec_entry.grid(row=1, column=1, sticky="w", padx=(75, 0))

# 結束時間輸入
tk.Label(root, text="結束時間 分:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
end_min_entry = tk.Entry(root, width=5)
end_min_entry.grid(row=2, column=1, sticky="w", padx=(0, 2))
tk.Label(root, text="秒:").grid(row=2, column=1, padx=(50, 0), sticky="w")
end_sec_entry = tk.Entry(root, width=5)
end_sec_entry.grid(row=2, column=1, sticky="w", padx=(75, 0))

# 按鈕
tk.Button(root, text="剪輯影片", command=cut_video).grid(row=3, column=1, pady=10)
tk.Button(root, text="預覽影片", command=preview_video).grid(row=3, column=2, padx=5)

root.mainloop()
