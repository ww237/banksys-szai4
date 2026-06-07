"""banksys-szai4 — 银行营销预测系统主入口."""

import sys
from pathlib import Path

# 确保项目根目录在 Python 路径中(Streamlit 页面独立运行时需要)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st

st.set_page_config(
    page_title="银行营销预测系统",
    page_icon="🏦",
    layout="wide",
)

st.title("🏦 银行营销预测系统")
st.markdown(
    """
    欢迎使用银行营销预测系统。请通过左侧导航选择功能：
    - **数据分析**：交互式探索银行营销数据集
    - **在线预测**：输入客户特征，预测认购意向
    """
)
