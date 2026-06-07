"""测试数据预处理模块."""

import pandas as pd
import pytest

from app.model.preprocess import (
    load_preprocessor,
    preprocess_features,
    save_preprocessor,
)


@pytest.fixture
def sample_df():
    return pd.DataFrame(
        {
            "age": [30, 40, None, 35],
            "job": ["admin.", "blue-collar", "entrepreneur", None],
            "income": [50000, 60000, None, 45000],
        }
    )


class TestPreprocessFeatures:
    def test_fills_missing_numeric_with_median(self, sample_df):
        result, _ = preprocess_features(sample_df)
        # age median = 35, so NaN → 35
        assert result["age"].iloc[2] == 35.0
        # income median = (50k+60k+45k)/3 = 51.67k approx
        assert result["income"].iloc[2] > 0

    def test_fills_missing_categorical_with_unknown(self, sample_df):
        result, _ = preprocess_features(sample_df)
        # job[3] was None → "unknown", which ordinal encodes to some value
        assert not result["job"].isnull().any()

    def test_fit_returns_encoder(self, sample_df):
        _, encoder = preprocess_features(sample_df, fit=True)
        assert encoder is not None

    def test_transform_with_existing_encoder(self, sample_df):
        # First fit
        _, encoder = preprocess_features(sample_df, fit=True)
        # Then transform same data
        result, enc2 = preprocess_features(sample_df, encoder=encoder, fit=False)
        assert enc2 is encoder  # same object returned
        assert not result.isnull().any().any()

    def test_all_columns_preserved(self, sample_df):
        result, _ = preprocess_features(sample_df)
        assert list(result.columns) == list(sample_df.columns)
        assert len(result) == len(sample_df)


class TestSaveLoad:
    def test_save_and_load_roundtrip(self, sample_df, tmp_path):
        _, encoder = preprocess_features(sample_df, fit=True)
        path = tmp_path / "encoder.pkl"
        save_preprocessor(encoder, str(path))
        loaded = load_preprocessor(str(path))
        # Verify loaded encoder works the same
        result1, _ = preprocess_features(sample_df, encoder=encoder, fit=False)
        result2, _ = preprocess_features(sample_df, encoder=loaded, fit=False)
        pd.testing.assert_frame_equal(result1, result2)
