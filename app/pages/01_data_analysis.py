"""数据分析交互页 — 银行营销数据探索."""

import pandas as pd
import streamlit as st
import plotly.express as px

from app.utils.data_loader import get_column_types, load_csv
from app.utils.analysis import (
    get_categorical_counts,
    get_correlation_matrix,
    get_grouped_stats,
    get_missing_info,
    get_numeric_stats,
    get_summary,
)

st.set_page_config(page_title="数据分析", page_icon="📊", layout="wide")

st.title("📊 银行营销数据分析")
st.markdown("交互式探索银行电话营销数据集,了解特征分布与认购意向关系。")


# ── 数据加载(缓存) ────────────────────────────────────────────
@st.cache_data
def load_data():
    return load_csv("train.csv")


try:
    df = load_data()
except FileNotFoundError:
    st.error("数据文件 `data/train.csv` 未找到,请确认数据已放置在 `data/` 目录下。")
    st.stop()

col_types = get_column_types(df)
numeric_cols = col_types["numeric"]
categorical_cols = col_types["categorical"]

# ── Tab 结构 ──────────────────────────────────────────────────
tab_overview, tab_univariate, tab_bivariate, tab_target = st.tabs(
    ["📋 数据概览", "📈 单变量分析", "🔗 双变量分析", "🎯 目标分析"]
)

# ── Tab 1: 数据概览 ───────────────────────────────────────────
with tab_overview:
    st.subheader("基本信息")
    summary = get_summary(df)
    col1, col2, col3 = st.columns(3)
    col1.metric("样本量", f"{summary['rows']:,}")
    col2.metric("特征数", summary["cols"])
    col3.metric("目标变量", "subscribe")

    st.subheader("列类型")
    type_df = pd.DataFrame(
        {
            "列名": summary["columns"],
            "类型": [summary["dtypes"][c] for c in summary["columns"]],
        }
    )
    st.dataframe(type_df, use_container_width=True, hide_index=True)

    st.subheader("缺失值")
    missing = get_missing_info(df)
    if missing.empty:
        st.success("✅ 数据无缺失值")
    else:
        st.dataframe(missing, use_container_width=True, hide_index=True)

# ── Tab 2: 单变量分析 ─────────────────────────────────────────
with tab_univariate:
    st.subheader("单变量分布")

    feature = st.selectbox(
        "选择特征",
        options=numeric_cols + categorical_cols,
        key="univar_select",
    )

    if feature:
        if feature in numeric_cols:
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("**描述性统计**")
                stats = get_numeric_stats(df, feature)
                st.dataframe(
                    pd.DataFrame(stats.items(), columns=["指标", "值"]),
                    use_container_width=True,
                    hide_index=True,
                )
            with col_b:
                chart_type = st.radio("图表类型", ["直方图", "箱线图"], horizontal=True)
                if chart_type == "直方图":
                    fig = px.histogram(
                        df,
                        x=feature,
                        nbins=50,
                        title=f"{feature} 分布直方图",
                        marginal="box",
                    )
                else:
                    fig = px.box(df, y=feature, title=f"{feature} 箱线图")
                st.plotly_chart(fig, use_container_width=True)
        else:
            counts = get_categorical_counts(df, feature)
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f"**{feature} 频次分布**")
                st.dataframe(counts, use_container_width=True, hide_index=True)
            with col_b:
                fig = px.bar(
                    counts,
                    x="value",
                    y="count",
                    title=f"{feature} 柱状图",
                    text="percentage",
                )
                fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
                st.plotly_chart(fig, use_container_width=True)

# ── Tab 3: 双变量分析 ─────────────────────────────────────────
with tab_bivariate:
    st.subheader("双变量关系")

    col_left, col_right = st.columns(2)
    with col_left:
        x_col = st.selectbox("X 轴(数值)", options=numeric_cols, key="bivar_x")
    with col_right:
        y_col = st.selectbox("Y 轴(数值)", options=numeric_cols, key="bivar_y")

    chart_mode = st.radio("分析模式", ["散点图", "相关性热力图"], horizontal=True)

    if chart_mode == "散点图":
        color_by = st.selectbox(
            "按认购意向着色",
            options=["(无)", "subscribe"],
            key="scatter_color",
        )
        color = None if color_by == "(无)" else color_by
        fig = px.scatter(
            df,
            x=x_col,
            y=y_col,
            color=color,
            opacity=0.6,
            title=f"{x_col} vs {y_col}",
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        corr = get_correlation_matrix(df)
        fig = px.imshow(
            corr,
            text_auto=".2f",
            aspect="auto",
            title="数值特征相关性热力图",
            color_continuous_scale="RdBu_r",
            zmin=-1,
            zmax=1,
        )
        st.plotly_chart(fig, use_container_width=True)

# ── Tab 4: 目标分析 ───────────────────────────────────────────
with tab_target:
    st.subheader("认购意向 (subscribe) 分析")

    subscribe_counts = df["subscribe"].value_counts()
    col_a, col_b = st.columns(2)
    with col_a:
        fig = px.pie(
            names=subscribe_counts.index,
            values=subscribe_counts.values,
            title="认购意向占比",
            hole=0.4,
        )
        st.plotly_chart(fig, use_container_width=True)
    with col_b:
        st.markdown(f"- **认购 (yes)**: {subscribe_counts.get('yes', 0):,} 人")
        st.markdown(f"- **未认购 (no)**: {subscribe_counts.get('no', 0):,} 人")
        st.markdown(
            f"- **认购率**: {subscribe_counts.get('yes', 0) / len(df) * 100:.2f}%"
        )

    st.divider()
    st.markdown("### 按认购意向分组的特征对比")

    compare_feat = st.selectbox(
        "选择对比特征",
        options=numeric_cols,
        key="target_compare",
    )
    if compare_feat:
        grouped = get_grouped_stats(df, "subscribe", compare_feat)
        col_a, col_b = st.columns(2)
        with col_a:
            fig = px.bar(
                grouped,
                x="subscribe",
                y="mean",
                title=f"{compare_feat} 按 subscribe 分组均值",
                text=grouped["mean"].round(2),
            )
            fig.update_traces(texttemplate="%{text}", textposition="outside")
            st.plotly_chart(fig, use_container_width=True)
        with col_b:
            fig = px.box(
                df,
                x="subscribe",
                y=compare_feat,
                title=f"{compare_feat} 分组箱线图",
            )
            st.plotly_chart(fig, use_container_width=True)
