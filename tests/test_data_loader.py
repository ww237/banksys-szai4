"""测试数据加载工具模块."""

import tempfile
from pathlib import Path

import pandas as pd
import pytest

from app.utils.data_loader import get_column_types, get_data_path, load_csv


class TestGetDataPath:
    """测试 get_data_path 函数."""

    def test_returns_path_ending_with_filename(self):
        path = get_data_path("train.csv")
        assert path.name == "train.csv"

    def test_path_is_under_data_dir(self):
        path = get_data_path("train.csv")
        assert path.parent.name == "data"


class TestLoadCsv:
    """测试 load_csv 函数."""

    def test_loads_valid_csv(self):
        # 用临时文件模拟
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("a,b,c\n1,2,3\n4,5,6\n")
            tmp_path = f.name

        # 临时更改 DATA_DIR 以指向临时目录
        import app.utils.data_loader as dl

        original = dl.DATA_DIR
        try:
            dl.DATA_DIR = Path(tmp_path).parent
            df = load_csv(Path(tmp_path).name)
            assert df.shape == (2, 3)
            assert list(df.columns) == ["a", "b", "c"]
        finally:
            dl.DATA_DIR = original
            Path(tmp_path).unlink(missing_ok=True)

    def test_raises_file_not_found_for_missing_file(self):
        with pytest.raises(FileNotFoundError, match="数据文件不存在"):
            load_csv("nonexistent_file.csv")


class TestGetColumnTypes:
    """测试 get_column_types 函数."""

    def test_separates_numeric_and_categorical(self):
        df = pd.DataFrame(
            {
                "age": [30, 40],
                "name": ["Alice", "Bob"],
                "score": [85.5, 90.0],
                "city": ["NY", "LA"],
            }
        )
        result = get_column_types(df)
        assert "age" in result["numeric"]
        assert "score" in result["numeric"]
        assert "name" in result["categorical"]
        assert "city" in result["categorical"]

    def test_all_numeric_no_categorical(self):
        df = pd.DataFrame({"x": [1, 2], "y": [3.0, 4.0]})
        result = get_column_types(df)
        assert result["numeric"] == ["x", "y"]
        assert result["categorical"] == []

    def test_all_categorical_no_numeric(self):
        df = pd.DataFrame({"a": ["foo", "bar"], "b": ["x", "y"]})
        result = get_column_types(df)
        assert result["numeric"] == []
        assert result["categorical"] == ["a", "b"]
