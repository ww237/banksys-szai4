"""在线预测页 — 点选输入客户特征,预测认购意向."""

from pathlib import Path

import pandas as pd
import streamlit as st

from app.model.predict import predict
from app.utils.data_loader import load_csv

st.set_page_config(page_title="在线预测", page_icon="🔮", layout="wide")

st.title("🔮 在线预测 — 银行定期存款认购意向")
st.markdown("填写客户特征,系统将预测该客户是否会认购定期存款。")

# ── 模型检查 ───────────────────────────────────────────────────
MODEL_DIR = Path(__file__).resolve().parent.parent.parent / "models"
MODEL_PATH = MODEL_DIR / "model.pkl"

if not MODEL_PATH.exists():
    st.warning(
        "⚠️ 模型尚未训练,请先运行以下命令:\n\n"
        "```bash\npython -m app.model.train\n```\n\n"
        "训练完成后刷新本页面。"
    )
    st.stop()


# ── 加载数据以获取分类特征选项 ─────────────────────────────────
@st.cache_data
def get_feature_options():
    df = load_csv("train.csv").drop(columns=["id", "subscribe"])
    options = {}
    for col in df.columns:
        if df[col].dtype == "object" or str(df[col].dtype) == "string":
            options[col] = sorted(df[col].dropna().unique().tolist())
        else:
            options[col] = {
                "min": float(df[col].min()),
                "max": float(df[col].max()),
            }
    return options


feature_options = get_feature_options()

# ── 输入表单 ───────────────────────────────────────────────────
st.subheader("客户特征")

with st.form("prediction_form"):
    col1, col2, col3 = st.columns(3)

    inputs = {}
    col_idx = 0
    for col_name, meta in feature_options.items():
        with [col1, col2, col3][col_idx % 3]:
            if isinstance(meta, list):
                # 分类特征:下拉
                inputs[col_name] = st.selectbox(col_name, options=meta, key=f"pred_{col_name}")
            else:
                # 数值特征:数字输入
                step = (
                    1.0
                    if col_name in ("age", "duration", "campaign", "pdays", "previous")
                    else 0.01
                )
                default = (meta["min"] + meta["max"]) / 2
                inputs[col_name] = st.number_input(
                    col_name,
                    min_value=meta["min"],
                    max_value=meta["max"],
                    value=round(default, 2),
                    step=step,
                    key=f"pred_{col_name}",
                )
        col_idx += 1

    submitted = st.form_submit_button("🔮 预测", type="primary", use_container_width=True)

# ── 预测结果 ───────────────────────────────────────────────────
if submitted:
    with st.spinner("正在预测..."):
        input_df = pd.DataFrame([inputs])
        result = predict(input_df)

    st.divider()
    st.subheader("预测结果")

    pred = result["prediction"].iloc[0]
    proba = result["probability"].iloc[0]

    if pred == "yes":
        st.success(f"✅ 预测: **会认购** (概率: {proba:.2%})")
    else:
        st.info(f"❌ 预测: **不会认购** (概率: {1 - proba:.2%})")

    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("认购概率", f"{proba:.2%}")
    with col_b:
        st.metric("不认购概率", f"{1 - proba:.2%}")
