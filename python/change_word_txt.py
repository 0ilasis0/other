import os


def replace_text_in_txt_files(folder_path, replacements):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)

                # 讀取檔案文字內容
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                original_content = content

                # 套用所有替換規則
                for old_str, new_str in replacements:
                    content = content.replace(old_str, new_str)

                # 若有改變才寫回檔案
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f'已替換文字：{file_path}')
                else:
                    print(f'無需替換：{file_path}')

# 替換字串清單（順序會影響結果）
replacements = [
    # ('他', '她'),
    # ('其她', '其他'),
]

# 執行路徑為資料夾（會遞迴搜尋裡面的 .txt）
replace_text_in_txt_files(r'C:\Users\User\Downloads', replacements)
