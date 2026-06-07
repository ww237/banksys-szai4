"""数据分析工具函数 — 纯逻辑,不依赖 Streamlit,方便测试."""

import pandas as pd


def get_summary(df: pd.DataFrame) -> dict:
    """返回 DataFrame 的基本摘要信息.

    Returns:
        {"rows": int, "cols": int, "columns": list[str], "dtypes": dict,
         "numeric_cols": list[str], "categorical_cols": list[str]}.
    """
    num_cols = df.select_dtypes(include=["number"]).columns.tolist()
    cat_cols = df.select_dtypes(include=["object", "string"]).columns.tolist()
    return {
        "rows": len(df),
        "cols": len(df.columns),
        "columns": df.columns.tolist(),
        "dtypes": {c: str(t) for c, t in df.dtypes.items()},
        "numeric_cols": num_cols,
        "categorical_cols": cat_cols,
    }


def get_numeric_stats(df: pd.DataFrame, column: str) -> dict:
    """返回数值列的描述性统计.

    Returns:
        {"count", "mean", "std", "min", "25%", "50%", "75%", "max"}.
    """
    stats = df[column].describe()
    return stats.to_dict()


def get_categorical_counts(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """返回分类列的频次统计(降序)."""
    counts = df[column].value_counts().reset_index()
    counts.columns = ["value", "count"]
    counts["percentage"] = (counts["count"] / counts["count"].sum() * 100).round(2)
    return counts


def get_missing_info(df: pd.DataFrame) -> pd.DataFrame:
    """返回每列的缺失值统计."""
    missing = df.isnull().sum().reset_index()
    missing.columns = ["column", "missing_count"]
    missing["missing_pct"] = (missing["missing_count"] / len(df) * 100).round(2)
    return missing[missing["missing_count"] > 0]


def get_correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """返回数值列的相关系数矩阵."""
    return df.select_dtypes(include=["number"]).corr()


def get_grouped_stats(df: pd.DataFrame, group_col: str, value_col: str) -> pd.DataFrame:
    """按 group_col 分组统计 value_col 的均值与计数."""
    grouped = (
        df.groupby(group_col)[value_col].agg(["mean", "count", "std"]).reset_index()
    )
    grouped.columns = [group_col, "mean", "count", "std"]
    return grouped
