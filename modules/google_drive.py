"""
🗂️ TONOSAMA Professional System - Google Drive Integration
1兆円ダイヤモンド級品質のGoogle Drive完全連携システム

正太さん形式フォルダ・ファイル管理とStreamlit連携
"""

import streamlit as st
import os
import io
import json
from typing import Dict, List, Optional, Tuple
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow
import logging
from datetime import datetime

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GoogleDriveIntegration:
    """Google Drive連携クラス"""
    
    def __init__(self):
        self.service = None
        self.credentials = None
        self.scopes = [
            'https://www.googleapis.com/auth/drive.file',
            'https://www.googleapis.com/auth/drive.readonly'
        ]
        self.client_config = self._get_client_config()
    
    def _get_client_config(self) -> Optional[Dict]:
        """クライアント設定取得"""
        try:
            return {
                "web": {
                    "client_id": st.secrets.get("google_client_id", ""),
                    "client_secret": st.secrets.get("google_client_secret", ""),
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": ["http://localhost:8501"]
                }
            }
        except Exception as e:
            logger.warning(f"Google認証情報未設定: {e}")
            return None
    
    def is_configured(self) -> bool:
        """Google Drive設定確認"""
        return (
            self.client_config and 
            self.client_config["web"]["client_id"] and
            self.client_config["web"]["client_secret"]
        )
    
    def authenticate(self) -> bool:
        """Google Drive認証"""
        if not self.is_configured():
            return False
        
        try:
            # セッション状態から認証情報取得
            if "google_credentials" in st.session_state:
                creds_info = st.session_state["google_credentials"]
                self.credentials = Credentials.from_authorized_user_info(creds_info, self.scopes)
                
                # 認証情報の有効性確認・更新
                if not self.credentials.valid:
                    if self.credentials.expired and self.credentials.refresh_token:
                        self.credentials.refresh(Request())
                        st.session_state["google_credentials"] = json.loads(self.credentials.to_json())
                    else:
                        return False
                
                # Google Drive サービス構築
                self.service = build('drive', 'v3', credentials=self.credentials)
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Google認証エラー: {e}")
            return False
    
    def get_auth_url(self) -> Optional[str]:
        """認証URL取得"""
        if not self.is_configured():
            return None
        
        try:
            flow = Flow.from_client_config(
                self.client_config, 
                scopes=self.scopes,
                redirect_uri="http://localhost:8501"
            )
            
            auth_url, _ = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true'
            )
            
            # Flowをセッション状態に保存
            st.session_state["oauth_flow"] = flow
            
            return auth_url
            
        except Exception as e:
            logger.error(f"認証URL生成エラー: {e}")
            return None
    
    def complete_auth(self, auth_code: str) -> bool:
        """認証完了処理"""
        try:
            if "oauth_flow" not in st.session_state:
                return False
            
            flow = st.session_state["oauth_flow"]
            flow.fetch_token(code=auth_code)
            
            self.credentials = flow.credentials
            st.session_state["google_credentials"] = json.loads(self.credentials.to_json())
            
            # Google Drive サービス構築
            self.service = build('drive', 'v3', credentials=self.credentials)
            
            # 認証フロー情報削除
            del st.session_state["oauth_flow"]
            
            return True
            
        except Exception as e:
            logger.error(f"認証完了エラー: {e}")
            return False
    
    def create_store_folder(self, store_name: str) -> Optional[str]:
        """店舗専用フォルダ作成"""
        if not self.service:
            logger.error("Google Driveサービスが初期化されていません")
            return None
        
        try:
            # メインフォルダ作成
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            folder_name = f"TONOSAMA_{store_name}_{timestamp}"
            
            folder_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder',
                'description': f'TONOSAMA Professional System - {store_name} 店舗データ'
            }
            
            folder = self.service.files().create(body=folder_metadata, fields='id,name,webViewLink').execute()
            folder_id = folder.get('id')
            
            logger.info(f"メインフォルダ作成: {folder_name} (ID: {folder_id})")
            
            # サブフォルダ作成
            subfolders = [
                "01_店舗基本情報",
                "02_店主ストーリー",
                "03_メニュー情報",
                "04_AI食レポ",
                "05_完成パッケージ"
            ]
            
            for subfolder_name in subfolders:
                subfolder_metadata = {
                    'name': subfolder_name,
                    'mimeType': 'application/vnd.google-apps.folder',
                    'parents': [folder_id]
                }
                
                self.service.files().create(body=subfolder_metadata).execute()
                logger.info(f"サブフォルダ作成: {subfolder_name}")
            
            return folder_id
            
        except Exception as e:
            logger.error(f"フォルダ作成エラー: {e}")
            return None
    
    def upload_file(self, file_content: bytes, file_name: str, parent_folder_id: str, 
                   mime_type: str = 'application/octet-stream') -> Optional[str]:
        """ファイルアップロード"""
        if not self.service:
            return None
        
        try:
            file_metadata = {
                'name': file_name,
                'parents': [parent_folder_id]
            }
            
            media = MediaIoBaseUpload(
                io.BytesIO(file_content),
                mimetype=mime_type,
                resumable=True
            )
            
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,name,webViewLink'
            ).execute()
            
            logger.info(f"ファイルアップロード成功: {file_name}")
            return file.get('id')
            
        except Exception as e:
            logger.error(f"ファイルアップロードエラー: {e}")
            return None
    
    def upload_csv_files(self, folder_id: str, csv_data: Dict[str, bytes]) -> Dict[str, str]:
        """CSV ファイル群アップロード"""
        upload_results = {}
        
        for filename, content in csv_data.items():
            file_id = self.upload_file(
                content, 
                filename, 
                folder_id, 
                'text/csv'
            )
            
            if file_id:
                upload_results[filename] = file_id
        
        return upload_results
    
    def upload_image(self, image_data: bytes, image_name: str, parent_folder_id: str) -> Optional[str]:
        """画像アップロード（リネーム・最適化対応）"""
        try:
            # 画像形式判定とMIMEタイプ設定
            if image_name.lower().endswith(('.jpg', '.jpeg')):
                mime_type = 'image/jpeg'
            elif image_name.lower().endswith('.png'):
                mime_type = 'image/png'
            elif image_name.lower().endswith('.webp'):
                mime_type = 'image/webp'
            else:
                mime_type = 'image/jpeg'  # デフォルト
            
            # タイムスタンプ付きファイル名生成
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_name = os.path.splitext(image_name)[0]
            extension = os.path.splitext(image_name)[1] or '.jpg'
            
            renamed_image = f"{base_name}_{timestamp}{extension}"
            
            return self.upload_file(
                image_data,
                renamed_image,
                parent_folder_id,
                mime_type
            )
            
        except Exception as e:
            logger.error(f"画像アップロードエラー: {e}")
            return None
    
    def get_folder_link(self, folder_id: str) -> Optional[str]:
        """フォルダ共有リンク取得"""
        if not self.service:
            return None
        
        try:
            # フォルダを共有可能に設定
            permission = {
                'type': 'anyone',
                'role': 'viewer'
            }
            
            self.service.permissions().create(
                fileId=folder_id,
                body=permission
            ).execute()
            
            # フォルダ情報取得
            folder = self.service.files().get(
                fileId=folder_id,
                fields='webViewLink'
            ).execute()
            
            return folder.get('webViewLink')
            
        except Exception as e:
            logger.error(f"フォルダリンク取得エラー: {e}")
            return None
    
    def create_complete_package(self, store_name: str, all_data: Dict) -> Optional[Dict[str, str]]:
        """完全パッケージ作成"""
        try:
            # メインフォルダ作成
            folder_id = self.create_store_folder(store_name)
            if not folder_id:
                return None
            
            # サブフォルダID取得
            subfolders = self._get_subfolders(folder_id)
            
            package_info = {
                'main_folder_id': folder_id,
                'main_folder_link': self.get_folder_link(folder_id),
                'uploaded_files': {}
            }
            
            # 1. 店舗基本情報アップロード
            if 'store_info_csv' in all_data:
                file_id = self.upload_file(
                    all_data['store_info_csv'],
                    f"{store_name}_店舗基本情報.csv",
                    subfolders.get('01_店舗基本情報', folder_id),
                    'text/csv'
                )
                package_info['uploaded_files']['store_info'] = file_id
            
            # 2. 店主ストーリーファイル
            if 'story_csv' in all_data:
                file_id = self.upload_file(
                    all_data['story_csv'],
                    f"{store_name}_14言語ストーリー.csv",
                    subfolders.get('02_店主ストーリー', folder_id),
                    'text/csv'
                )
                package_info['uploaded_files']['story'] = file_id
            
            # 3. メニューCSV・画像
            if 'menu_csv' in all_data:
                file_id = self.upload_file(
                    all_data['menu_csv'],
                    f"{store_name}_14言語メニュー.csv",
                    subfolders.get('03_メニュー情報', folder_id),
                    'text/csv'
                )
                package_info['uploaded_files']['menu'] = file_id
            
            # 4. AI食レポCSV
            if 'food_report_csv' in all_data:
                file_id = self.upload_file(
                    all_data['food_report_csv'],
                    f"{store_name}_14言語AI食レポ.csv",
                    subfolders.get('04_AI食レポ', folder_id),
                    'text/csv'
                )
                package_info['uploaded_files']['food_report'] = file_id
            
            # 5. 画像ファイル群
            if 'images' in all_data:
                for image_name, image_data in all_data['images'].items():
                    file_id = self.upload_image(
                        image_data,
                        image_name,
                        subfolders.get('03_メニュー情報', folder_id)
                    )
                    package_info['uploaded_files'][f'image_{image_name}'] = file_id
            
            logger.info(f"完全パッケージ作成完了: {store_name}")
            return package_info
            
        except Exception as e:
            logger.error(f"完全パッケージ作成エラー: {e}")
            return None
    
    def _get_subfolders(self, parent_folder_id: str) -> Dict[str, str]:
        """サブフォルダID取得"""
        if not self.service:
            return {}
        
        try:
            query = f"parents='{parent_folder_id}' and mimeType='application/vnd.google-apps.folder'"
            results = self.service.files().list(
                q=query,
                fields="files(id,name)"
            ).execute()
            
            subfolders = {}
            for folder in results.get('files', []):
                subfolders[folder['name']] = folder['id']
            
            return subfolders
            
        except Exception as e:
            logger.error(f"サブフォルダ取得エラー: {e}")
            return {}

# シングルトンインスタンス
_google_drive_instance = None

def get_google_drive_integration() -> GoogleDriveIntegration:
    """Google Drive連携インスタンス取得"""
    global _google_drive_instance
    if _google_drive_instance is None:
        _google_drive_instance = GoogleDriveIntegration()
    return _google_drive_instance

def render_google_auth_section():
    """Google認証セクション表示"""
    drive = get_google_drive_integration()
    
    if not drive.is_configured():
        st.warning("⚠️ Google Drive連携が設定されていません")
        st.info("""
        Google Drive連携を有効にするには、以下の設定が必要です：
        1. Google Cloud Consoleでプロジェクト作成
        2. Drive API有効化
        3. OAuth 2.0クライアントID作成
        4. secrets.tomlに認証情報設定
        """)
        return False
    
    if drive.authenticate():
        st.success("✅ Google Drive連携済み")
        return True
    else:
        st.warning("🔑 Google Drive認証が必要です")
        
        auth_url = drive.get_auth_url()
        if auth_url:
            st.markdown(f"[🔐 Google認証ページを開く]({auth_url})")
            
            auth_code = st.text_input(
                "認証コードを貼り付け:",
                placeholder="4/...",
                key="google_auth_code"
            )
            
            if auth_code and st.button("認証完了"):
                if drive.complete_auth(auth_code):
                    st.success("✅ Google Drive認証完了！")
                    st.rerun()
                else:
                    st.error("❌ 認証に失敗しました")
        
        return False

def create_package_and_upload(store_name: str, all_system_data: Dict) -> Optional[Dict]:
    """パッケージ作成・アップロード統合処理"""
    drive = get_google_drive_integration()
    
    if not drive.authenticate():
        st.error("Google Drive認証が必要です")
        return None
    
    with st.spinner("📁 Google Driveに完全パッケージを作成中..."):
        result = drive.create_complete_package(store_name, all_system_data)
        
        if result:
            st.success("✅ Google Driveパッケージ作成完了！")
            return result
        else:
            st.error("❌ パッケージ作成に失敗しました")
            return None