"""
TONOSAMA Professional System - State Management Module
完璧な状態管理 - 1兆円ダイヤモンド級品質

全システム状態の集中管理、永続化、バリデーション
"""

import streamlit as st
import json
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
import logging
from dataclasses import dataclass, asdict
from pathlib import Path

# UI Styling Import（存在する場合のみ）
try:
    from modules.ui_styling import inject_diamond_css, render_tonosama_header, render_quality_badge, inject_custom_metrics_style
    UI_STYLING_AVAILABLE = True
except ImportError:
    UI_STYLING_AVAILABLE = False

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class StoreInfo:
    """店舗基本情報データクラス"""
    store_name_ja: str = ""
    store_name_romaji: str = ""
    store_type: str = ""
    price_band: str = ""
    address: str = ""
    tel: str = ""
    website: str = ""
    instagram: str = ""
    facebook: str = ""
    email: str = ""
    nearest_station: str = ""
    walk_time: str = ""
    access_detail: str = ""
    open_hours: str = ""
    closed_days: str = ""
    
    # 設備情報
    wheelchair: str = ""
    dietary_restrictions: str = ""
    halal_support: str = ""
    allergy_info: str = ""

@dataclass
class MenuItem:
    """メニューアイテムデータクラス"""
    id: str = ""
    name: str = ""
    price: int = 0
    category: str = ""
    desc: str = ""
    image_path: str = ""
    recommendation_score: int = 1  # 1-5スター

@dataclass
class SystemState:
    """システム全体状態データクラス"""
    # セッション管理
    session_id: str = ""
    created_at: str = ""
    last_updated: str = ""
    current_step: int = 1
    
    # 店舗情報
    store: StoreInfo = None
    
    # メニュー情報
    menu: List[MenuItem] = None
    menu_order: List[str] = None  # メニューID順序
    featured_menu_id: str = ""
    
    # 店主ストーリー
    imperator_answers: Dict[str, str] = None
    imperator_story: str = ""
    story_approved: bool = False
    story_approved_at: str = ""
    
    # AI生成コンテンツ
    generated_content: Dict[str, Dict[str, str]] = None
    
    # アップロードファイル
    store_representative_image: Any = None
    uploaded_menu_files: List[Any] = None
    
    # プラン選択
    selected_plan: str = ""
    plan_selected_at: str = ""
    
    # システム状態
    validation_errors: List[str] = None
    processing_status: Dict[str, str] = None

class StateManager:
    """完璧な状態管理システム"""
    
    def __init__(self):
        """初期化 - セッション状態の完璧な管理"""
        self.session_key = "tonosama_professional_state"
        self.backup_dir = Path("data/backups")
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # 初期化処理
        self._initialize_session_state()
        
    def _initialize_session_state(self):
        """セッション状態の初期化"""
        if self.session_key not in st.session_state:
            logger.info("新規セッション開始 - 初期状態作成")
            
            # 初期状態作成
            initial_state = SystemState(
                session_id=str(uuid.uuid4()),
                created_at=datetime.now(timezone.utc).isoformat(),
                last_updated=datetime.now(timezone.utc).isoformat(),
                store=StoreInfo(),
                menu=[],
                menu_order=[],
                imperator_answers={f"q{i}": "" for i in range(15)},
                generated_content={},
                uploaded_menu_files=[],
                validation_errors=[],
                processing_status={}
            )
            
            st.session_state[self.session_key] = initial_state
            self._auto_backup()
    
    def get_state(self) -> SystemState:
        """現在の状態を取得（セーフガード付き）"""
        try:
            # セッションキーが存在しない場合は初期化
            if self.session_key not in st.session_state:
                logger.warning(f"セッション状態キー'{self.session_key}'が存在しません - 初期化実行")
                self._initialize_session_state()
            
            return st.session_state[self.session_key]
            
        except Exception as e:
            logger.error(f"状態取得エラー: {e}")
            # 緊急時の初期化
            self._initialize_session_state()
            return st.session_state[self.session_key]
    
    def update_state(self, **kwargs) -> None:
        """状態の更新"""
        try:
            current_state = self.get_state()
            
            # 更新処理
            for key, value in kwargs.items():
                if hasattr(current_state, key):
                    setattr(current_state, key, value)
                else:
                    logger.warning(f"未知の状態キー: {key}")
            
            # タイムスタンプ更新
            current_state.last_updated = datetime.now(timezone.utc).isoformat()
            
            # セッション状態に反映
            st.session_state[self.session_key] = current_state
            
            # 自動バックアップ
            self._auto_backup()
            
            logger.info(f"状態更新完了: {list(kwargs.keys())}")
            
        except Exception as e:
            logger.error(f"状態更新エラー: {e}")
            self._handle_state_error(e)
    
    def update_store_info(self, **store_data) -> None:
        """店舗情報の更新"""
        current_state = self.get_state()
        store = current_state.store
        
        for key, value in store_data.items():
            if hasattr(store, key):
                setattr(store, key, value)
        
        self.update_state(store=store)
    
    def add_menu_item(self, menu_item: MenuItem) -> None:
        """メニューアイテムの追加"""
        current_state = self.get_state()
        
        # IDが未設定の場合は自動生成
        if not menu_item.id:
            menu_item.id = f"menu_{len(current_state.menu) + 1}_{uuid.uuid4().hex[:8]}"
        
        # メニューリストに追加
        current_state.menu.append(menu_item)
        current_state.menu_order.append(menu_item.id)
        
        self.update_state(menu=current_state.menu, menu_order=current_state.menu_order)
        
        logger.info(f"メニューアイテム追加: {menu_item.name} (ID: {menu_item.id})")
    
    def update_menu_item(self, item_id: str, **item_data) -> None:
        """メニューアイテムの更新"""
        current_state = self.get_state()
        
        for item in current_state.menu:
            if item.id == item_id:
                for key, value in item_data.items():
                    if hasattr(item, key):
                        setattr(item, key, value)
                break
        
        self.update_state(menu=current_state.menu)
    
    def delete_menu_item(self, item_id: str) -> None:
        """メニューアイテムの削除"""
        current_state = self.get_state()
        
        # メニューリストから削除
        current_state.menu = [item for item in current_state.menu if item.id != item_id]
        current_state.menu_order = [oid for oid in current_state.menu_order if oid != item_id]
        
        # 生成コンテンツからも削除
        if item_id in current_state.generated_content:
            del current_state.generated_content[item_id]
        
        # イチオシメニューが削除された場合
        if current_state.featured_menu_id == item_id:
            current_state.featured_menu_id = ""
        
        self.update_state(
            menu=current_state.menu,
            menu_order=current_state.menu_order,
            generated_content=current_state.generated_content,
            featured_menu_id=current_state.featured_menu_id
        )
        
        logger.info(f"メニューアイテム削除: {item_id}")
    
    def reorder_menu(self, new_order: List[str]) -> None:
        """メニュー順序の変更"""
        self.update_state(menu_order=new_order)
    
    def update_imperator_answer(self, question_id: str, answer: str) -> None:
        """帝王質問回答の更新"""
        current_state = self.get_state()
        current_state.imperator_answers[question_id] = answer
        self.update_state(imperator_answers=current_state.imperator_answers)
    
    def set_story_approved(self, story: str) -> None:
        """店主ストーリー承認"""
        self.update_state(
            imperator_story=story,
            story_approved=True,
            story_approved_at=datetime.now(timezone.utc).isoformat()
        )
    
    def add_generated_content(self, menu_id: str, language: str, content: str) -> None:
        """AI生成コンテンツの追加"""
        current_state = self.get_state()
        
        if menu_id not in current_state.generated_content:
            current_state.generated_content[menu_id] = {}
        
        current_state.generated_content[menu_id][language] = content
        self.update_state(generated_content=current_state.generated_content)
    
    def validate_state(self) -> List[str]:
        """状態の完全バリデーション"""
        errors = []
        current_state = self.get_state()
        
        # Step 1: 店舗情報バリデーション
        if not current_state.store.store_name_ja:
            errors.append("店舗名（日本語）が入力されていません")
        
        if not current_state.store.store_type:
            errors.append("業種が選択されていません")
        
        # Step 2: ストーリーバリデーション
        if not current_state.story_approved:
            errors.append("店主ストーリーが承認されていません")
        
        # Step 3: メニューバリデーション
        if not current_state.menu:
            errors.append("メニューが1つ以上必要です")
        
        for item in current_state.menu:
            if not item.name:
                errors.append(f"メニューアイテム {item.id} に料理名が設定されていません")
            if item.price <= 0:
                errors.append(f"メニューアイテム {item.name} の価格が設定されていません")
        
        # Step 6: プラン選択バリデーション
        if current_state.current_step >= 6:
            if not current_state.featured_menu_id:
                errors.append("イチオシメニューが選択されていません")
        
        # 状態に反映
        current_state.validation_errors = errors
        self.update_state(validation_errors=errors)
        
        return errors
    
    def can_proceed_to_step(self, target_step: int) -> bool:
        """指定ステップに進めるかの判定"""
        errors = self.validate_state()
        current_state = self.get_state()
        
        # ステップ別必要条件チェック
        requirements = {
            1: [],  # 常に可能
            2: [lambda: current_state.store.store_name_ja],
            3: [lambda: current_state.story_approved],
            4: [lambda: len(current_state.menu) > 0],
            5: [lambda: len(current_state.menu) > 0],
            6: [lambda: len(current_state.menu) > 0]
        }
        
        if target_step in requirements:
            for requirement in requirements[target_step]:
                if not requirement():
                    return False
        
        return True
    
    def _auto_backup(self) -> None:
        """自動バックアップ"""
        try:
            current_state = self.get_state()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            backup_data = {
                "timestamp": timestamp,
                "session_id": current_state.session_id,
                "state": asdict(current_state)
            }
            
            backup_file = self.backup_dir / f"backup_{timestamp}.json"
            
            with open(backup_file, "w", encoding="utf-8") as f:
                json.dump(backup_data, f, ensure_ascii=False, indent=2)
            
            # 古いバックアップの削除（直近20件のみ保持）
            backup_files = sorted(self.backup_dir.glob("backup_*.json"))
            if len(backup_files) > 20:
                for old_file in backup_files[:-20]:
                    old_file.unlink()
            
        except Exception as e:
            logger.error(f"バックアップエラー: {e}")
    
    def restore_from_backup(self, backup_file: Path) -> bool:
        """バックアップからの復元"""
        try:
            with open(backup_file, "r", encoding="utf-8") as f:
                backup_data = json.load(f)
            
            # 状態復元
            state_dict = backup_data["state"]
            restored_state = SystemState(**state_dict)
            
            st.session_state[self.session_key] = restored_state
            
            logger.info(f"バックアップ復元完了: {backup_file}")
            return True
            
        except Exception as e:
            logger.error(f"復元エラー: {e}")
            return False
    
    def export_state(self) -> dict:
        """状態のエクスポート"""
        current_state = self.get_state()
        return asdict(current_state)
    
    def import_state(self, state_dict: dict) -> bool:
        """状態のインポート"""
        try:
            imported_state = SystemState(**state_dict)
            st.session_state[self.session_key] = imported_state
            self._auto_backup()
            return True
        except Exception as e:
            logger.error(f"インポートエラー: {e}")
            return False
    
    def reset_session(self) -> None:
        """セッションのリセット"""
        if self.session_key in st.session_state:
            del st.session_state[self.session_key]
        self._initialize_session_state()
        logger.info("セッション完全リセット")
    
    def _handle_state_error(self, error: Exception) -> None:
        """状態エラーの処理"""
        logger.error(f"状態管理エラー: {error}")
        
        # エラー通知をStreamlitに表示
        st.error(f"システムエラーが発生しました: {str(error)}")
        st.error("状態の復旧を試みています...")
        
        # 緊急時の状態復旧
        try:
            self._initialize_session_state()
            st.success("状態を初期化しました")
        except Exception as recovery_error:
            st.error(f"復旧に失敗しました: {recovery_error}")
    
    def initialize_ui(self) -> None:
        """UI初期化・スタイリング適用"""
        if UI_STYLING_AVAILABLE:
            # ダイヤモンド級CSS注入
            inject_diamond_css()
            inject_custom_metrics_style()
            
            # 品質バッジ表示
            render_quality_badge()
        else:
            logger.warning("UIスタイリングモジュールが利用できません")

# グローバルインスタンス
state_manager = StateManager()

def get_state_manager() -> StateManager:
    """状態管理インスタンスの取得（完全セーフ初期化）"""
    global state_manager
    
    # グローバルインスタンスが未初期化の場合
    if 'state_manager' not in globals() or state_manager is None:
        logger.info("グローバルstate_manager未初期化 - 新規作成")
        state_manager = StateManager()
    
    # セッションキーが存在しない場合は強制初期化
    if state_manager.session_key not in st.session_state:
        logger.info("セッション状態が存在しません - 緊急初期化実行")
        try:
            state_manager._initialize_session_state()
        except Exception as e:
            logger.error(f"初期化エラー: {e}")
            # 完全に新しいインスタンスを作成
            state_manager = StateManager()
            state_manager._initialize_session_state()
    
    return state_manager

def initialize_tonosama_ui():
    """TONOSAMA UIの完全初期化（Streamlit Cloud対応）"""
    try:
        # まず状態管理を確実に初期化
        state_manager = get_state_manager()
        
        if UI_STYLING_AVAILABLE:
            # ダイヤモンド級CSS注入
            inject_diamond_css()
            inject_custom_metrics_style()
            
            # TONOSAMAヘッダー表示（状態が安定してから）
            current_state = state_manager.get_state()
            render_tonosama_header()
            
            # 品質バッジ（非固定位置）
            render_quality_badge()
            
            logger.info("TONOSAMA UI初期化完了")
        else:
            logger.warning("UIスタイリングモジュールが利用できません")
            
    except Exception as e:
        logger.error(f"UI初期化エラー: {e}")
        # 基本的な表示だけでも確保
        st.markdown("# 🏮 TONOSAMA Professional System")
        st.error("UI初期化に問題がありました。基本機能は動作します。")