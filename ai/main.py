from src.data_loader import DataLoader
from src.debug import dbg
from src.preprocessor import DataPreprocessor
from src.visualizer import DataVisualizer


def main():
    # 初始化所有物件
    loader = DataLoader()
    visualizer = DataVisualizer()
    preprocessor = DataPreprocessor()

    raw_df = loader.load()

    visualizer.generate_eda_plots(raw_df)

    X_processed, y_processed = preprocessor.process(raw_df)

    dbg.log(f"處理後特徵矩陣大小: {X_processed.shape}")

if __name__ == "__main__":
    main()