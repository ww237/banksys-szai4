ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim

WORKDIR /app

# Install production dependencies
COPY requirements.txt .
ARG PIP_INDEX_URL=https://pypi.org/simple
RUN pip install --no-cache-dir --timeout 120 -i "${PIP_INDEX_URL}" -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY .streamlit/ ./.streamlit/

# Copy data (for local deployment; excluded from Git)
COPY data/ ./data/

# Copy pre-trained model if exists
COPY models/ ./models/ 2>/dev/null || true

EXPOSE 8004

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8004/_stcore/health')" || exit 1

ENTRYPOINT ["streamlit", "run", "app/main.py", "--server.port=8004", "--server.address=0.0.0.0"]
