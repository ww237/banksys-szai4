"""测试数据分析工具模块."""

import pandas as pd
import pytest

from app.utils.analysis import (
    get_categorical_counts,
    get_correlation_matrix,
    get_grouped_stats,
    get_missing_info,
    get_numeric_stats,
    get_summary,
)


@pytest.fixture
def sample_df():
    """构造含数值、分类、缺失值的样本 DataFrame."""
    return pd.DataFrame(
        {
            "age": [30, 40, 50, None, 35],
            "income": [50000, 60000, 70000, 55000, 45000],
            "city": ["NY", "LA", "NY", "SF", None],
            "gender": ["M", "F", "F", "M", "M"],
        }
    )


class TestGetSummary:
    def test_returns_correct_counts(self, sample_df):
        result = get_summary(sample_df)
        assert result["rows"] == 5
        assert result["cols"] == 4

    def test_separates_numeric_and_categorical(self, sample_df):
        result = get_summary(sample_df)
        assert "age" in result["numeric_cols"]
        assert "income" in result["numeric_cols"]
        assert "city" in result["categorical_cols"]
        assert "gender" in result["categorical_cols"]

    def test_returns_dtypes(self, sample_df):
        result = get_summary(sample_df)
        assert "age" in result["dtypes"]
        assert "city" in result["dtypes"]


class TestGetNumericStats:
    def test_returns_describe_stats(self, sample_df):
        stats = get_numeric_stats(sample_df, "income")
        assert "mean" in stats
        assert "std" in stats
        assert stats["count"] == 5
        assert stats["min"] == 45000.0
        assert stats["max"] == 70000.0


class TestGetCategoricalCounts:
    def test_returns_counts_and_percentages(self, sample_df):
        counts = get_categorical_counts(sample_df, "gender")
        assert len(counts) == 2  # M, F
        assert set(counts.columns) == {"value", "count", "percentage"}
        # 3 M + 2 F
        m_row = counts[counts["value"] == "M"].iloc[0]
        assert m_row["count"] == 3
        assert abs(m_row["percentage"] - 60.0) < 0.01


class TestGetMissingInfo:
    def test_returns_only_columns_with_missing(self, sample_df):
        missing = get_missing_info(sample_df)
        assert len(missing) == 2  # age(null), city(null)
        assert "age" in missing["column"].values
        assert "city" in missing["column"].values
        assert "income" not in missing["column"].values

    def test_no_missing_returns_empty(self):
        df = pd.DataFrame({"a": [1, 2, 3]})
        missing = get_missing_info(df)
        assert missing.empty


class TestGetCorrelationMatrix:
    def test_returns_square_dataframe(self, sample_df):
        corr = get_correlation_matrix(sample_df)
        assert corr.shape[0] == corr.shape[1]
        assert 0 <= abs(corr.loc["age", "income"]) <= 1

    def test_excludes_categorical(self, sample_df):
        corr = get_correlation_matrix(sample_df)
        assert "city" not in corr.columns
        assert "gender" not in corr.columns


class TestGetGroupedStats:
    def test_groups_correctly(self, sample_df):
        grouped = get_grouped_stats(sample_df, "gender", "income")
        assert len(grouped) == 2
        assert set(grouped.columns) == {"gender", "mean", "count", "std"}
        m_mean = grouped[grouped["gender"] == "M"]["mean"].iloc[0]
        # (50000+55000+45000)/3 = 50000
        assert m_mean == 50000.0
