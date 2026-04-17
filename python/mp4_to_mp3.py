import os

from moviepy import AudioFileClip, ColorClip, ImageClip


def batch_mp3_to_mp4(input_folder, output_folder, image_path=None):
    """
    將資料夾內所有 MP3 轉為 MP4
    :param input_folder: MP3 來源路徑
    :param output_folder: MP4 輸出路徑
    :param image_path: 背景圖片路徑 (選填，若無則用黑畫面)
    """
    # 建立輸出資料夾
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 取得資料夾內所有 mp3 檔案
    files = [f for f in os.listdir(input_folder) if f.lower().endswith('.mp3')]

    if not files:
        print("資料夾內沒有找到 MP3 檔案。")
        return

    for filename in files:
        mp3_path = os.path.join(input_folder, filename)
        output_filename = os.path.splitext(filename)[0] + ".mp4"
        output_path = os.path.join(output_folder, output_filename)

        print(f"正在處理: {filename}")

        try:
            # 載入音訊
            audio = AudioFileClip(mp3_path)

            if image_path and os.path.exists(image_path):
                # 使用自訂圖片作為背景
                video = ImageClip(image_path).set_duration(audio.duration)
            else:
                # 建立純黑背景 (解析度預設 720p)
                video = ColorClip(size=(1280, 720), color=(0, 0, 0), duration=audio.duration)

            # 將音訊與畫面結合
            video = video.set_audio(audio)

            # 匯出影片 (設定 fps 以降低處理負擔，靜態畫面不需要高 fps)
            video.write_videofile(output_path, fps=1, codec="libx264", audio_codec="aac")

            # 關閉資源
            audio.close()
            video.close()

        except Exception as e:
            print(f"處理 {filename} 時出錯: {e}")

if __name__ == "__main__":
    # 設定你的路徑
    SOURCE_DIR = r"C:\Users\User\Download\song"   # MP3 所在的資料夾
    EXPORT_DIR = r"C:\Users\User\Download\song"   # 轉換後的資料夾
    BG_IMAGE = None   # (選填) 背景圖路徑，不用的話改成 None

    batch_mp3_to_mp4(SOURCE_DIR, EXPORT_DIR, BG_IMAGE)