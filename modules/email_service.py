"""
📧 TONOSAMA Professional System - Email Service
1兆円ダイヤモンド級品質の戸塚さん完全連携システム

自動収益化メール送信とStreamlit統合
"""

import streamlit as st
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import io
import json

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailService:
    """メール送信サービスクラス"""
    
    def __init__(self):
        self.admin_email = st.secrets.get("admin_email", "nolimits1218@gmail.com")
        self.sendgrid_api_key = st.secrets.get("sendgrid_api_key", "")
        self.smtp_configured = bool(self.sendgrid_api_key)
        
        # 戸塚さんメールアドレス（固定）
        self.totsuka_email = "nolimits1218@gmail.com"
        
        # メールテンプレート
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, Dict]:
        """メールテンプレート読み込み"""
        return {
            "free_plan": {
                "subject": "【TONOSAMA】無料プラン - イチオシメニュー.txt送付",
                "body_template": """
戸塚様

いつもお世話になっております。
TONOSAMA Professional Systemより、新規店舗のイチオシメニューをお送りいたします。

【店舗情報】
店舗名: {store_name}
業種: {store_type}
システム利用日: {created_date}
プラン: 無料プラン

【イチオシメニュー】
{recommended_menu}

添付のイチオシメニュー.txtファイルをご確認ください。

※この店舗は無料プランのため、戸塚様への共有のみとなります。

システム自動送信
TONOSAMA Professional System
"""
            },
            "paid_plan_notification": {
                "subject": "【TONOSAMA】有料プラン利用完了通知 - 正太さん連携開始",
                "body_template": """
戸塚様

いつもお世話になっております。
TONOSAMA Professional Systemより、有料プラン利用完了をご報告いたします。

【店舗情報】
店舗名: {store_name}
業種: {store_type}
選択プラン: {selected_plan}
システム利用日: {created_date}
完了日時: {completion_date}

【処理内容】
• 14言語AI食レポ生成完了
• 正太さん形式CSV生成完了
• Google Driveフォルダ作成完了
• 完全パッケージ送信完了

【Google Driveリンク】
{google_drive_link}

【正太さんへの送信内容】
• 店舗基本情報CSV
• 店主ストーリー（14言語）CSV  
• メニュー情報（14言語）CSV
• AI食レポ（14言語）CSV
• 全画像ファイル

※正太さんには既に完全パッケージを送信済みです。

収益情報：
プラン料金: {plan_price}円

システム自動送信
TONOSAMA Professional System
"""
            },
            "error_notification": {
                "subject": "【TONOSAMA】システムエラー発生通知",
                "body_template": """
戸塚様

TONOSAMA Professional Systemにてエラーが発生いたしました。

【エラー情報】
発生日時: {error_time}
店舗名: {store_name}
エラー内容: {error_message}
エラー詳細: {error_details}

【システム状況】
セッションID: {session_id}
現在のステップ: {current_step}

お手数ですが、確認をお願いいたします。

システム自動送信
TONOSAMA Professional System
"""
            }
        }
    
    def is_configured(self) -> bool:
        """メール設定確認"""
        return bool(self.sendgrid_api_key)
    
    def send_free_plan_notification(self, store_info: Dict, recommended_menu: str) -> bool:
        """無料プラン通知送信"""
        try:
            template = self.templates["free_plan"]
            
            # メール本文作成
            body = template["body_template"].format(
                store_name=store_info.get("store_name_ja", "未設定"),
                store_type=store_info.get("store_type", "未設定"),
                created_date=datetime.now().strftime("%Y年%m月%d日"),
                recommended_menu=recommended_menu
            )
            
            # イチオシメニューファイル作成
            menu_file_content = f"""TONOSAMA Professional System
イチオシメニュー

店舗名: {store_info.get("store_name_ja", "未設定")}
推奨メニュー: {recommended_menu}
生成日時: {datetime.now().strftime("%Y年%m月%d日 %H時%M分")}

※このファイルは無料プランで生成されました。
"""
            
            # 添付ファイル準備
            attachments = [
                {
                    "filename": "イチオシメニュー.txt",
                    "content": menu_file_content.encode('utf-8'),
                    "content_type": "text/plain"
                }
            ]
            
            # メール送信
            return self._send_email(
                to_email=self.totsuka_email,
                subject=template["subject"],
                body=body,
                attachments=attachments
            )
            
        except Exception as e:
            logger.error(f"無料プラン通知送信エラー: {e}")
            return False
    
    def send_paid_plan_notification(self, store_info: Dict, plan_info: Dict, 
                                  google_drive_link: str = "") -> bool:
        """有料プラン完了通知送信"""
        try:
            template = self.templates["paid_plan_notification"]
            
            # プラン料金マッピング
            plan_prices = {
                "A4": 3000,
                "テント型": 5000
            }
            
            # メール本文作成
            body = template["body_template"].format(
                store_name=store_info.get("store_name_ja", "未設定"),
                store_type=store_info.get("store_type", "未設定"),
                selected_plan=plan_info.get("selected_plan", "未設定"),
                created_date=store_info.get("created_at", datetime.now().strftime("%Y年%m月%d日")),
                completion_date=datetime.now().strftime("%Y年%m月%d日 %H時%M分"),
                google_drive_link=google_drive_link or "作成中...",
                plan_price=plan_prices.get(plan_info.get("selected_plan", ""), 0)
            )
            
            # メール送信
            return self._send_email(
                to_email=self.totsuka_email,
                subject=template["subject"],
                body=body
            )
            
        except Exception as e:
            logger.error(f"有料プラン通知送信エラー: {e}")
            return False
    
    def send_error_notification(self, error_info: Dict) -> bool:
        """エラー通知送信"""
        try:
            template = self.templates["error_notification"]
            
            # メール本文作成
            body = template["body_template"].format(
                error_time=datetime.now().strftime("%Y年%m月%d日 %H時%M分"),
                store_name=error_info.get("store_name", "不明"),
                error_message=error_info.get("error_message", ""),
                error_details=error_info.get("error_details", ""),
                session_id=error_info.get("session_id", ""),
                current_step=error_info.get("current_step", "不明")
            )
            
            # メール送信
            return self._send_email(
                to_email=self.totsuka_email,
                subject=template["subject"],
                body=body
            )
            
        except Exception as e:
            logger.error(f"エラー通知送信エラー: {e}")
            return False
    
    def _send_email(self, to_email: str, subject: str, body: str, 
                   attachments: List[Dict] = None) -> bool:
        """メール送信（SendGrid使用）"""
        if not self.is_configured():
            logger.warning("SendGrid APIキーが設定されていません")
            return False
        
        try:
            # SendGrid API使用
            import sendgrid
            from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType
            
            sg = sendgrid.SendGridAPIClient(api_key=self.sendgrid_api_key)
            
            # メール作成
            message = Mail(
                from_email="system@tonosama.professional",
                to_emails=to_email,
                subject=subject,
                html_content=body.replace('\n', '<br>')
            )
            
            # 添付ファイル追加
            if attachments:
                for attachment_info in attachments:
                    attachment = Attachment(
                        FileContent(attachment_info["content"].decode('utf-8') if isinstance(attachment_info["content"], bytes) else attachment_info["content"]),
                        FileName(attachment_info["filename"]),
                        FileType(attachment_info.get("content_type", "text/plain"))
                    )
                    message.add_attachment(attachment)
            
            # 送信実行
            response = sg.send(message)
            
            if response.status_code == 202:
                logger.info(f"メール送信成功: {to_email}")
                return True
            else:
                logger.error(f"メール送信失敗: {response.status_code}")
                return False
                
        except ImportError:
            # SendGridライブラリがない場合のフォールバック
            logger.warning("SendGridライブラリが利用できません。SMTPを使用します")
            return self._send_email_smtp(to_email, subject, body, attachments)
            
        except Exception as e:
            logger.error(f"メール送信エラー: {e}")
            return False
    
    def _send_email_smtp(self, to_email: str, subject: str, body: str, 
                        attachments: List[Dict] = None) -> bool:
        """SMTP メール送信（フォールバック）"""
        try:
            # Gmail SMTP設定（実際の本番環境では適切な設定を使用）
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            smtp_username = self.admin_email
            smtp_password = st.secrets.get("gmail_app_password", "")
            
            if not smtp_password:
                logger.warning("Gmail App Passwordが設定されていません")
                return False
            
            # メッセージ作成
            msg = MIMEMultipart()
            msg['From'] = smtp_username
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # 本文添付
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # 添付ファイル処理
            if attachments:
                for attachment_info in attachments:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment_info["content"])
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename= "{attachment_info["filename"]}"'
                    )
                    msg.attach(part)
            
            # SMTP接続・送信
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_username, smtp_password)
            
            text = msg.as_string()
            server.sendmail(smtp_username, to_email, text)
            server.quit()
            
            logger.info(f"SMTP メール送信成功: {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"SMTP メール送信エラー: {e}")
            return False
    
    def test_connection(self) -> Tuple[bool, str]:
        """メール送信テスト"""
        try:
            test_result = self._send_email(
                to_email=self.totsuka_email,
                subject="【TONOSAMA】システム接続テスト",
                body=f"TONOSAMA Professional System接続テスト\n送信日時: {datetime.now().strftime('%Y年%m月%d日 %H時%M分')}"
            )
            
            if test_result:
                return True, "メール送信テスト成功"
            else:
                return False, "メール送信テスト失敗"
                
        except Exception as e:
            return False, f"テストエラー: {str(e)}"

# シングルトンインスタンス
_email_service_instance = None

def get_email_service() -> EmailService:
    """メールサービスインスタンス取得"""
    global _email_service_instance
    if _email_service_instance is None:
        _email_service_instance = EmailService()
    return _email_service_instance

def render_email_test_section():
    """メールテストセクション表示"""
    email_service = get_email_service()
    
    st.markdown("### 📧 戸塚さん連携テスト")
    
    if not email_service.is_configured():
        st.warning("""
        ⚠️ メール送信が設定されていません
        
        以下の設定が必要です：
        - SendGrid APIキー または Gmail App Password
        - secrets.tomlに認証情報設定
        """)
        return False
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("✅ メール送信設定済み")
        st.info(f"送信先: {email_service.totsuka_email}")
    
    with col2:
        if st.button("📧 接続テスト実行", type="secondary"):
            with st.spinner("メール送信テスト中..."):
                success, message = email_service.test_connection()
                
                if success:
                    st.success(f"✅ {message}")
                else:
                    st.error(f"❌ {message}")
    
    return True

def send_completion_notification(store_info: Dict, plan_type: str, 
                               google_drive_info: Dict = None):
    """完了通知自動送信"""
    email_service = get_email_service()
    
    if not email_service.is_configured():
        st.warning("メール送信が設定されていないため、通知をスキップします")
        return
    
    try:
        if plan_type == "無料":
            # 無料プラン: イチオシメニューのみ送信
            recommended_menu = store_info.get("recommended_menu", "未設定")
            success = email_service.send_free_plan_notification(store_info, recommended_menu)
        else:
            # 有料プラン: 完全パッケージ通知
            plan_info = {"selected_plan": plan_type}
            google_drive_link = google_drive_info.get("main_folder_link", "") if google_drive_info else ""
            success = email_service.send_paid_plan_notification(store_info, plan_info, google_drive_link)
        
        if success:
            st.success(f"✅ 戸塚さんに{plan_type}プラン完了通知を送信しました")
        else:
            st.error(f"❌ {plan_type}プラン通知送信に失敗しました")
            
    except Exception as e:
        logger.error(f"完了通知送信エラー: {e}")
        st.error(f"通知送信エラー: {e}")

def send_error_alert(error_info: Dict):
    """エラーアラート自動送信"""
    email_service = get_email_service()
    
    if email_service.is_configured():
        try:
            email_service.send_error_notification(error_info)
            logger.info("エラー通知を戸塚さんに送信しました")
        except Exception as e:
            logger.error(f"エラー通知送信失敗: {e}")