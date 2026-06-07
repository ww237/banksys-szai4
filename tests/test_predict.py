"""测试预测模块."""

import pytest

from app.model.predict import load_model, predict


class TestLoadModel:
    def test_raises_when_model_missing(self, monkeypatch, tmp_path):
        # 临时更改 MODEL_DIR 指向不存在模型的目录
        import app.model.predict as pm

        original = pm.MODEL_DIR
        monkeypatch.setattr(pm, "MODEL_DIR", tmp_path)
        with pytest.raises(FileNotFoundError, match="模型文件未找到"):
            load_model()
        monkeypatch.setattr(pm, "MODEL_DIR", original)

    def test_loads_model_when_exists(self, monkeypatch):
        import app.model.predict as pm

        models_dir = pm.MODEL_DIR
        if not (models_dir / "model.pkl").exists():
            pytest.skip("模型尚未训练,跳过此测试")
        model = load_model()
        assert model is not None


class TestPredict:
    def test_predict_returns_correct_columns(self, monkeypatch):
        import app.model.predict as pm

        models_dir = pm.MODEL_DIR
        if not (models_dir / "model.pkl").exists():
            pytest.skip("模型尚未训练,跳过此测试")

        from app.utils.data_loader import load_csv

        df = load_csv("train.csv").drop(columns=["id", "subscribe"]).head(3)
        result = predict(df)
        assert list(result.columns) == ["prediction", "probability"]
        assert len(result) == 3
        assert result["prediction"].isin(["yes", "no"]).all()
        assert (result["probability"] >= 0).all() and (result["probability"] <= 1).all()
