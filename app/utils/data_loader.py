"""数据加载与缓存工具."""

from pathlib import Path

import pandas as pd

# 项目根目录下的数据路径
DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"


def get_data_path(filename: str) -> Path:
    """返回数据文件的绝对路径."""
    return DATA_DIR / filename


def load_csv(filename: str) -> pd.DataFrame:
    """加载 CSV 数据文件为 DataFrame.

    Args:
        filename: CSV 文件名(如 train.csv, test.csv).

    Returns:
        加载的 DataFrame.

    Raises:
        FileNotFoundError: 文件不存在时抛出.
    """
    path = get_data_path(filename)
    if not path.exists():
        raise FileNotFoundError(f"数据文件不存在: {path}")
    return pd.read_csv(path)


def get_column_types(df: pd.DataFrame) -> dict[str, list[str]]:
    """返回 DataFrame 中数值列与分类列的列名列表.

    Args:
        df: 输入 DataFrame.

    Returns:
        {"numeric": [...], "categorical": [...]}.
    """
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "string"]).columns.tolist()
    return {"numeric": numeric_cols, "categorical": categorical_cols}
