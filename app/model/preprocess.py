"""数据预处理 — 与训练/预测共享."""

import joblib
import pandas as pd
from sklearn.preprocessing import OrdinalEncoder


def preprocess_features(
    df: pd.DataFrame, encoder: OrdinalEncoder | None = None, fit: bool = False
) -> tuple[pd.DataFrame, OrdinalEncoder]:
    """预处理特征 DataFrame.

    - 填充缺失值:数值列用中位数,分类列用 "unknown"
    - 编码分类变量:OrdinalEncoder(训练时 fit,预测时 transform)

    Args:
        df: 输入特征 DataFrame(不含 id 与标签列)。
        encoder: 已有编码器;None 时自动创建。
        fit: 是否 fit encoder(训练时为 True,预测时为 False)。

    Returns:
        (预处理后的 DataFrame, 编码器)。
    """
    df = df.copy()

    # 分离列类型
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "string"]).columns.tolist()

    # 填充缺失值
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].median())
    for col in categorical_cols:
        df[col] = df[col].fillna("unknown")

    # 编码分类变量
    if categorical_cols:
        if encoder is None:
            encoder = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)
            fit = True  # 未提供编码器时必须 fit
        if fit:
            encoded = encoder.fit_transform(df[categorical_cols].astype(str))
        else:
            encoded = encoder.transform(df[categorical_cols].astype(str))
        df[categorical_cols] = encoded

    return df, encoder


def save_preprocessor(encoder: OrdinalEncoder, path: str) -> None:
    """保存编码器到文件."""
    joblib.dump(encoder, path)


def load_preprocessor(path: str) -> OrdinalEncoder:
    """从文件加载编码器."""
    return joblib.load(path)
