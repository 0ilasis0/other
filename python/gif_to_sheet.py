import math

from PIL import Image, ImageSequence


def gif_to_sprite_sheet(input_path, output_path,
                        sampling_interval=1,
                        scale_factor=1.0,
                        fixed_cols=None,
                        pixel_art_mode=True): # [新增] 專門針對像素圖的放大模式
    try:
        with Image.open(input_path) as im:
            original_duration = im.info.get('duration', 100)

            # 設定縮放演算法
            # Pixel Art 必須用 NEAREST (保持鋸齒，不模糊)
            # 普通照片用 LANCZOS (平滑處理)
            resample_algo = Image.Resampling.NEAREST if pixel_art_mode else Image.Resampling.LANCZOS

            frames = []
            iterator = ImageSequence.Iterator(im)
            for i, frame in enumerate(iterator):
                if i % sampling_interval == 0:
                    f = frame.copy().convert('RGBA')

                    # 執行縮放
                    if scale_factor != 1.0:
                        new_w = int(f.width * scale_factor)
                        new_h = int(f.height * scale_factor)
                        f = f.resize((new_w, new_h), resample_algo)

                    frames.append(f)

        if not frames:
            print("錯誤：沒有擷取到任何幀。")
            return

        n_frames = len(frames)
        frame_w, frame_h = frames[0].size

        if fixed_cols:
            cols = fixed_cols
            rows = math.ceil(n_frames / cols)
        else:
            cols = math.ceil(math.sqrt(n_frames))
            rows = math.ceil(n_frames / cols)

        sheet_w = cols * frame_w
        sheet_h = rows * frame_h
        sheet = Image.new('RGBA', (sheet_w, sheet_h), (0, 0, 0, 0))

        for i, frame in enumerate(frames):
            row = i // cols
            col = i % cols
            x = col * frame_w
            y = row * frame_h
            sheet.paste(frame, (x, y))

        sheet.save(output_path)

        print(f"\n--- 轉換完成 ---")
        print(f"模式: {'像素風格(不模糊)' if pixel_art_mode else '平滑模式'}")
        print(f"縮放倍率: {scale_factor}x")
        print(f"單格尺寸: {frame_w}x{frame_h}")
        print(f"輸出檔案: {output_path}")

    except Exception as e:
        print(f"發生錯誤: {e}")

# --- 使用範例 ---
input_path = r"C:\Users\User\Downloads\21512.gif"
output_path = r"C:\Users\User\Downloads\黑塔_高清放大.png"


gif_to_sprite_sheet(
    input_path, output_path,
    sampling_interval = 1,
    scale_factor = 1.0,
    fixed_cols = None,
    pixel_art_mode = True
)
"""
將 GIF 動畫轉換為遊戲用的 Sprite Sheet (精靈圖集)。

參數說明：
:param input_path:      原始 GIF 檔案的路徑。
:param output_path:     輸出的 PNG 檔案路徑 (建議使用 .png 以保留透明度)。

:param sampling_interval: 採樣間隔 (控制動畫的總幀數/FPS)。
                            - 1: 保留所有原始幀。
                            - 2: 每兩幀取一幀，總圖片數量減半，動作會看起來快兩倍。
                            - 常用於縮小檔案體積，或調整動畫節奏。

:param scale_factor:    圖片縮放比例 (控制解析度)。
                            - 1.0: 原始尺寸。
                            - 2.0: 長寬放大兩倍 (解析度提高)。
                            - 0.5: 長寬縮小一半 (節省記憶體)。

:param fixed_cols:      固定輸出的列數 (控制排版)。
                            - None: 自動計算，讓輸出的圖片接近正方形 (例如 16 幀會排成 4x4)。
                            - 數字: 例如設為 8，則不論總幀數多少，一行固定就是 8 張圖。

:param pixel_art_mode:  像素藝術模式 (控制放大品質)。
                            - True: 使用「最近鄰插值」，放大時會保持像素邊緣銳利，適合黑塔這種像素風格。
                            - False: 使用「LANCZOS」平滑濾波，放大時會進行反鋸齒處理，適合一般的照片。
"""