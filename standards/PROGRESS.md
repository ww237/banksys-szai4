# PROGRESS · banksys-szai4 〔本项目活记忆 · 状态机〕

> **作用**:这是项目的"存档点"。任意 AI、任意重启会话,读它即可知道当前做到哪、下一步做什么、踩过什么坑。
> **更新时机**:每完成一个有意义步骤、每次会话结束前。
> **格式要求**:时间倒序,最新在上;短、准、可接力。

---

## 当前状态 (最后更新: 2026-06-07 · by AI)

- **阶段**:`开发中 — US-1 CI 全绿,等待人工 Review & Merge`
- **上一步完成**:Phase 1 全部完成;PR #1 已创建,CI 全绿(lint-and-test ✅ + docker-build ✅)。
- **下一步 (TODO 第一条)**:**人工 Review PR #1 并合并 main**,然后进入 Phase 2(US-2 数据分析页)。
- **阻塞项**:等待人工合并 PR #1。

---

## 待办清单 (TODO,按优先级)

- [x] **Phase 0 — 需求确认**:用户审阅 `00-project-context.md`、`01-requirements.md`、`PROGRESS.md`,确认无误。
- [x] **Phase 1 — US-1 工程化初始化**:
  - [x] 从 `main` 开 feature 分支 `feature/1-project-init`
  - [x] 创建 `requirements.txt` 与 `requirements-dev.txt`
  - [x] 创建 `app/` 目录骨架(`main.py`, `pages/`, `model/`, `utils/`)
  - [x] 创建 `tests/` 目录与基础测试
  - [x] 创建 `.streamlit/config.toml`(端口 8004)
  - [x] 创建 `Dockerfile`
  - [x] 创建 `.github/workflows/ci.yml`(ruff + pytest + docker build)
  - [x] 创建 `.gitignore`(排除 `data/`, `models/`, `__pycache__`, `.venv/` 等)
  - [x] 本地自检全绿:ruff format ✅, ruff check ✅, pytest 100% ✅(docker build 跳过,本地无 Docker)
- [ ] **Phase 2 — US-2 数据分析页**:
  - [ ] 从 `main` 开 feature 分支 `feature/2-data-analysis`
  - [ ] 实现 `app/utils/data_loader.py`(load_csv + 缓存)
  - [ ] 实现 `app/pages/01_data_analysis.py`(统计摘要 + 直方图 + 柱状图 + 散点图 + 分组对比)
  - [ ] 编写测试 `tests/test_data_loader.py`、`tests/test_pages.py`
  - [ ] 本地自检全绿
  - [ ] 创建 PR,CI 全绿后合并 main
- [ ] **Phase 3 — US-3 模型训练**:
  - [ ] 从 `main` 开 feature 分支 `feature/3-model-training`
  - [ ] 实现 `app/model/train.py`(数据加载 → 预处理 → 训练 → 评估 → 保存)
  - [ ] 实现 `app/model/predict.py`(加载模型 + 推理)
  - [ ] 编写测试 `tests/test_train.py`、`tests/test_predict.py`
  - [ ] 运行训练,验证 AUC ≥ 0.70 并产出 `models/model.pkl`
  - [ ] 本地自检全绿
  - [ ] 创建 PR,CI 全绿后合并 main
- [ ] **Phase 4 — US-4 预测页**:
  - [ ] 从 `main` 开 feature 分支 `feature/4-prediction-page`
  - [ ] 实现 `app/pages/02_prediction.py`(表单 + 预测展示)
  - [ ] 处理模型缺失的友好提示
  - [ ] 编写测试
  - [ ] 本地自检全绿
  - [ ] 创建 PR,CI 全绿后合并 main
- [ ] **Phase 5 — US-5 本地启动与最终验证**:
  - [ ] 从 `main` 开 feature 分支 `feature/5-deploy-verify`
  - [ ] 编写 `README.md`(项目说明 + 启动步骤)
  - [ ] 验证 `streamlit run` 启动成功
  - [ ] 验证 Docker 构建与运行
  - [ ] 本地自检全绿
  - [ ] 创建 PR,CI 全绿后合并 main
  - [ ] **最终**:启动应用,将 URL (`http://localhost:8004`) 发给用户验证

---

## 关键决策记录 (ADR)

| 日期 | 决策 | 理由 |
|---|---|---|
| 2026-06-07 | 框架选 Streamlit | 纯 Python,快速构建数据交互页面;课程指定 |
| 2026-06-07 | 模型选 scikit-learn(逻辑回归/随机森林) | 轻量、无需 GPU、可解释;二分类任务标配 |
| 2026-06-07 | 不做 CD,仅本地部署 | 用户明确要求;CI 阶段构建 Docker 但不推送 |
| 2026-06-07 | 数据与模型不进 Git | 数据文件合计约 3.7 MB;模型文件二进制不可 diff;通过 .gitignore 排除 |
| 2026-06-07 | 端口固定 8004 | 用户指定 |
| 2026-06-07 | Dockerfile data/models 目录改为 VOLUME 挂载 | CI 环境无 gitignored 文件,COPY 失败;运行时通过 `-v` 挂载数据 |

---

## 已知坑 (GOTCHAS)

- **GitHub HTTPS 443 被墙,git push/pull 超时**:教学楼网络 DNS/防火墙拦截 HTTPS。解决:用 SSH 443 替代(`ssh://git@ssh.github.com:443/<user>/<repo>.git`),需先 `ssh-keyscan -p 443 ssh.github.com >> ~/.ssh/known_hosts`。
- **Dockerfile COPY data/models 在 CI 失败**:数据/模型目录被 `.gitignore` 排除,CI checkout 无这些目录,`COPY` 报错。解决:用 `RUN mkdir -p` 创建空目录 + `VOLUME` 声明;运行时通过 `-v` 挂载真实数据。

---

## 里程碑 (DONE)

- [x] 2026-06-07:完成 `00-project-context.md`、`01-requirements.md`、`PROGRESS.md` 初稿。
- [x] 2026-06-07:US-1 工程化初始化完成 — 本地自检全绿(ruff format ✅, ruff check ✅, pytest 100% ✅)。
