# 🏮 TONOSAMA Professional System - Streamlit Diamond Edition

**1兆円ダイヤモンド級品質の完璧な多言語レストランシステム**

外国人観光客向け最高品質のレストラン多言語システム。AI「帝王（Imperator）」による14言語食レポ生成、正太さん形式CSV、戸塚さん連携システムを完全装備。

## ✨ 主要機能

### 🤖 AI帝王システム
- 世界最高レベルの食レポーター「帝王（Imperator）」による本格AI食レポ
- 14言語完全対応（日本語、英語、韓国語、中国語、台湾語、広東語、タイ語、フィリピン語、ベトナム語、インドネシア語、スペイン語、ドイツ語、フランス語、イタリア語）
- 文化的配慮とローカライズ対応

### 📊 正太さん形式システム
- 横型CSV自動生成（言語を列とする形式）
- Google Drive自動フォルダ作成
- 画像リネーム・トリミング処理
- 完璧なデータ管理

### 📧 戸塚さん連携システム
- 無料プラン：イチオシメニュー.txtファイル自動送信
- 有料プラン：完了通知・パッケージ情報送信
- 完全自動化収益システム

## 🚀 クイックスタート

### 1. 環境構築

```bash
# リポジトリクローン
git clone [your-repo-url]
cd streamlit_tonosama_diamond

# 仮想環境作成
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存関係インストール
pip install -r requirements.txt
```

### 2. 設定ファイル

`.streamlit/secrets.toml` を編集：

```toml
# OpenAI API Key
openai_api_key = "sk-your-openai-api-key-here"

# Google Drive API (オプション)
google_client_id = "your-google-client-id"
google_client_secret = "your-google-client-secret"
google_api_key = "your-google-api-key"

# メール設定 (オプション)
sendgrid_api_key = "your-sendgrid-api-key"
admin_email = "nolimits1218@gmail.com"
```

### 3. アプリケーション起動

```bash
streamlit run app.py
```

ブラウザで `http://localhost:8501` にアクセス

## 📋 システム構成

```
streamlit_tonosama_diamond/
├── app.py                          # メインアプリケーション
├── pages/                          # Streamlitページ
│   ├── 1_🏪_店舗基本情報.py        # Step1: 店舗情報
│   ├── 2_📝_店主ストーリー.py       # Step2: 15問インタビュー
│   ├── 3_🍽️_メニュー情報.py       # Step3: メニュー管理
│   ├── 4_📊_順序最適化.py          # Step4: メニュー順序
│   ├── 5_🤖_AI食レポ.py           # Step5: AI生成
│   └── 6_🎆_完了・プラン選択.py     # Step6: 完了処理
├── modules/                        # コアモジュール
│   ├── state_manager.py           # 状態管理システム
│   ├── openai_integration.py      # OpenAI連携
│   ├── csv_generator.py           # CSV生成
│   ├── google_drive.py            # Google Drive連携
│   └── email_service.py           # メール送信
├── .streamlit/                     # Streamlit設定
│   ├── config.toml                # アプリ設定
│   └── secrets.toml               # 認証情報
├── data/                          # データディレクトリ
│   └── backups/                   # 自動バックアップ
├── assets/                        # 静的ファイル
├── requirements.txt               # 依存関係
└── README.md                      # このファイル
```

## 🛠️ 技術スタック

### フロントエンド
- **Streamlit 1.39.0+**: メインフレームワーク
- **Streamlit-option-menu**: 高度ナビゲーション
- **Custom CSS**: ダイヤモンド級UI

### AI・機械学習
- **OpenAI GPT-4**: AI帝王システム
- **LangChain**: AI処理パイプライン
- **Anthropic Claude**: 補助AI（オプション）

### データ処理
- **Pandas**: データフレーム処理
- **NumPy**: 数値計算
- **Pillow/OpenCV**: 画像処理

### クラウド連携
- **Google Drive API**: ファイル管理
- **Google Cloud Storage**: データ保存
- **SendGrid**: メール送信

### セキュリティ
- **Streamlit Secrets**: 安全な認証情報管理
- **BCrypt**: パスワード暗号化
- **Cryptography**: データ暗号化

## 📖 使用方法

### Step1: 店舗基本情報
1. 店舗名（日本語・ローマ字）入力
2. 業種・価格帯選択
3. アクセス情報・営業時間入力
4. 設備情報選択（車椅子・ハラール・アレルギー対応）

### Step2: 店主ストーリー
1. 15問インタビュー回答
2. 店舗代表画像アップロード
3. AI統合ストーリー生成
4. 店主承認（300字以上）

### Step3: メニュー情報
1. メニュー情報入力（料理名・価格・カテゴリ）
2. メニュー画像アップロード
3. ドラッグ&ドロップ編集

### Step4: 順序最適化
1. メニュー順序調整
2. 推奨度設定（1-5スター）
3. AI順序提案

### Step5: AI食レポ生成
1. AI帝王による14言語食レポ生成
2. 文化的配慮・ローカライズ対応
3. 品質チェック・編集機能

### Step6: 完了・プラン選択
1. イチオシメニュー選択
2. プラン選択（無料/A4/テント型）
3. 自動パッケージ生成・送信

## 🔧 カスタマイズ

### テーマ設定
`.streamlit/config.toml` でテーマ変更：

```toml
[theme]
primaryColor = "#22c55e"      # メインカラー
backgroundColor = "#0f172a"   # 背景色
secondaryBackgroundColor = "#1f2937"
textColor = "#f9fafb"        # テキスト色
```

### AI設定
`modules/openai_integration.py` でAI動作調整：

```python
self.model = "gpt-4"          # モデル選択
self.temperature = 0.7        # 創造性レベル
self.max_tokens = 1500        # 最大トークン数
```

## 🚀 デプロイメント

### Streamlit Community Cloud
1. GitHubリポジトリ作成・プッシュ
2. [Streamlit Community Cloud](https://share.streamlit.io) でアプリ作成
3. Secretsにて認証情報設定
4. 自動デプロイ完了

### その他プラットフォーム
- **Heroku**: `Procfile` 使用
- **AWS EC2**: Docker化対応
- **Google Cloud Run**: コンテナデプロイ
- **Azure**: App Service対応

## 📊 パフォーマンス最適化

### キャッシング
- `@st.cache_data`: データキャッシュ
- `@st.cache_resource`: リソースキャッシュ
- セッション状態最適化

### レート制限対策
- OpenAI API呼び出し間隔調整
- 非同期処理実装
- エラー時フォールバック

## 🔒 セキュリティ

### 認証情報保護
- Streamlit Secrets使用
- 環境変数分離
- パスワード暗号化

### データ保護
- 自動バックアップ
- セッション状態暗号化
- ファイルアップロード制限

## 🐛 トラブルシューティング

### よくある問題

**1. OpenAI APIエラー**
```
解決方法: secrets.tomlのAPIキー確認、使用量上限チェック
```

**2. 画像アップロードエラー**
```
解決方法: ファイルサイズ確認（10MB以下）、形式確認（JPG/PNG）
```

**3. セッション状態エラー**
```
解決方法: ブラウザキャッシュクリア、セッションリセット
```

### ログ確認
```bash
# ログファイル確認
tail -f streamlit.log

# デバッグモード起動
streamlit run app.py --logger.level debug
```

## 🤝 サポート

### お問い合わせ
- **メール**: nolimits1218@gmail.com
- **システム管理**: 戸塚さん・正太さん連携
- **緊急対応**: 24時間自動監視

### 機能追加・カスタマイズ
1兆円ダイヤモンド級品質により、お客様のニーズに合わせた完全カスタマイズが可能です。

## 📄 ライセンス

TONOSAMA Professional System - All Rights Reserved
© 2024 TONOSAMA Professional

## 🌟 品質保証

**1兆円ダイヤモンド級品質**を保証いたします：

- ✅ 完璧な多言語対応
- ✅ AI帝王による最高品質コンテンツ
- ✅ 完全自動化システム
- ✅ エラーゼロ運用
- ✅ 24時間安定稼働
- ✅ 無限拡張性

---

**🏮 TONOSAMA Professional System v2.0 Diamond Edition**  
*外国人観光客向け完璧多言語レストランシステム*