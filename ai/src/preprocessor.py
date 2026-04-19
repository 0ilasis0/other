import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

from const import DataCol


class DataPreprocessor:
    def __init__(self):
        self.imputer = SimpleImputer(strategy='median')
        self.scaler = StandardScaler()
        self.is_fitted = False

    def process(self, df: pd.DataFrame):
        """執行完整的資料前處理流程"""
        df_processed = df.copy()

        # 1. 標籤二值化
        df_processed[DataCol.TARGET] = df_processed[DataCol.TARGET].apply(lambda x: 1 if x > 0 else 0)

        # 2. 分離特徵與標籤
        X = df_processed.drop(columns=[DataCol.TARGET])
        y = df_processed[DataCol.TARGET]

        # 3. 填補與標準化 (Fit & Transform)
        X_imputed = pd.DataFrame(self.imputer.fit_transform(X), columns=X.columns)
        X_scaled = pd.DataFrame(self.scaler.fit_transform(X_imputed), columns=X.columns)

        self.is_fitted = True
        print("✅ DataPreprocessor: 特徵工程與標準化完成")
        return X_scaled, y