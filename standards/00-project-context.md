# 00 · 项目上下文 〔本项目活记忆 · AI 维护〕

> **作用**:这是项目的"身份档案"。AI 接管项目时先读这里,了解项目目标、技术栈、目录、部署取值。
> **更新时机**:架构、技术栈、目录结构、端口、部署目录、重要约束变化时更新。

---

## 1. 项目是什么

- **项目名称**:`banksys-szai4` — 银行营销预测系统
- **一句话目标**:基于银行电话营销历史数据,提供交互式数据分析与客户认购预测服务。
- **使用者/受益者**:银行业务分析师、营销团队;用于辅助决策是否向某客户发起营销电话。
- **核心功能**:
  - **数据分析交互页**:加载银行营销 CSV 数据,提供统计摘要、分布图表、相关性分析等交互式探索能力。
  - **在线预测系统**:离线训练二分类模型(认购 yes/no),在线提供点选表单输入客户特征,返回预测结果与概率。
- **输入/数据**(如有):
  - `data/train.csv`(约 2.8 MB,含标签列 `subscribe`):用于离线模型训练。
  - `data/test.csv`(约 0.9 MB,不含标签列):用于预测演示。
  - 数据为公开银行营销数据集,不涉及敏感个人信息;**CSV 不进 Git**(通过 `.gitignore` 排除)。

## 2. 技术栈

| 层 | 选型 | 理由 |
|---|---|---|
| 语言/运行时 | Python 3.11 | 课程指定版本,生态成熟(数据科学/ML/Web) |
| Web/App 框架 | Streamlit | 纯 Python 即可构建数据交互页面,无需前后端分离,适合快速原型与教学 |
| 数据处理 | pandas | CSV 读取、清洗、统计分析的标配 |
| 可视化 | plotly | 交互式图表,与 Streamlit 深度集成 |
| 机器学习 | scikit-learn | 经典二分类模型(逻辑回归/随机森林),轻量、可解释、无需 GPU |
| 测试 | pytest | 课程指定;配合 `pytest-cov` 达覆盖率门禁 |
| 格式/静态检查 | ruff | 课程指定;统一格式与 lint,速度快 |
| 打包/运行 | Docker | 课程指定;本地与 CI 均可构建镜像 |
| CI/CD | GitHub Actions | 通用、可视化、适合教学与团队协作 |

## 3. 目录地图

```text
banksys_szai4/
├── standards/                  # AI 项目记忆与通用规范
│   ├── README.md
│   ├── 00-project-context.md
│   ├── 01-requirements.md
│   ├── PROGRESS.md
│   ├── 02-coding-standards.md
│   ├── 03-testing-standards.md
│   ├── 04-git-workflow.md
│   ├── 05-cicd-standards.md
│   ├── 06-ai-collab-protocol.md
│   └── templates/
├── data/                       # 原始数据(不进 Git)
│   ├── train.csv
│   └── test.csv
├── app/                        # Streamlit 应用主目录
│   ├── __init__.py
│   ├── main.py                 # Streamlit 入口,页面路由
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── 01_data_analysis.py # 数据分析交互页
│   │   └── 02_prediction.py    # 在线预测页
│   ├── model/
│   │   ├── __init__.py
│   │   ├── train.py            # 模型训练脚本
│   │   └── predict.py          # 模型加载与推理
│   └── utils/
│       ├── __init__.py
│       └── data_loader.py      # 数据加载与预处理
├── tests/                      # 测试目录
│   ├── __init__.py
│   ├── test_data_loader.py
│   ├── test_train.py
│   ├── test_predict.py
│   └── test_pages.py
├── models/                     # 训练产出模型文件(不进 Git)
├── requirements.txt            # 生产运行依赖
├── requirements-dev.txt        # 本地/CI 检查依赖
├── Dockerfile                  # 容器构建定义
├── .github/workflows/
│   └── ci.yml                  # CI 流水线(ruff + pytest + docker build)
├── .gitignore
└── README.md
```

> 新增目录前先更新本节,避免项目越做越散。

## 4. 质量门槛

| 类型 | 本项目标准 |
|---|---|
| 格式检查 | `ruff format --check .` |
| 静态检查 | `ruff check .` |
| 单元测试 | `pytest` |
| 覆盖率 | `pytest --cov=app --cov-fail-under=80` |
| 构建 | `docker build .` 成功 |
| 业务/模型指标 | 模型 AUC ≥ 0.70(二分类基线);预测接口返回格式校验 |

## 5. 不变约束

- 密钥、密码、私钥、Token **绝不写进代码或文档**,只进 GitHub Secrets / 环境变量。
- 大文件(`data/*.csv`、`models/*.pkl`)不进 Git,通过 `.gitignore` 排除。
- `main` 分支受保护,日常开发必须走 feature 分支 + PR。
- CI 红灯不合并。
- 本项目不做 CD(本地部署),CI 阶段构建 Docker 镜像但不推送。

## 6. 部署/CI 占位符取值

> `guides/` 和 workflow 里的通用占位符,在本项目里的真实值只写这里。

| 占位符 | 本项目取值 | 说明 |
|---|---|---|
| `<APP>` | `banksys-szai4` | 应用名/镜像名/容器名 |
| `<DEPLOY_DIR>` | `E:\my_xiangmu` | 本地项目根目录(本地部署,非服务器) |
| `<PORT>` | `8004` | Streamlit 服务端口 |
| `<PYVER>` | `3.11` | Python 版本 |
| `<HEALTHCHECK>` | `/_stcore/health` | Streamlit 内置健康检查端点 |
| `<SSH_USER>` | — | 不适用(仅本地部署) |
| `<SSH_HOST>` | — | 不适用(仅本地部署) |
