"""
🏮 TONOSAMA Professional System - Modules Package
1兆円ダイヤモンド級品質のモジュールパッケージ

全てのコアモジュールを統合管理
"""

__version__ = "2.0.0"
__author__ = "TONOSAMA Professional"
__description__ = "外国人観光客向け完璧多言語レストランシステム"

# モジュール情報
MODULES = {
    "state_manager": "状態管理システム",
    "openai_integration": "OpenAI連携システム", 
    "csv_generator": "CSV生成システム",
    "google_drive": "Google Drive連携システム",
    "email_service": "メール送信システム",
    "ui_styling": "UIスタイリングシステム",
    "error_handler": "エラーハンドリングシステム"
}

def get_module_info():
    """モジュール情報取得"""
    return {
        "version": __version__,
        "author": __author__, 
        "description": __description__,
        "modules": MODULES
    }