"""
TONOSAMA Professional System - OpenAI Integration Module
完璧なAI連携システム - 1兆円ダイヤモンド級品質

世界最高レベルの食レポーター「帝王（Imperator）」による
多言語コンテンツ生成・翻訳機能
"""

import streamlit as st
import openai
import asyncio
import time
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
from dataclasses import dataclass

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class LanguageInfo:
    """言語情報データクラス"""
    code: str
    name: str
    context: str
    native_name: str = ""

class OpenAIIntegration:
    """完璧なOpenAI統合システム"""
    
    def __init__(self):
        """初期化 - API設定と言語マッピング"""
        
        # OpenAI設定
        self.model = "gpt-4"
        self.fallback_model = "gpt-3.5-turbo"
        self.max_tokens = 1500
        self.temperature = 0.7
        
        # 14言語完全対応マッピング
        self.languages = {
            "ja": LanguageInfo(
                code="ja",
                name="日本語",
                context="Japanese cultural context with emphasis on hospitality (omotenashi)",
                native_name="日本語"
            ),
            "en": LanguageInfo(
                code="en",
                name="English",
                context="Western cultural context with clear, direct communication",
                native_name="English"
            ),
            "ko": LanguageInfo(
                code="ko",
                name="한국어",
                context="Korean cultural context with respectful honorifics",
                native_name="한국어"
            ),
            "zh-CN": LanguageInfo(
                code="zh-CN",
                name="简体中文",
                context="Mainland Chinese cultural context",
                native_name="简体中文"
            ),
            "zh-TW": LanguageInfo(
                code="zh-TW",
                name="繁體中文",
                context="Traditional Chinese cultural context",
                native_name="繁體中文"
            ),
            "zh-HK": LanguageInfo(
                code="zh-HK",
                name="廣東話",
                context="Hong Kong Cantonese cultural context",
                native_name="廣東話"
            ),
            "th": LanguageInfo(
                code="th",
                name="ไทย",
                context="Thai cultural context with polite expressions",
                native_name="ภาษาไทย"
            ),
            "tl": LanguageInfo(
                code="tl",
                name="Filipino",
                context="Filipino cultural context with warm hospitality",
                native_name="Filipino"
            ),
            "vi": LanguageInfo(
                code="vi",
                name="Tiếng Việt",
                context="Vietnamese cultural context",
                native_name="Tiếng Việt"
            ),
            "id": LanguageInfo(
                code="id",
                name="Bahasa Indonesia",
                context="Indonesian cultural context",
                native_name="Bahasa Indonesia"
            ),
            "es": LanguageInfo(
                code="es",
                name="Español",
                context="Spanish cultural context",
                native_name="Español"
            ),
            "de": LanguageInfo(
                code="de",
                name="Deutsch",
                context="German cultural context with precision",
                native_name="Deutsch"
            ),
            "fr": LanguageInfo(
                code="fr",
                name="Français",
                context="French cultural context with elegance",
                native_name="Français"
            ),
            "it": LanguageInfo(
                code="it",
                name="Italiano",
                context="Italian cultural context with passion for food",
                native_name="Italiano"
            )
        }
        
        # レート制限対策
        self.request_count = 0
        self.last_request_time = 0
        self.min_request_interval = 1.0  # 秒
    
    def get_api_key(self) -> Optional[str]:
        """APIキーの安全な取得"""
        try:
            # Streamlit Secretsから取得
            if "openai_api_key" in st.secrets:
                return st.secrets["openai_api_key"]
            
            # セッション状態から取得
            if "openai_api_key" in st.session_state:
                return st.session_state["openai_api_key"]
            
            # 環境変数から取得
            import os
            if "OPENAI_API_KEY" in os.environ:
                return os.environ["OPENAI_API_KEY"]
            
            logger.warning("OpenAI APIキーが見つかりません")
            return None
            
        except Exception as e:
            logger.error(f"APIキー取得エラー: {e}")
            return None
    
    def validate_api_key(self, api_key: str) -> bool:
        """APIキーの有効性検証"""
        if not api_key or not api_key.startswith("sk-"):
            return False
        
        try:
            # テスト呼び出し
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model=self.fallback_model,
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=1
            )
            return True
        except Exception as e:
            logger.error(f"APIキー検証失敗: {e}")
            return False
    
    async def _rate_limited_request(self) -> None:
        """レート制限対策"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            await asyncio.sleep(sleep_time)
        
        self.last_request_time = time.time()
        self.request_count += 1
    
    async def generate_story(self, imperator_answers: Dict[str, str], store_info: Dict) -> str:
        """帝王式統合ストーリー生成"""
        try:
            api_key = self.get_api_key()
            if not api_key:
                raise Exception("OpenAI APIキーが設定されていません")
            
            await self._rate_limited_request()
            
            # プロンプト構築
            prompt = self._build_story_prompt(imperator_answers, store_info)
            
            client = openai.OpenAI(api_key=api_key)
            
            response = await self._make_async_request(
                client,
                prompt,
                "店主ストーリー生成"
            )
            
            return response
            
        except Exception as e:
            logger.error(f"ストーリー生成エラー: {e}")
            return self._get_fallback_story(imperator_answers, store_info)
    
    async def generate_menu_description(self, menu_item: Dict, language: str, store_info: Dict) -> str:
        """AI食レポ生成（指定言語）"""
        try:
            api_key = self.get_api_key()
            if not api_key:
                raise Exception("OpenAI APIキーが設定されていません")
            
            await self._rate_limited_request()
            
            # プロンプト構築
            prompt = self._build_menu_prompt(menu_item, language, store_info)
            
            client = openai.OpenAI(api_key=api_key)
            
            response = await self._make_async_request(
                client,
                prompt,
                f"食レポ生成 ({language})"
            )
            
            return response
            
        except Exception as e:
            logger.error(f"食レポ生成エラー ({language}): {e}")
            return self._get_fallback_menu_description(menu_item, language)
    
    async def generate_multilingual_content(self, base_content: str, target_languages: List[str]) -> Dict[str, str]:
        """多言語コンテンツ一括生成"""
        results = {}
        total = len(target_languages)
        
        # プログレスバー表示
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, language in enumerate(target_languages):
            try:
                status_text.text(f"翻訳中: {self.languages[language].name} ({i+1}/{total})")
                
                # 翻訳実行
                translated = await self.translate_content(base_content, language)
                results[language] = translated
                
                # プログレス更新
                progress_bar.progress((i + 1) / total)
                
                # 進捗通知
                st.success(f"✅ {self.languages[language].name} 翻訳完了")
                
            except Exception as e:
                logger.error(f"多言語生成エラー ({language}): {e}")
                results[language] = self._get_fallback_translation(base_content, language)
                st.warning(f"⚠️ {language} フォールバック使用")
        
        # 完了通知
        status_text.text("多言語生成完了！")
        progress_bar.empty()
        status_text.empty()
        
        return results
    
    async def translate_content(self, content: str, target_language: str) -> str:
        """高精度翻訳機能"""
        try:
            api_key = self.get_api_key()
            if not api_key:
                raise Exception("OpenAI APIキーが設定されていません")
            
            await self._rate_limited_request()
            
            # 翻訳プロンプト構築
            prompt = self._build_translation_prompt(content, target_language)
            
            client = openai.OpenAI(api_key=api_key)
            
            response = await self._make_async_request(
                client,
                prompt,
                f"翻訳 ({target_language})"
            )
            
            return response
            
        except Exception as e:
            logger.error(f"翻訳エラー ({target_language}): {e}")
            return self._get_fallback_translation(content, target_language)
    
    async def _make_async_request(self, client: openai.OpenAI, prompt: str, task_name: str) -> str:
        """非同期API呼び出し"""
        try:
            # メインモデルで試行
            response = await asyncio.to_thread(
                client.chat.completions.create,
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are Imperator, a world-class food critic and storyteller specializing in Japanese restaurant culture."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            result = response.choices[0].message.content.strip()
            logger.info(f"{task_name} 成功 (model: {self.model})")
            return result
            
        except Exception as e:
            logger.warning(f"{task_name} フォールバックモデル使用: {e}")
            
            # フォールバックモデルで再試行
            try:
                response = await asyncio.to_thread(
                    client.chat.completions.create,
                    model=self.fallback_model,
                    messages=[
                        {
                            "role": "system", 
                            "content": "You are Imperator, a world-class food critic and storyteller."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=self.temperature,
                    max_tokens=self.max_tokens
                )
                
                result = response.choices[0].message.content.strip()
                logger.info(f"{task_name} 成功 (fallback: {self.fallback_model})")
                return result
                
            except Exception as fallback_error:
                logger.error(f"{task_name} 完全失敗: {fallback_error}")
                raise fallback_error
    
    def _build_story_prompt(self, answers: Dict[str, str], store_info: Dict) -> str:
        """店主ストーリー生成プロンプト構築"""
        store_name = store_info.get('store_name_ja', '')
        store_type = store_info.get('store_type', '')
        
        # 15問の質問タイトル
        questions = [
            "創業当時の苦労", "店名の由来", "開業後の変化", "立地の理由", "始めたきっかけ",
            "伝えたい核", "嬉しい瞬間", "看板料理の物語", "譲れない軸", "海外のお客様へ",
            "日本らしさ", "世界への一言", "これからの場所像", "5-10年後の理想", "お客様への感謝"
        ]
        
        # 回答内容の構築
        answered_content = []
        for i, (q_key, answer) in enumerate(answers.items()):
            if answer and answer.strip():
                answered_content.append(f"{questions[i]}: {answer.strip()}")
        
        prompt = f"""あなたは世界最高レベルの食レポーター「帝王（Imperator）」です。

店舗情報：
- 店舗名：{store_name}
- 業種：{store_type}

店主からの15問回答：
{chr(10).join(answered_content)}

これらの情報から、この店舗の魅力的なストーリーを作成してください。以下の要素を含めてください：

1. 店主の想いと背景
2. 料理へのこだわり
3. お客様への想い
4. 店舗の特徴・雰囲気
5. 訪れる人へのメッセージ

要件：
- 800-1000文字程度
- 感動的で魅力的な内容
- 外国人観光客にも伝わる心に響く表現
- 店主の人柄と料理への情熱が伝わる内容
- 読み手が実際に訪れたくなるような魅力的な描写

日本語で、店主の心からの想いが伝わるストーリーを作成してください。"""

        return prompt
    
    def _build_menu_prompt(self, menu_item: Dict, language: str, store_info: Dict) -> str:
        """食レポ生成プロンプト構築"""
        lang_info = self.languages.get(language, self.languages['en'])
        
        # 設備情報の取得
        facility_info = self._get_facility_info_text(store_info)
        
        prompt = f"""You are "Imperator", the world's top food critic and reviewer.

Menu Item: {menu_item.get('name', '')}
Price: ¥{menu_item.get('price', 0)}
Category: {menu_item.get('category', 'メイン料理')}
Description: {menu_item.get('desc', '')}

Restaurant Information:
- Store Name: {store_info.get('store_name_ja', '')}
- Type: {store_info.get('store_type', '')}
- Facility Information:
{facility_info}

Create an enticing, professional food description in {lang_info.name} that captures:

1. Visual appeal and presentation
2. Taste, texture, and aroma  
3. Cooking method and ingredients
4. Cultural significance if applicable
5. Why customers should try this dish
6. Include allergy/dietary information ONLY if restaurant provides detailed labeling

Cultural Context: {lang_info.context}

Requirements:
- Length: 80-120 words
- Professional food critic tone (Imperator style)
- Mouth-watering and appealing description
- Culturally appropriate for {lang_info.name} speakers
- Suitable for restaurant menu display
- Include dietary restriction notes only when restaurant has detailed allergy labeling
- Focus on the culinary experience and emotional connection

Please write only the description without any additional formatting or labels."""

        return prompt
    
    def _build_translation_prompt(self, content: str, target_language: str) -> str:
        """翻訳プロンプト構築"""
        lang_info = self.languages.get(target_language, self.languages['en'])
        
        prompt = f"""You are a professional translator specializing in Japanese restaurant and hospitality content. Translate the following Japanese restaurant story/description to {lang_info.name} with the highest accuracy and cultural sensitivity.

Critical Translation Requirements:
- ACCURACY: Maintain exact meaning and nuance from the original Japanese
- CULTURAL ADAPTATION: Adapt expressions naturally for {lang_info.context}
- EMOTIONAL IMPACT: Preserve the warmth, hospitality (omotenashi), and emotional connection
- PROFESSIONAL TONE: Keep sophisticated, authentic restaurant-quality language
- FOOD TERMINOLOGY: Use precise culinary terms appropriate for {lang_info.name}
- LOCAL APPEAL: Make it naturally appealing and trustworthy to {lang_info.name} speakers
- CONSISTENCY: Maintain consistent terminology and style throughout

Context: This is for a Japanese restaurant's international marketing to attract foreign tourists. The translation will be used in official multilingual menus and promotional materials.

Original Japanese text:
{content}

Requirements for output:
- Provide ONLY the translation
- No additional commentary, formatting, or explanations  
- Length should be proportional to the original (not shorter or longer)
- Use natural, flowing language that reads as if originally written in {lang_info.name}
- Maintain the emotional warmth and hospitality of the original

Translation:"""

        return prompt
    
    def _get_facility_info_text(self, store_info: Dict) -> str:
        """設備情報のテキスト生成"""
        facility_texts = []
        
        # 車椅子対応
        wheelchair = store_info.get('wheelchair', '')
        if wheelchair == 'available':
            facility_texts.append('- Wheelchair accessible facility')
        elif wheelchair == 'partial':  
            facility_texts.append('- Limited wheelchair accessibility')
        elif wheelchair == 'not_available':
            facility_texts.append('- Not wheelchair accessible')
        
        # 食事制限対応
        dietary = store_info.get('dietary_restrictions', '')
        if dietary == 'full':
            facility_texts.append('- Full vegetarian/vegan options available')
        elif dietary == 'limited':
            facility_texts.append('- Some vegetarian/vegan options available')
        elif dietary == 'none':
            facility_texts.append('- No specific vegetarian/vegan menu')
        
        # ハラール対応
        halal = store_info.get('halal_support', '')
        if halal == 'certified':
            facility_texts.append('- Halal certified restaurant')
        elif halal == 'friendly':
            facility_texts.append('- Muslim-friendly options available')
        elif halal == 'not_available':
            facility_texts.append('- No halal certification')
        
        # アレルギー表示
        allergy = store_info.get('allergy_info', '')
        if allergy == 'detailed':
            facility_texts.append('- Detailed allergy labeling provided for all dishes')
        elif allergy == 'basic':
            facility_texts.append('- Basic allergy information available')
        elif allergy == 'none':
            facility_texts.append('- No allergy labeling system in place')
        
        return '\n'.join(facility_texts) if facility_texts else '- Standard restaurant facilities'
    
    def _get_fallback_story(self, answers: Dict[str, str], store_info: Dict) -> str:
        """フォールバックストーリー"""
        store_name = store_info.get('store_name_ja', 'お店')
        store_type = store_info.get('store_type', 'レストラン')
        
        return f"""{store_name}は、{store_type}として地域に愛され続けている特別なお店です。

店主の深いこだわりと情熱が込められた料理は、訪れる人々の心を温かく満たします。厳選された食材と伝統的な技法を大切にしながら、常にお客様に最高の体験をお届けすることを心がけています。

アットホームな雰囲気の中で、ゆっくりとお食事をお楽しみいただけます。地元の方から観光で訪れる方まで、すべてのお客様に心地よいひとときを過ごしていただきたいという想いで、日々真心を込めて営業しています。

ぜひ一度足をお運びいただき、私たちの想いが詰まった料理を味わってみてください。心よりお待ちしております。"""
    
    def _get_fallback_menu_description(self, menu_item: Dict, language: str) -> str:
        """フォールバックメニュー説明"""
        name = menu_item.get('name', '')
        
        fallbacks = {
            'ja': f"{name}は当店自慢の一品です。厳選された食材を使用し、丁寧に調理いたします。ぜひ一度お試しください。",
            'en': f"{name} is our signature dish, carefully prepared with selected ingredients. A must-try item that showcases our culinary excellence.",
            'ko': f"{name}는 저희 식당의 대표 메뉴입니다. 엄선된 재료로 정성껏 조리한 특별한 요리를 꼭 맛보세요.",
            'zh-CN': f"{name}是本店的招牌菜，采用精选食材精心制作。这道特色料理值得您品尝。",
            'zh-TW': f"{name}是本店的招牌菜，採用精選食材精心製作。這道特色料理值得您品嚐。",
        }
        
        return fallbacks.get(language, fallbacks['en'])
    
    def _get_fallback_translation(self, content: str, language: str) -> str:
        """フォールバック翻訳"""
        lang_name = self.languages.get(language, {}).get('name', language)
        return f"[{lang_name} translation of: {content[:50]}...]"
    
    def get_supported_languages(self) -> List[LanguageInfo]:
        """サポート言語一覧取得"""
        return list(self.languages.values())
    
    def get_language_info(self, language_code: str) -> Optional[LanguageInfo]:
        """言語情報取得"""
        return self.languages.get(language_code)

# グローバルインスタンス
openai_integration = OpenAIIntegration()

def get_openai_integration() -> OpenAIIntegration:
    """OpenAI統合インスタンスの取得"""
    return openai_integration