# 🏮 TONOSAMA Professional System - デプロイメントガイド

**1兆円ダイヤモンド級品質の完璧なデプロイメント手順**

## 📋 目次

- [前提条件](#前提条件)
- [ローカル開発環境](#ローカル開発環境)
- [Streamlit Community Cloud](#streamlit-community-cloud)
- [Docker デプロイ](#docker-デプロイ)
- [本番環境デプロイ](#本番環境デプロイ)
- [トラブルシューティング](#トラブルシューティング)

## 🔧 前提条件

### 必須要件
- Python 3.11+
- pip (最新版)
- Git
- OpenAI APIキー

### オプション要件
- Docker & Docker Compose
- Google Cloud Console アカウント (Google Drive連携用)
- SendGrid アカウント (メール送信用)

## 🏠 ローカル開発環境

### 1. リポジトリクローン

```bash
git clone [your-repo-url]
cd streamlit_tonosama_diamond
```

### 2. 仮想環境構築

```bash
# 仮想環境作成
python -m venv venv

# 仮想環境有効化
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### 3. 依存関係インストール

```bash
pip install -r requirements.txt
```

### 4. 設定ファイル作成

```bash
# 設定例をコピー
cp .streamlit/secrets.toml.example .streamlit/secrets.toml

# エディタで編集
nano .streamlit/secrets.toml
```

**secrets.toml の設定例:**

```toml
openai_api_key = "sk-your-actual-api-key-here"
admin_email = "nolimits1218@gmail.com"
```

### 5. アプリケーション起動

```bash
# 開発モード
./deploy.sh local

# または直接起動
streamlit run app.py
```

## ☁️ Streamlit Community Cloud

### 1. GitHubリポジトリ準備

```bash
# GitHubリポジトリ作成・プッシュ
git add .
git commit -m "🏮 TONOSAMA Professional System v2.0 Diamond Edition"
git push origin main
```

### 2. Streamlit Community Cloudでデプロイ

1. [Streamlit Community Cloud](https://share.streamlit.io) にアクセス
2. "New app" をクリック
3. GitHubリポジトリを選択
4. Branch: `main`
5. Main file path: `app.py`
6. App URL: `your-app-name` (例: `tonosama-professional`)

### 3. Secrets設定

アプリ設定の「Secrets」セクションで以下を設定:

```toml
openai_api_key = "sk-your-actual-api-key-here"
admin_email = "nolimits1218@gmail.com"
```

### 4. デプロイ実行

- "Deploy!" をクリック
- 数分でアプリが公開されます

## 🐳 Docker デプロイ

### 1. Docker イメージビルド

```bash
docker build -t tonosama-professional .
```

### 2. コンテナ実行

```bash
# 単体実行
docker run -p 8501:8501 tonosama-professional

# または Docker Compose使用
docker-compose up -d
```

### 3. アクセス確認

```
http://localhost:8501
```

## 🚀 本番環境デプロイ

### AWS EC2 デプロイ

```bash
# EC2インスタンス準備
sudo yum update -y
sudo yum install -y python3 pip git

# アプリケーション配置
git clone [your-repo-url]
cd streamlit_tonosama_diamond

# デプロイ実行
./deploy.sh production
```

### Google Cloud Run デプロイ

```bash
# Cloud Run用設定
gcloud builds submit --tag gcr.io/[PROJECT-ID]/tonosama-professional

# サービスデプロイ
gcloud run deploy --image gcr.io/[PROJECT-ID]/tonosama-professional --platform managed
```

### Heroku デプロイ

```bash
# Heroku CLI
heroku create tonosama-professional

# 環境変数設定
heroku config:set OPENAI_API_KEY=your-api-key

# デプロイ
git push heroku main
```

## 🔍 トラブルシューティング

### よくある問題と解決方法

#### 1. 依存関係エラー

```bash
# 解決方法
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

#### 2. OpenAI APIエラー

- APIキーの確認
- 使用量上限の確認
- ネットワーク接続の確認

#### 3. メモリ不足

```bash
# Docker の場合
docker run -m 2g -p 8501:8501 tonosama-professional
```

#### 4. ポート競合

```bash
# 別ポート使用
streamlit run app.py --server.port=8502
```

### ログ確認

```bash
# アプリケーションログ
tail -f streamlit.log

# Docker ログ
docker logs tonosama-professional

# Streamlit Cloud ログ
# Web UIのログセクションで確認
```

## 📊 パフォーマンス最適化

### キャッシュ設定

```python
# アプリ内で設定済み
@st.cache_data
@st.cache_resource
```

### メモリ使用量最適化

- セッション状態の定期クリア
- 大きなファイルの適切な処理
- 不要なデータの削除

## 🔐 セキュリティ設定

### 本番環境での注意事項

1. **secrets.toml を Git に含めない**
   ```bash
   echo ".streamlit/secrets.toml" >> .gitignore
   ```

2. **HTTPS使用を強制**
   - リバースプロキシ設定
   - SSL証明書設定

3. **ファイアウォール設定**
   - 必要なポートのみ開放
   - 不正アクセス監視

## 📞 サポート

### お問い合わせ

- **メール**: nolimits1218@gmail.com
- **システム管理**: 戸塚さん・正太さん連携
- **緊急対応**: 24時間監視システム

### 機能追加・カスタマイズ

1兆円ダイヤモンド級品質により、お客様のニーズに合わせた完全カスタマイズが可能です。

---

**🏮 TONOSAMA Professional System v2.0 Diamond Edition**  
*外国人観光客向け完璧多言語レストランシステム*

© 2024 TONOSAMA Professional - All Rights Reserved