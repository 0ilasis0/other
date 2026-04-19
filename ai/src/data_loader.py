import os

import pandas as pd

from const import DataCol, DataVar
from debug import dbg


class DataLoader:
    def __init__(self, file_path: str = DataVar.file_path):
        self.file_path = file_path

    def load(self) -> pd.DataFrame:
        """載入並回傳 DataFrame"""
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"錯誤：找不到資料檔 {self.file_path}")

        df = pd.read_csv(self.file_path, names=DataCol.get_all_values(), na_values='?')
        dbg.log(f"資料載入成功，形狀 {df.shape}")
        return df