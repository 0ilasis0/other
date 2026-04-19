import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from const import DataCol, DataVar
from debug import dbg


class DataVisualizer:
    def __init__(self, output_dir: str = DataVar.plot_dir):
        self.output_dir = output_dir
        # 全局設定繪圖風格
        sns.set_theme(style="whitegrid")

    def generate_eda_plots(self, df: pd.DataFrame):
        """生成所有 EDA 相關圖表"""
        df_viz = df.copy()
        # 轉換標籤供視覺化使用
        df_viz[DataCol.TARGET] = np.where(df_viz[DataCol.TARGET] > 0, 1, 0)

        self._plot_target_dist(df_viz)
        self._plot_correlation(df_viz)
        dbg.log(f"✅ DataVisualizer: 視覺化圖表已儲存至 '{self.output_dir}'")

    def _plot_target_dist(self, df: pd.DataFrame):
        plt.figure(figsize=(6, 4))
        sns.countplot(data=df, x=DataCol.TARGET, hue=DataCol.TARGET, palette='Set2', legend=False)
        plt.title('Distribution of Target (0: Healthy, 1: Disease)')
        plt.savefig(os.path.join(self.output_dir, '1_target_distribution.png'))
        plt.close()

    def _plot_correlation(self, df: pd.DataFrame):
        plt.figure(figsize=(12, 10))
        sns.heatmap(df.corr(), annot=True, fmt=".2f", cmap='coolwarm', cbar=True)
        plt.title('Correlation Heatmap')
        plt.savefig(os.path.join(self.output_dir, '2_correlation_heatmap.png'))
        plt.close()