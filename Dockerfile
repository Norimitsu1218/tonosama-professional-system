# 🏮 TONOSAMA Professional System - Docker Configuration
# 1兆円ダイヤモンド級品質の完璧なDockerイメージ

FROM python:3.11-slim

# システム依存関係インストール
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリ設定
WORKDIR /app

# 依存関係ファイルコピー
COPY requirements.txt .

# Python依存関係インストール
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# アプリケーションファイルコピー
COPY . .

# ポート公開
EXPOSE 8501

# ヘルスチェック
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# アプリケーション実行
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]