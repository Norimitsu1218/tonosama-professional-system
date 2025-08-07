"""
TONOSAMA Professional System - CSV Generator Module
完璧なCSV生成システム - 1兆円ダイヤモンド級品質

正太さん形式対応・14言語横型CSV・完全自動化
"""

import streamlit as st
import pandas as pd
import io
import csv
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging
from dataclasses import asdict

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CSVGenerator:
    """完璧なCSV生成システム"""
    
    def __init__(self):
        """初期化"""
        self.encoding = 'utf-8-sig'  # BOM付きUTF-8（Excel対応）
        self.delimiter = ','
        self.newline = '\n'
        
        # 14言語定義（正太さん形式）
        self.languages = [
            {'code': 'ja', 'name': '日本語'},
            {'code': 'en', 'name': '英語'},
            {'code': 'ko', 'name': '韓国語'},
            {'code': 'zh-CN', 'name': '中国語'},
            {'code': 'zh-TW', 'name': '台湾語'},
            {'code': 'zh-HK', 'name': '広東語'},
            {'code': 'th', 'name': 'タイ語'},
            {'code': 'tl', 'name': 'フィリピン語'},
            {'code': 'vi', 'name': 'ベトナム語'},
            {'code': 'id', 'name': 'インドネシア語'},
            {'code': 'es', 'name': 'スペイン語'},
            {'code': 'de', 'name': 'ドイツ語'},
            {'code': 'fr', 'name': 'フランス語'},
            {'code': 'it', 'name': 'イタリア語'}
        ]
    
    def generate_store_info_csv(self, store_data: Dict) -> Dict[str, Any]:
        """店舗情報CSV生成（基本情報）"""
        try:
            # ヘッダー
            headers = ['項目', '内容', '備考']
            
            # データ行構築
            rows = [
                ['店舗名（日本語）', store_data.get('store_name_ja', ''), ''],
                ['店舗名（ローマ字）', store_data.get('store_name_romaji', ''), ''],
                ['業種', store_data.get('store_type', ''), ''],
                ['価格帯', store_data.get('price_band', ''), ''],
                ['住所', store_data.get('address', ''), ''],
                ['電話番号', store_data.get('tel', ''), ''],
                ['ウェブサイト', store_data.get('website', ''), ''],
                ['Instagram', store_data.get('instagram', ''), ''],
                ['Facebook', store_data.get('facebook', ''), ''],
                ['メールアドレス', store_data.get('email', ''), ''],
                ['最寄り駅', store_data.get('nearest_station', ''), ''],
                ['徒歩時間', store_data.get('walk_time', ''), '分'],
                ['営業時間', store_data.get('open_hours', ''), ''],
                ['定休日', store_data.get('closed_days', ''), '']
            ]
            
            # 設備情報追加
            facility_info = self._get_facility_info_rows(store_data)
            rows.extend(facility_info)
            
            # CSV生成
            csv_content = self._create_csv_content([headers] + rows)
            filename = f"{store_data.get('store_name_ja', 'レストラン')}_店舗情報.csv"
            
            logger.info(f"店舗情報CSV生成完了: {filename}")
            
            return {
                'success': True,
                'content': csv_content,
                'filename': filename,
                'rows': len(rows)
            }
            
        except Exception as e:
            logger.error(f"店舗情報CSV生成エラー: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def generate_story_multilingual_csv(self, story_text: str, store_name: str, translated_content: Dict[str, str] = None) -> Dict[str, Any]:
        """店主ストーリー14言語CSV生成（正太さん形式：横型）"""
        try:
            if not story_text:
                return {
                    'success': False,
                    'error': 'ストーリーテキストが設定されていません'
                }
            
            # ヘッダー作成（横型：言語が列）
            headers = ['店舗名'] + [lang['name'] + 'ストーリー' for lang in self.languages]
            
            # データ行作成（1行に全言語のストーリー）
            row_data = [store_name]
            
            for lang in self.languages:
                if lang['code'] == 'ja':
                    # 日本語はオリジナル
                    row_data.append(story_text)
                elif translated_content and lang['code'] in translated_content:
                    # 翻訳済みコンテンツを使用
                    row_data.append(translated_content[lang['code']])
                else:
                    # フォールバック翻訳
                    fallback = self._get_fallback_story_translation(story_text, lang['code'], store_name)
                    row_data.append(fallback)
            
            # CSV生成
            csv_content = self._create_csv_content([headers, row_data])
            filename = f"{store_name}_店主ストーリー_14言語.csv"
            
            logger.info(f"店主ストーリー14言語CSV生成完了: {filename}")
            
            return {
                'success': True,
                'content': csv_content,
                'filename': filename,
                'languages_count': len(self.languages)
            }
            
        except Exception as e:
            logger.error(f"店主ストーリー14言語CSV生成エラー: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def generate_multilingual_food_report_csv(self, menu_data: List[Dict], generated_data: Dict[str, Dict[str, str]], store_name: str) -> Dict[str, Any]:
        """14言語食レポCSV生成（正太さん形式：横型）"""
        try:
            # ヘッダー作成
            headers = [
                'メニューID',
                '料理名',
                '価格',
                'カテゴリー'
            ]
            
            # 各言語の説明文列を追加
            for lang in self.languages:
                headers.append(f"説明文_{lang['name']}")
            
            rows = []
            
            # メニューデータ処理
            for i, item in enumerate(menu_data):
                row = [
                    item.get('id', f'menu_{i+1}'),
                    item.get('name', ''),
                    item.get('price', ''),
                    item.get('category', 'メイン料理')
                ]
                
                # 各言語の説明文を追加
                for lang in self.languages:
                    item_id = item.get('id', f'menu_{i+1}')
                    if (item_id in generated_data and 
                        lang['code'] in generated_data[item_id]):
                        # AI生成済みコンテンツ使用
                        description = generated_data[item_id][lang['code']]
                    else:
                        # フォールバック使用
                        description = self._get_fallback_menu_description(item, lang['code'])
                    
                    row.append(description)
                
                rows.append(row)
            
            # CSV生成
            csv_content = self._create_csv_content([headers] + rows)
            filename = f"{store_name}_食レポ_14言語.csv"
            
            logger.info(f"14言語食レポCSV生成完了: {filename}")
            
            return {
                'success': True,
                'content': csv_content,
                'filename': filename,
                'menu_count': len(menu_data),
                'languages_count': len(self.languages)
            }
            
        except Exception as e:
            logger.error(f"14言語食レポCSV生成エラー: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def generate_package_summary_csv(self, package_data: Dict) -> Dict[str, Any]:
        """パッケージサマリーCSV生成"""
        try:
            headers = ['項目', '内容', '詳細']
            
            rows = [
                ['生成日時', datetime.now().strftime('%Y年%m月%d日 %H:%M:%S'), ''],
                ['店舗名', package_data.get('store_name', ''), ''],
                ['プラン', package_data.get('plan', ''), ''],
                ['セッションID', package_data.get('session_id', ''), ''],
                ['', '', ''],  # 区切り行
                ['生成ファイル一覧', '', ''],
                ['店舗情報CSV', 'あり' if package_data.get('store_csv_success') else 'なし', ''],
                ['店主ストーリー14言語CSV', 'あり' if package_data.get('story_csv_success') else 'なし', ''],
                ['食レポ14言語CSV', 'あり' if package_data.get('menu_csv_success') else 'なし', ''],
                ['店舗代表画像', 'あり' if package_data.get('store_image_success') else 'なし', ''],
                ['メニュー画像', f"{package_data.get('image_success_count', 0)}件", f"全{package_data.get('image_total_count', 0)}件中"]
            ]
            
            csv_content = self._create_csv_content([headers] + rows)
            filename = f"{package_data.get('store_name', 'TONOSAMA')}_パッケージサマリー.csv"
            
            return {
                'success': True,
                'content': csv_content,
                'filename': filename
            }
            
        except Exception as e:
            logger.error(f"パッケージサマリーCSV生成エラー: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _get_facility_info_rows(self, store_data: Dict) -> List[List[str]]:
        """設備情報行の生成"""
        rows = []
        
        # 車椅子対応
        wheelchair = store_data.get('wheelchair', '')
        if wheelchair == 'available':
            rows.append(['車椅子対応', '対応可能', ''])
        elif wheelchair == 'partial':
            rows.append(['車椅子対応', '一部対応', ''])
        elif wheelchair == 'not_available':
            rows.append(['車椅子対応', '対応不可', ''])
        
        # 食事制限対応
        dietary = store_data.get('dietary_restrictions', '')
        if dietary == 'full':
            rows.append(['ベジタリアン対応', 'フル対応', ''])
        elif dietary == 'limited':
            rows.append(['ベジタリアン対応', '一部対応', ''])
        elif dietary == 'none':
            rows.append(['ベジタリアン対応', '対応なし', ''])
        
        # ハラール対応
        halal = store_data.get('halal_support', '')
        if halal == 'certified':
            rows.append(['ハラール対応', '認証済み', ''])
        elif halal == 'friendly':
            rows.append(['ハラール対応', 'フレンドリー', ''])
        elif halal == 'not_available':
            rows.append(['ハラール対応', '対応なし', ''])
        
        # アレルギー表示
        allergy = store_data.get('allergy_info', '')
        if allergy == 'detailed':
            rows.append(['アレルギー表示', '詳細表示', ''])
        elif allergy == 'basic':
            rows.append(['アレルギー表示', '基本表示', ''])
        elif allergy == 'none':
            rows.append(['アレルギー表示', '表示なし', ''])
        
        return rows
    
    def _get_fallback_story_translation(self, original_story: str, language: str, store_name: str) -> str:
        """ストーリーフォールバック翻訳"""
        fallbacks = {
            'en': f"{store_name} is a beloved restaurant that continues to serve our community with passion and dedication. Our commitment to quality ingredients and traditional techniques ensures every guest enjoys an exceptional dining experience. We welcome both local patrons and international visitors with warm hospitality and authentic flavors.",
            'ko': f"{store_name}은 정성과 헌신으로 지역사회에 사랑받는 식당입니다. 품질 좋은 재료와 전통 기법에 대한 우리의 철학으로 모든 손님이 특별한 식사 경험을 즐기실 수 있습니다.",
            'zh-CN': f"{store_name}是一家以热情和奉献精神持续为社区服务的受人喜爱的餐厅。我们对优质食材和传统技艺的坚持，确保每位客人都能享受到卓越的用餐体验。",
            'zh-TW': f"{store_name}是一家以熱情和奉獻精神持續為社區服務的受人喜愛的餐廳。我們對優質食材和傳統技藝的堅持，確保每位客人都能享受到卓越的用餐體驗。"
        }
        
        return fallbacks.get(language, fallbacks['en'])
    
    def _get_fallback_menu_description(self, menu_item: Dict, language: str) -> str:
        """メニューフォールバック説明"""
        name = menu_item.get('name', '')
        
        fallbacks = {
            'ja': f"{name}は当店自慢の一品です。厳選された食材を使用し、丁寧に調理いたします。",
            'en': f"{name} is our signature dish, carefully prepared with selected ingredients.",
            'ko': f"{name}는 저희 식당의 대표 메뉴입니다. 엄선된 재료로 정성껏 조리합니다.",
            'zh-CN': f"{name}是本店的招牌菜，采用精选食材精心制作。",
            'zh-TW': f"{name}是本店的招牌菜，採用精選食材精心製作。"
        }
        
        return fallbacks.get(language, fallbacks['en'])
    
    def _create_csv_content(self, data: List[List[str]]) -> str:
        """CSV形式文字列の作成"""
        output = io.StringIO()
        writer = csv.writer(output, delimiter=self.delimiter, quotechar='"', quoting=csv.QUOTE_ALL)
        
        for row in data:
            writer.writerow(row)
        
        content = output.getvalue()
        output.close()
        
        return content
    
    def create_downloadable_csv(self, content: str, filename: str) -> bytes:
        """ダウンロード可能なCSVファイル作成"""
        # BOM付きUTF-8エンコーディング
        return content.encode(self.encoding)
    
    def display_csv_preview(self, csv_content: str, title: str = "CSVプレビュー", max_rows: int = 10):
        """CSVプレビュー表示"""
        try:
            # CSV文字列をDataFrameに変換
            df = pd.read_csv(io.StringIO(csv_content))
            
            st.subheader(title)
            
            # 基本統計
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("行数", len(df))
            with col2:
                st.metric("列数", len(df.columns))
            with col3:
                st.metric("データサイズ", f"{len(csv_content)} 文字")
            
            # データ表示
            if len(df) > max_rows:
                st.write(f"最初の{max_rows}行を表示:")
                st.dataframe(df.head(max_rows))
                st.info(f"他に{len(df) - max_rows}行のデータがあります")
            else:
                st.dataframe(df)
                
        except Exception as e:
            st.error(f"CSVプレビューエラー: {e}")
            st.text("生のCSVデータ:")
            st.text(csv_content[:500] + "..." if len(csv_content) > 500 else csv_content)

# グローバルインスタンス
csv_generator = CSVGenerator()

def get_csv_generator() -> CSVGenerator:
    """CSV生成インスタンスの取得"""
    return csv_generator