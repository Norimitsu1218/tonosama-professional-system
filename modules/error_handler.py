"""
🛡️ TONOSAMA Professional System - Error Handler
1兆円ダイヤモンド級品質の完璧なエラーハンドリングシステム

包括的エラー処理・ユーザーフレンドリーなメッセージ・自動復旧機能
"""

import streamlit as st
import logging
import traceback
import functools
from typing import Callable, Any, Optional, Dict, List
from datetime import datetime
from dataclasses import dataclass
from modules.email_service import send_error_alert

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ErrorInfo:
    """エラー情報データクラス"""
    error_type: str
    error_message: str
    error_details: str
    timestamp: str
    user_message: str
    solution_hint: str
    error_code: str = ""
    recovery_action: str = ""

class TONOSAMAErrorHandler:
    """TONOSAMAエラーハンドラー"""
    
    def __init__(self):
        self.error_messages = self._load_error_messages()
        self.solution_hints = self._load_solution_hints()
    
    def _load_error_messages(self) -> Dict[str, str]:
        """ユーザーフレンドリーなエラーメッセージ"""
        return {
            "OpenAIError": "🤖 AI処理でエラーが発生しました",
            "AuthenticationError": "🔑 APIキーの認証に失敗しました", 
            "RateLimitError": "⏰ AI処理の制限に達しました",
            "ValidationError": "📋 入力データに不備があります",
            "FileNotFoundError": "📂 ファイルが見つかりません",
            "PermissionError": "🔒 ファイルへのアクセス権限がありません",
            "ConnectionError": "🌐 ネットワーク接続でエラーが発生しました",
            "TimeoutError": "⏱️ 処理がタイムアウトしました",
            "ImportError": "📦 必要なライブラリが不足しています",
            "KeyError": "🔑 必要なデータが不足しています",
            "ValueError": "💢 データの形式が正しくありません",
            "AttributeError": "⚙️ システム内部でエラーが発生しました",
            "TypeError": "🔧 データ型が正しくありません",
            "GoogleDriveError": "☁️ Google Drive連携でエラーが発生しました",
            "EmailError": "📧 メール送信でエラーが発生しました",
            "CSVError": "📊 CSV生成でエラーが発生しました",
            "ImageError": "🖼️ 画像処理でエラーが発生しました",
            "StateError": "💾 状態管理でエラーが発生しました"
        }
    
    def _load_solution_hints(self) -> Dict[str, str]:
        """解決方法のヒント"""
        return {
            "OpenAIError": "OpenAI APIキーを確認し、アカウントに十分なクレジットがあることを確認してください",
            "AuthenticationError": "secrets.tomlファイルのAPIキーが正しく設定されていることを確認してください",
            "RateLimitError": "しばらく時間をおいてから再度お試しください。有料プランへのアップグレードもご検討ください",
            "ValidationError": "入力フィールドをすべて正しく入力しているか確認してください",
            "FileNotFoundError": "ファイルパスが正しいことを確認し、ファイルが存在することを確認してください",
            "PermissionError": "ファイルやフォルダのアクセス権限を確認してください",
            "ConnectionError": "インターネット接続を確認し、ファイアウォール設定をチェックしてください",
            "TimeoutError": "処理を再実行してください。問題が続く場合は処理するデータを小さくしてください",
            "ImportError": "requirements.txtの依存関係をpip installで再インストールしてください",
            "KeyError": "必要なデータがすべて入力されているか確認してください",
            "ValueError": "入力データの形式を確認してください（数値、日付、文字列など）",
            "AttributeError": "ページを再読み込みし、問題が続く場合はセッションをリセットしてください",
            "TypeError": "入力データの型を確認してください",
            "GoogleDriveError": "Google Drive APIの設定を確認し、認証情報をチェックしてください",
            "EmailError": "メール設定（SendGrid APIキー）を確認してください",
            "CSVError": "データの内容を確認し、特殊文字が含まれていないか確認してください",
            "ImageError": "画像ファイルの形式（JPG、PNG）とサイズ（10MB以下）を確認してください",
            "StateError": "セッションをリセットしてから再度お試しください"
        }
    
    def get_error_type(self, error: Exception) -> str:
        """エラータイプを取得"""
        error_class = error.__class__.__name__
        
        # 特定のエラーマッピング
        if "openai" in str(error).lower() or "gpt" in str(error).lower():
            return "OpenAIError"
        elif "authentication" in str(error).lower():
            return "AuthenticationError"  
        elif "rate limit" in str(error).lower():
            return "RateLimitError"
        elif "validation" in str(error).lower():
            return "ValidationError"
        elif "google" in str(error).lower() and "drive" in str(error).lower():
            return "GoogleDriveError"
        elif "email" in str(error).lower() or "mail" in str(error).lower():
            return "EmailError"
        elif "csv" in str(error).lower():
            return "CSVError"
        elif "image" in str(error).lower() or "PIL" in str(error):
            return "ImageError"
        elif "state" in str(error).lower():
            return "StateError"
        else:
            return error_class
    
    def handle_error(self, error: Exception, context: str = "", 
                    show_details: bool = False, 
                    auto_recover: bool = True) -> ErrorInfo:
        """包括的エラー処理"""
        try:
            error_type = self.get_error_type(error)
            error_message = str(error)
            error_details = traceback.format_exc()
            timestamp = datetime.now().isoformat()
            
            # ユーザーフレンドリーメッセージ
            user_message = self.error_messages.get(
                error_type, 
                f"🚨 予期しないエラーが発生しました: {error_type}"
            )
            
            # 解決方法のヒント
            solution_hint = self.solution_hints.get(
                error_type,
                "ページを再読み込みしてから再度お試しください。問題が続く場合はシステム管理者にご連絡ください"
            )
            
            # エラー情報作成
            error_info = ErrorInfo(
                error_type=error_type,
                error_message=error_message,
                error_details=error_details,
                timestamp=timestamp,
                user_message=user_message,
                solution_hint=solution_hint
            )
            
            # ログ出力
            logger.error(f"エラー発生 [{context}]: {error_type} - {error_message}")
            
            # Streamlitでの表示
            self._display_error(error_info, show_details)
            
            # エラー通知送信（重大なエラーの場合）
            if self._is_critical_error(error_type):
                self._send_error_notification(error_info, context)
            
            # 自動復旧試行
            if auto_recover:
                self._attempt_auto_recovery(error_type)
            
            return error_info
            
        except Exception as handler_error:
            # エラーハンドラー自体のエラー
            logger.critical(f"エラーハンドラーでエラー発生: {handler_error}")
            st.error("システムでクリティカルなエラーが発生しました。管理者にお問い合わせください。")
            return ErrorInfo("CriticalError", str(handler_error), "", timestamp, "システムエラー", "管理者に連絡")
    
    def _display_error(self, error_info: ErrorInfo, show_details: bool = False):
        """Streamlitでのエラー表示"""
        # メインエラーメッセージ
        st.error(error_info.user_message)
        
        # 解決方法のヒント
        st.info(f"💡 **解決方法**: {error_info.solution_hint}")
        
        # 詳細情報（オプション）
        if show_details:
            with st.expander("🔍 エラー詳細情報", expanded=False):
                st.code(f"""
エラータイプ: {error_info.error_type}
発生時刻: {error_info.timestamp}
エラーメッセージ: {error_info.error_message}

詳細:
{error_info.error_details}
                """, language="text")
        else:
            if st.button("🔍 エラー詳細を表示"):
                st.session_state[f"show_error_details_{hash(error_info.timestamp)}"] = True
                st.rerun()
    
    def _is_critical_error(self, error_type: str) -> bool:
        """クリティカルエラーかどうかを判定"""
        critical_errors = [
            "StateError", "AuthenticationError", "PermissionError", 
            "CriticalError", "ImportError"
        ]
        return error_type in critical_errors
    
    def _send_error_notification(self, error_info: ErrorInfo, context: str):
        """エラー通知送信"""
        try:
            notification_data = {
                "error_time": error_info.timestamp,
                "store_name": st.session_state.get("store_name", "不明"),
                "error_message": error_info.user_message,
                "error_details": f"Type: {error_info.error_type}\nContext: {context}\nMessage: {error_info.error_message}",
                "session_id": st.session_state.get("session_id", "不明"),
                "current_step": st.session_state.get("current_step", "不明")
            }
            
            send_error_alert(notification_data)
            
        except Exception as e:
            logger.error(f"エラー通知送信失敗: {e}")
    
    def _attempt_auto_recovery(self, error_type: str):
        """自動復旧試行"""
        try:
            if error_type == "StateError":
                st.info("🔄 状態の自動復旧を試行中...")
                # 状態リセット
                if st.button("状態をリセット"):
                    st.session_state.clear()
                    st.rerun()
                    
            elif error_type == "ValidationError":
                st.info("📋 入力データの検証を行ってください")
                
            elif error_type == "TimeoutError":
                st.info("⏱️ 処理を再実行してください")
                if st.button("🔄 再実行"):
                    st.rerun()
                    
        except Exception as e:
            logger.error(f"自動復旧失敗: {e}")

# グローバルインスタンス
_error_handler = TONOSAMAErrorHandler()

def get_error_handler() -> TONOSAMAErrorHandler:
    """エラーハンドラーインスタンス取得"""
    return _error_handler

def handle_errors(context: str = "", show_details: bool = False, auto_recover: bool = True):
    """エラーハンドリングデコレータ"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_handler = get_error_handler()
                error_handler.handle_error(e, context, show_details, auto_recover)
                return None
        return wrapper
    return decorator

def safe_execute(func: Callable, *args, context: str = "", **kwargs) -> Any:
    """安全な関数実行"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        error_handler = get_error_handler()
        error_handler.handle_error(e, context)
        return None

def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> List[str]:
    """必須フィールドバリデーション"""
    missing_fields = []
    
    for field in required_fields:
        if field not in data or not data[field]:
            missing_fields.append(field)
    
    return missing_fields

def validate_openai_connection() -> bool:
    """OpenAI接続バリデーション"""
    try:
        import openai
        
        # APIキー確認
        api_key = st.secrets.get("openai_api_key")
        if not api_key:
            st.error("🔑 OpenAI APIキーが設定されていません")
            st.info("💡 **解決方法**: secrets.tomlファイルにopenai_api_keyを設定してください")
            return False
        
        # 簡単な接続テスト（実際のAPI呼び出しは行わない）
        if not api_key.startswith("sk-"):
            st.error("🔑 OpenAI APIキーの形式が正しくありません")
            st.info("💡 **解決方法**: APIキーは'sk-'で始まる必要があります")
            return False
        
        return True
        
    except ImportError:
        st.error("📦 OpenAIライブラリがインストールされていません")
        st.info("💡 **解決方法**: pip install openai を実行してください")
        return False
    except Exception as e:
        error_handler = get_error_handler()
        error_handler.handle_error(e, "OpenAI接続検証")
        return False

def validate_file_upload(uploaded_file, allowed_types: List[str], max_size_mb: int = 10) -> bool:
    """ファイルアップロードバリデーション"""
    if uploaded_file is None:
        return False
    
    try:
        # ファイル形式チェック
        file_type = uploaded_file.type
        if not any(allowed_type in file_type for allowed_type in allowed_types):
            st.error(f"🚫 サポートされていないファイル形式です: {file_type}")
            st.info(f"💡 **対応形式**: {', '.join(allowed_types)}")
            return False
        
        # ファイルサイズチェック
        file_size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
        if file_size_mb > max_size_mb:
            st.error(f"🚫 ファイルサイズが大きすぎます: {file_size_mb:.1f}MB")
            st.info(f"💡 **制限**: {max_size_mb}MB以下のファイルをアップロードしてください")
            return False
        
        return True
        
    except Exception as e:
        error_handler = get_error_handler()
        error_handler.handle_error(e, "ファイルアップロード検証")
        return False

def render_error_recovery_panel():
    """エラー復旧パネル表示"""
    with st.expander("🛡️ システム復旧オプション", expanded=False):
        st.markdown("### システム復旧オプション")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 ページリロード", use_container_width=True):
                st.rerun()
            
            if st.button("🗑️ キャッシュクリア", use_container_width=True):
                st.cache_data.clear()
                st.success("キャッシュをクリアしました")
        
        with col2:
            if st.button("💾 セッションリセット", use_container_width=True):
                if st.session_state.get('confirm_session_reset'):
                    st.session_state.clear()
                    st.rerun()
                else:
                    st.session_state['confirm_session_reset'] = True
                    st.warning("もう一度押すとセッションがリセットされます")
            
            if st.button("🏠 ホームに戻る", use_container_width=True):
                st.switch_page("app.py")

def init_error_handling():
    """エラーハンドリング初期化"""
    # Streamlitのエラーハンドリング設定
    st.set_option('client.showErrorDetails', False)
    
    logger.info("TONOSAMA Error Handling System 初期化完了")