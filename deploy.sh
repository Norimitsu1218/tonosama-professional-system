#!/bin/bash

# 🏮 TONOSAMA Professional System - Deployment Script
# 1兆円ダイヤモンド級品質の完璧なデプロイメントスクリプト

set -e

echo "🏮 TONOSAMA Professional System - デプロイメント開始"
echo "=================================================="

# 環境変数チェック
check_environment() {
    echo "📋 環境チェック中..."
    
    # Python環境
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python3が見つかりません"
        exit 1
    fi
    
    # pip環境
    if ! command -v pip &> /dev/null; then
        echo "❌ pipが見つかりません"  
        exit 1
    fi
    
    echo "✅ 基本環境OK"
}

# 依存関係インストール
install_dependencies() {
    echo "📦 依存関係インストール中..."
    
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        echo "✅ 依存関係インストール完了"
    else
        echo "❌ requirements.txtが見つかりません"
        exit 1
    fi
}

# 設定ファイル確認
check_config() {
    echo "⚙️ 設定ファイル確認中..."
    
    if [ ! -f ".streamlit/secrets.toml" ]; then
        echo "⚠️ secrets.tomlが見つかりません"
        echo "💡 .streamlit/secrets.toml.exampleを参考に設定ファイルを作成してください"
    fi
    
    if [ ! -f ".streamlit/config.toml" ]; then
        echo "⚠️ config.tomlが見つかりません"
        echo "💡 デフォルト設定で起動します"
    fi
    
    echo "✅ 設定ファイル確認完了"
}

# アプリケーション起動
start_application() {
    echo "🚀 アプリケーション起動中..."
    
    if [ "$1" = "production" ]; then
        echo "🎯 本番モードで起動"
        streamlit run app.py --server.port=8501 --server.address=0.0.0.0
    else
        echo "🔧 開発モードで起動"
        streamlit run app.py
    fi
}

# Docker デプロイ
deploy_docker() {
    echo "🐳 Docker デプロイ実行中..."
    
    if command -v docker &> /dev/null; then
        docker build -t tonosama-professional .
        docker run -p 8501:8501 tonosama-professional
        echo "✅ Docker デプロイ完了"
    else
        echo "❌ Dockerが見つかりません"
        exit 1
    fi
}

# Streamlit Community Cloud 用準備
prepare_streamlit_cloud() {
    echo "☁️ Streamlit Community Cloud 準備中..."
    
    # 必要ファイル確認
    required_files=("app.py" "requirements.txt" ".streamlit/config.toml")
    
    for file in "${required_files[@]}"; do
        if [ ! -f "$file" ]; then
            echo "❌ 必要ファイルが見つかりません: $file"
            exit 1
        fi
    done
    
    echo "✅ Streamlit Community Cloud 準備完了"
    echo "💡 GitHubにプッシュしてから https://share.streamlit.io でデプロイしてください"
}

# メイン処理
main() {
    case "$1" in
        "local")
            check_environment
            install_dependencies
            check_config
            start_application
            ;;
        "production")
            check_environment
            install_dependencies
            check_config
            start_application "production"
            ;;
        "docker")
            deploy_docker
            ;;
        "cloud")
            prepare_streamlit_cloud
            ;;
        *)
            echo "使用方法: $0 {local|production|docker|cloud}"
            echo ""
            echo "オプション:"
            echo "  local      - ローカル開発環境で起動"
            echo "  production - 本番環境で起動"  
            echo "  docker     - Docker環境で起動"
            echo "  cloud      - Streamlit Community Cloud準備"
            exit 1
            ;;
    esac
}

# スクリプト実行
main "$@"

echo ""
echo "🎉 デプロイメント処理完了"
echo "🏮 TONOSAMA Professional System が稼働中です"