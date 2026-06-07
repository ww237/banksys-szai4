"""离线模型训练脚本.

用法: python -m app.model.train
产出: models/model.pkl, models/encoder.pkl, models/metrics.json
"""

import json
import logging
import sys
from pathlib import Path

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split

from app.model.preprocess import preprocess_features, save_preprocessor
from app.utils.data_loader import load_csv

MODEL_DIR = Path(__file__).resolve().parent.parent.parent / "models"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    """主训练流程."""
    # 1. 加载数据
    logger.info("加载训练数据...")
    df = load_csv("train.csv")
    logger.info("数据形状: %s", df.shape)

    # 2. 分离特征与标签
    if "id" in df.columns:
        df = df.drop(columns=["id"])
    y = df["subscribe"].map({"yes": 1, "no": 0})
    X = df.drop(columns=["subscribe"])

    pos_rate = y.mean()
    logger.info("正样本(yes)占比: %.2f%%", pos_rate * 100)

    # 3. 预处理
    logger.info("预处理特征...")
    X_processed, encoder = preprocess_features(X, fit=True)

    # 4. 划分训练/验证集(分层)
    X_train, X_val, y_train, y_val = train_test_split(
        X_processed, y, test_size=0.2, stratify=y, random_state=42
    )
    logger.info("训练集: %d, 验证集: %d", len(X_train), len(X_val))

    # 5. 训练模型
    logger.info("训练 RandomForestClassifier...")
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)

    # 6. 评估
    y_pred = model.predict(X_val)
    y_proba = model.predict_proba(X_val)[:, 1]
    auc = roc_auc_score(y_val, y_proba)
    report = classification_report(y_val, y_pred, target_names=["no", "yes"], output_dict=True)

    logger.info("验证集 AUC: %.4f", auc)
    logger.info("分类报告:\n%s", classification_report(y_val, y_pred, target_names=["no", "yes"]))

    # 7. 保存模型与预处理
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    model_path = MODEL_DIR / "model.pkl"
    encoder_path = MODEL_DIR / "encoder.pkl"
    metrics_path = MODEL_DIR / "metrics.json"

    import joblib

    joblib.dump(model, model_path)
    save_preprocessor(encoder, str(encoder_path))

    metrics = {
        "auc": round(auc, 4),
        "accuracy": report["accuracy"],
        "precision_yes": report["yes"]["precision"],
        "recall_yes": report["yes"]["recall"],
        "f1_yes": report["yes"]["f1-score"],
        "train_samples": len(X_train),
        "val_samples": len(X_val),
        "positive_rate": round(pos_rate, 4),
    }
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)

    logger.info("模型已保存: %s", model_path)
    logger.info("编码器已保存: %s", encoder_path)
    logger.info("指标已保存: %s", metrics_path)

    # 8. AUC 门禁
    if auc < 0.70:
        logger.error("AUC %.4f 低于最低阈值 0.70,训练不合格!", auc)
        sys.exit(1)
    logger.info("训练完成! AUC %.4f ≥ 0.70 ✅", auc)


if __name__ == "__main__":
    main()
