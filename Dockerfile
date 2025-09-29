FROM python:3.9-slim

# 作業ディレクトリの設定
WORKDIR /app

# システムパッケージの更新と必要なパッケージのインストール
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Pythonの依存関係をコピーしてインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# spaCyの日本語モデルをダウンロード
RUN python -m spacy download ja_core_news_sm

# アプリケーションコードをコピー
COPY . .

# ログディレクトリの作成
RUN mkdir -p logs

# ポートの公開
EXPOSE 8000

# アプリケーションの起動
CMD ["python", "main.py"]
