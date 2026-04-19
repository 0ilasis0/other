import sys
from dataclasses import dataclass
from pathlib import Path

from debug import dbg


def _resource_path(*paths):
    """
    取得外部資源路徑：
    - 打包成 exe 時：使用 exe 同目錄
    - 開發模式：使用專案根目錄
    """
    if getattr(sys, "frozen", False):
        # exe 打包後使用的路徑
        base_path = Path(sys.executable).resolve().parent.parent
    else:
        # 開發環境使用的路徑
        base_path = Path(__file__).resolve().parent.parent.parent

    return base_path.joinpath(*paths)


@dataclass(frozen = True)
class _PathBase:
    data = _resource_path("data")
    plot = _resource_path("plot")

    @classmethod
    def get_all_paths(cls):
        return [v for _, v in vars(cls).items() if isinstance(v, Path)]

@dataclass(frozen = True)
class PathConfig:
    data = _PathBase.data / 'processed.cleveland.data'
    plot_dir = _PathBase.plot

def setup_filesystem():
    """
    確保所有靜態路徑的「資料夾」都存在。
    """
    try:
        for d in _PathBase.get_all_paths():
            if not d.exists():
                d.mkdir(parents=True, exist_ok=True)
                dbg.log(f"[系統初始化] 建立新資料夾: {d}")

    except Exception as e:
        dbg.error(f"路徑系統初始化警告: {e}")
