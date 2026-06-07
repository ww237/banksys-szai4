# 01 · 需求 / 活 PRD 〔本项目活记忆 · AI 维护〕

> **作用**:这是本项目唯一的需求文档。所有新功能、缺陷、技术债都追加到这里,不要另起多个 PRD 文件。
> **更新时机**:每次有新需求、需求变更、验收标准变化时更新。

---

## 1. 需求来源

| 类型 | 来源 | 进入方式 |
|---|---|---|
| 功能需求 Feature | 课程作业 / 银行营销场景 | 写成用户故事 |
| 缺陷 Bug | 测试 / 本地运行 / CI 日志 | 写复现步骤和期望结果 |
| 技术债 Tech Debt | 开发 / Review / CI/CD 故障 | 写影响和修复目标 |

---

## 2. Issue 生命周期

| 阶段 | 状态 | 动作 |
|---|---|---|
| 提出 | Open | 写清场景、目标、验收标准 |
| 排期 | Backlog / Todo | 决定优先级和负责人 |
| 开发 | In Progress | 从 main 开 feature 分支 |
| 评审 | In Review | 提 PR,等待 CI 和 Review |
| 合并 | Done | PR 合并 main,自动关闭 Issue |
| 验收 | Verified | 按验收标准确认 |

**追踪规则**:分支名带 Issue 号,PR 描述写 `closes #<编号>`。

---

## 3. 用户故事模板

```text
### US-<编号> <一句话标题> · 状态: Backlog
作为 <角色>,
我想要 <能力>,
以便 <价值>。

验收标准:
- AC1: Given <前提>,When <动作>,Then <可验证结果>。
- AC2: <补充标准>

技术备注:
- <可选:约束、边界、风险>
```

---

## 4. 需求清单

### US-1 初始化项目工程化与 CI · 状态: Backlog

作为 **项目开发者**,
我想要 项目具备基础工程结构、依赖管理、测试框架与 CI 流水线,
以便 后续每次代码提交都能自动检查质量门禁,确保代码可靠。

验收标准:
- AC1: Given 项目根目录,When 执行 `pip install -r requirements.txt -r requirements-dev.txt`,Then 所有依赖成功安装(Python 3.11)。
- AC2: Given 项目代码,When 执行 `ruff format --check .`,Then 格式检查通过。
- AC3: Given 项目代码,When 执行 `ruff check .`,Then 静态检查零错误。
- AC4: Given 测试代码,When 执行 `pytest --cov=app --cov-fail-under=80`,Then 单元测试全部通过且覆盖率 ≥ 80%。
- AC5: Given 项目根目录,When 执行 `docker build .`,Then 镜像成功构建(Docker 环境或 CI 上验证)。
- AC6: Given Push 到 feature 分支,When 创建 PR,Then GitHub Actions CI 自动运行 ruff + pytest + docker build 三道门禁全绿。
- AC7: 从 `main` 开 feature 分支完成初始化,不直接 push main。

技术备注:
- 依赖清单:`requirements.txt`(生产:streamlit, pandas, plotly, scikit-learn)、`requirements-dev.txt`(pytest, pytest-cov, ruff)。
- 端口固定 8004;Streamlit 配置文件写入 `.streamlit/config.toml`。
- 数据文件(`data/*.csv`)与模型产物(`models/*.pkl`)通过 `.gitignore` 排除。

---

### US-2 数据分析交互页面 · 状态: Backlog

作为 **银行业务分析师**,
我想要 在浏览器中交互式地探索银行营销数据,
以便 快速了解数据分布、特征关系,为营销策略制定提供数据洞察。

验收标准:
- AC1: Given 应用已启动(端口 8004),When 访问数据分析页面,Then 页面成功加载并展示 `data/train.csv` 的数据(行数、列数、各列类型)。
- AC2: Given 数据分析页面,When 用户选择某个数值型特征,Then 展示该特征的描述性统计(均值、标准差、最小值、四分位数、最大值)与直方图。
- AC3: Given 数据分析页面,When 用户选择某个分类型特征,Then 展示该特征的频次分布柱状图及占比。
- AC4: Given 数据分析页面,When 用户选择两个数值型特征,Then 展示二者的散点图或相关性热力图。
- AC5: Given 数据分析页面,When 用户切换目标变量 `subscribe` 筛选,Then 页面按 yes/no 分组重新渲染图表(如分组直方图对比)。
- AC6: Given 大数据文件,When 页面加载,Then 数据在 5 秒内完成读取与展示(单次加载,非每次交互重新读取)。

技术备注:
- 页面使用 Streamlit multipage 机制,路径为 `app/pages/01_data_analysis.py`。
- 图表库使用 plotly(plotly.express),支持悬停、缩放、下载。
- 数据加载通过 `app/utils/data_loader.py` 统一入口,支持缓存(`@st.cache_data`)。

---

### US-3 离线模型训练模块 · 状态: Backlog

作为 **数据科学家**,
我想要 使用银行营销历史数据离线训练一个二分类模型,
以便 模型能够根据客户特征预测其是否会认购定期存款,为在线预测提供模型文件。

验收标准:
- AC1: Given `data/train.csv` 存在且包含 `subscribe` 标签列,When 执行 `python -m app.model.train`,Then 完成以下流程并输出训练日志:
  - 数据加载成功,显示样本量与正负比例。
  - 数据预处理(缺失值处理、分类变量编码)自动完成。
  - 划分训练集与验证集(如 80/20 分层抽样)。
  - 训练至少一个 scikit-learn 分类器(如 LogisticRegression 或 RandomForestClassifier)。
  - 输出验证集上的分类报告(precision / recall / f1-score)与 AUC 值。
- AC2: Given 训练完成,When 检查 `models/` 目录,Then 存在训练好的模型文件(如 `model.pkl`)及必要的编码器/预处理对象。
- AC3: Given 训练完成,When 检查 AUC 指标,Then AUC ≥ 0.70(二分类合理基线)。
- AC4: Given 模型已保存,When 调用 `app/model/predict.py` 的加载函数,Then 能成功加载模型并执行推理返回预测类别(yes/no)与概率。

技术备注:
- 模型训练为离线步骤,不在 Streamlit 运行时触发;训练结果保存到 `models/` 目录。
- `models/` 目录加入 `.gitignore`;模型文件不被版本控制。
- 分类变量编码策略(如 OrdinalEncoder / OneHotEncoder)需一并保存,确保预测时编码一致。

---

### US-4 在线预测交互页面 · 状态: Backlog

作为 **银行营销人员**,
我想要 在浏览器中通过点选表单输入客户特征,
以便 系统实时返回该客户是否会认购定期存款的预测结果,辅助我决定是否发起营销电话。

验收标准:
- AC1: Given 应用已启动(端口 8004)且模型文件 `models/model.pkl` 存在,When 访问预测页面,Then 页面展示一个包含所有必需特征字段的输入表单(点选/下拉/滑块)。
- AC2: Given 预测表单,When 用户填写所有字段并点击"预测"按钮,Then 页面显示预测结果:认购(yes)或不认购(no),并附预测概率值(如 0.73)。
- AC3: Given 用户输入,When 某字段未填写或填写非法值,Then 表单提示校验错误,阻止提交,不抛出 500。
- AC4: Given 模型文件不存在,When 访问预测页面,Then 页面显示友好提示"模型尚未训练,请先运行训练脚本",不崩溃。
- AC5: Given 预测结果已展示,When 用户修改输入并再次点击预测,Then 结果即时更新为新预测值。

技术备注:
- 表单字段与训练特征完全对应:age(滑块), job(下拉), marital(下拉), education(下拉), default(下拉 yes/no/unknown), housing, loan, contact, month, day_of_week, duration(数字输入), campaign(数字), pdays(数字), previous(数字), poutcome(下拉), emp_var_rate, cons_price_index, cons_conf_index, lending_rate3m, nr_employed。
- 分类特征的选项值从训练数据中提取,不要硬编码。
- 预测页路径为 `app/pages/02_prediction.py`。

---

### US-5 本地部署与验证 · 状态: Backlog

作为 **使用者**,
我想要 一键启动 Streamlit 应用并在浏览器中访问,
以便 无需复杂配置即可使用数据分析和预测功能。

验收标准:
- AC1: Given 项目依赖已安装,When 执行 `streamlit run app/main.py --server.port 8004`,Then 应用在 `http://localhost:8004` 启动成功。
- AC2: Given 应用已启动,When 浏览器访问 `http://localhost:8004`,Then 显示 Streamlit 主页(含页面导航)。
- AC3: Given 应用已启动,When 访问 `http://localhost:8004/_stcore/health`,Then 返回 200 状态码(健康检查)。
- AC4: Given Docker 已安装,When 执行 `docker build -t banksys-szai4 . && docker run -d -p 8004:8004 --name banksys-szai4 banksys-szai4`,Then 容器成功运行,健康检查通过。

技术备注:
- 启动命令通过 README.md 说明;`.streamlit/config.toml` 固化端口为 8004。
- Dockerfile 中容器内端口固定 8004,映射到主机 8004。

---

## 5. 非功能需求

- **安全**:密钥只进 Secrets,不进 Git。
- **可维护**:一需求一小 PR,避免大爆炸式提交。
- **可测试**:核心逻辑必须有单元测试;数据加载、模型训练、预测推理均需覆盖。
- **可部署**:本地 `streamlit run` 即可启动;Docker 构建可选。
- **数据不入库**:`data/` 与 `models/` 目录加入 `.gitignore`,CI 中使用项目自带数据文件。
- **端口固定**:8004,不随机。
