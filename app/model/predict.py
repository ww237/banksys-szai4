"""模型加载与在线推理."""

import logging
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from app.model.preprocess import load_preprocessor, preprocess_features

MODEL_DIR = Path(__file__).resolve().parent.parent.parent / "models"

logger = logging.getLogger(__name__)


def load_model() -> RandomForestClassifier:
    """加载训练好的模型.

    Returns:
        模型对象.

    Raises:
        FileNotFoundError: 模型文件不存在时抛出.
    """
    path = MODEL_DIR / "model.pkl"
    if not path.exists():
        raise FileNotFoundError(
            f"模型文件未找到: {path}\n请先运行训练脚本: python -m app.model.train"
        )
    return joblib.load(path)


def predict(df: pd.DataFrame) -> pd.DataFrame:
    """对新数据进行预测.

    Args:
        df: 包含特征的 DataFrame(列名需与训练数据一致,不含 id 和标签)。

    Returns:
        DataFrame 包含列: prediction (yes/no), probability (float).
    """
    model = load_model()
    encoder = load_preprocessor(str(MODEL_DIR / "encoder.pkl"))

    # 预处理
    X, _ = preprocess_features(df, encoder=encoder, fit=False)

    # 推理
    proba = model.predict_proba(X)[:, 1]
    pred = ["yes" if p >= 0.5 else "no" for p in proba]

    return pd.DataFrame({"prediction": pred, "probability": proba.round(4)})
