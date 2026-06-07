# 🏦 banksys-szai4 — 银行营销预测系统

基于银行电话营销数据,提供**交互式数据分析**与**客户认购预测**的 Web 应用。

## 功能

- 📊 **数据分析**:交互式探索数据分布、特征关系与认购意向关联(4 个分析 Tab)
- 🔮 **在线预测**:点选输入客户特征,实时预测是否会认购定期存款

## 技术栈

Python 3.11 · Streamlit · scikit-learn · plotly · pandas · pytest · ruff · Docker

## 快速开始

### 1. 准备数据

确保 `data/train.csv` 和 `data/test.csv` 已放置在项目 `data/` 目录下。

### 2. 安装依赖

```bash
pip install -r requirements.txt -r requirements-dev.txt
# 国内用户可使用清华镜像:
# pip install -r requirements.txt -r requirements-dev.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 3. 训练模型(首次使用)

```bash
python -m app.model.train
```

训练完成后会在 `models/` 目录生成:
- `model.pkl` — 随机森林分类器
- `encoder.pkl` — 特征编码器
- `metrics.json` — 评估指标(AUC, accuracy 等)

### 4. 启动应用

```bash
streamlit run app/main.py
```

浏览器访问 **http://localhost:8004**

## 健康检查

```bash
curl http://localhost:8004/_stcore/health
```

## Docker 部署

```bash
# 构建镜像
docker build -t banksys-szai4 .

# 运行容器(挂载 data 和 models 目录)
docker run -d \
  -p 8004:8004 \
  -v "$(pwd)/data:/app/data" \
  -v "$(pwd)/models:/app/models" \
  --name banksys-szai4 \
  banksys-szai4
```

## 运行测试

```bash
pytest --cov=app --cov-fail-under=80
```

## 代码检查

```bash
ruff format --check .
ruff check .
```

## 项目结构

```text
banksys-szai4/
├── app/                  # 应用主目录
│   ├── main.py           # Streamlit 入口
│   ├── pages/            # 页面(数据分析 + 预测)
│   ├── model/            # 模型训练/推理/预处理
│   └── utils/            # 数据加载 + 分析工具
├── tests/                # 单元测试(30 个用例)
├── data/                 # 数据文件(不进 Git)
├── models/               # 模型产物(不进 Git)
├── standards/            # 项目规范与活文档
├── Dockerfile
└── .github/workflows/    # CI 流水线
```
