"""
🏮 TONOSAMA Professional System - Streamlit Edition
1兆円ダイヤモンド級品質の多言語レストランシステム

完璧なナビゲーション・状態管理・ユーザーエクスペリエンス
"""

import streamlit as st
from streamlit_option_menu import option_menu
import asyncio
import logging
from datetime import datetime
from pathlib import Path

# モジュールインポート
from modules.state_manager import get_state_manager, SystemState, initialize_tonosama_ui
from modules.openai_integration import get_openai_integration
from modules.ui_styling import render_step_progress, render_diamond_divider, render_tonosama_footer

# ページ設定
st.set_page_config(
    page_title="🏮 TONOSAMA Professional System",
    page_icon="🏮",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://tonosama-pro.com/help',
        'Report a bug': 'https://tonosama-pro.com/support',
        'About': """
        # TONOSAMA Professional System
        
        外国人観光客向け完璧多言語レストランシステム
        
        **特徴:**
        - 🤖 AI帝王による14言語食レポ生成
        - 📊 正太さん形式CSV自動生成
        - 🔄 戸塚さん連携システム
        - 💎 1兆円ダイヤモンド級品質
        
        Version 2.0 Diamond Edition
        """
    }
)

# カスタムCSS
st.markdown("""
<style>
    /* メインテーマ */
    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f172a 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        border: 1px solid #22c55e;
    }
    
    .main-title {
        color: #22c55e;
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 20px rgba(34, 197, 94, 0.5);
    }
    
    .main-subtitle {
        color: #d1d5db;
        font-size: 1.2rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .diamond-badge {
        background: linear-gradient(45deg, #ffd700, #ffed4e);
        color: #1a1a2e;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-weight: bold;
        text-align: center;
        margin: 1rem auto;
        display: block;
        width: fit-content;
        box-shadow: 0 5px 15px rgba(255, 215, 0, 0.4);
    }
    
    /* ステップ表示 */
    .step-indicator {
        background: rgba(34, 197, 94, 0.1);
        border: 2px solid #22c55e;
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        text-align: center;
    }
    
    .step-current {
        color: #22c55e;
        font-size: 1.5rem;
        font-weight: bold;
    }
    
    .step-progress {
        color: #9ca3af;
        font-size: 1rem;
        margin-top: 0.5rem;
    }
    
    /* 成功/警告/エラー表示 */
    .success-box {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.1), rgba(34, 197, 94, 0.05));
        border: 1px solid #22c55e;
        border-radius: 10px;
        padding: 1rem;
        color: #22c55e;
    }
    
    .warning-box {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(245, 158, 11, 0.05));
        border: 1px solid #f59e0b;
        border-radius: 10px;
        padding: 1rem;
        color: #f59e0b;
    }
    
    .error-box {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(239, 68, 68, 0.05));
        border: 1px solid #ef4444;
        border-radius: 10px;
        padding: 1rem;
        color: #ef4444;
    }
    
    /* ナビゲーション改善 */
    .nav-button {
        background: linear-gradient(135deg, #22c55e, #16a34a);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s;
        margin: 0.5rem;
    }
    
    .nav-button:hover {
        background: linear-gradient(135deg, #16a34a, #15803d);
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(34, 197, 94, 0.4);
    }
    
    .nav-button:disabled {
        background: #6b7280;
        cursor: not-allowed;
        transform: none;
        box-shadow: none;
    }
    
    /* カード表示 */
    .info-card {
        background: rgba(31, 41, 55, 0.8);
        border: 1px solid #374151;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.1), rgba(34, 197, 94, 0.05));
        border: 1px solid rgba(34, 197, 94, 0.3);
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TONOSAMAApp:
    """メインアプリケーションクラス"""
    
    def __init__(self):
        """初期化"""
        self.state_manager = get_state_manager()
        self.openai = get_openai_integration()
        
        # ページ定義
        self.pages = {
            "🏠 ホーム": "home",
            "🏪 Step1: 店舗基本情報": "step1", 
            "📝 Step2: 店主ストーリー": "step2",
            "🍽️ Step3: メニュー情報": "step3",
            "📊 Step4: 順序最適化": "step4",
            "🤖 Step5: AI食レポ": "step5",
            "🎆 Step6: 完了・プラン選択": "step6",
            "⚙️ システム設定": "settings"
        }
    
    def run(self):
        """メインアプリケーション実行"""
        try:
            # セッション状態確認・初期化（緊急対応）
            if "tonosama_professional_state" not in st.session_state:
                self.state_manager._initialize_session_state()
            
            # ヘッダー表示
            self.render_header()
            
            # ステップ進捗表示
            current_state = self.state_manager.get_state()
            render_step_progress(current_state.current_step)
            
            # 分割線
            render_diamond_divider()
            
            # サイドバーナビゲーション
            selected_page = self.render_sidebar()
            
            # メインコンテンツ
            self.render_main_content(selected_page)
            
            # フッター
            self.render_footer()
            
        except Exception as e:
            logger.error(f"アプリケーションエラー: {e}")
            st.error("システムエラーが発生しました。ページを再読み込みしてください。")
    
    def render_header(self):
        """ヘッダー表示"""
        st.markdown("""
        <div class="main-header">
            <div class="main-title">🏮 TONOSAMA Professional System</div>
            <div class="main-subtitle">外国人観光客向け完璧多言語レストランシステム</div>
            <div class="diamond-badge">💎 1兆円ダイヤモンド級品質 💎</div>
        </div>
        """, unsafe_allow_html=True)
        
        # 現在のステップ表示
        current_state = self.state_manager.get_state()
        st.markdown(f"""
        <div class="step-indicator">
            <div class="step-current">現在のステップ: Step {current_state.current_step}</div>
            <div class="step-progress">セッションID: {current_state.session_id[:8]}... | 開始時刻: {current_state.created_at[:19]}</div>
        </div>
        """, unsafe_allow_html=True)
    
    def render_sidebar(self) -> str:
        """サイドバーナビゲーション"""
        with st.sidebar:
            st.markdown("### 🧭 ナビゲーション")
            
            # ページ選択
            selected = option_menu(
                menu_title=None,
                options=list(self.pages.keys()),
                icons=[
                    "house", "shop", "pencil-square", "grid-3x3-gap", 
                    "bar-chart", "robot", "stars", "gear"
                ],
                default_index=0,
                orientation="vertical",
                styles={
                    "container": {"padding": "0!important", "background-color": "transparent"},
                    "icon": {"color": "#22c55e", "font-size": "18px"},
                    "nav-link": {
                        "font-size": "14px",
                        "text-align": "left", 
                        "margin": "2px",
                        "padding": "10px",
                        "border-radius": "10px"
                    },
                    "nav-link-selected": {"background-color": "#22c55e"}
                }
            )
            
            # システム状態表示
            self.render_system_status()
            
            # クイックアクション
            self.render_quick_actions()
            
            return self.pages[selected]
    
    def render_system_status(self):
        """システム状態表示"""
        st.markdown("---")
        st.markdown("### 📊 システム状態")
        
        current_state = self.state_manager.get_state()
        
        # 進行状況メトリクス
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                label="完了ステップ",
                value=f"{current_state.current_step}/6",
                delta=None
            )
        
        with col2:
            # メニュー数
            menu_count = len(current_state.menu) if current_state.menu else 0
            st.metric(
                label="メニュー数",
                value=menu_count,
                delta=None
            )
        
        # 状態チェックリスト
        st.markdown("#### ✅ 完了状況")
        
        checks = [
            ("店舗情報", bool(current_state.store and current_state.store.store_name_ja)),
            ("店主ストーリー", current_state.story_approved),
            ("メニュー登録", menu_count > 0),
            ("AI食レポ", bool(current_state.generated_content)),
            ("プラン選択", bool(current_state.selected_plan))
        ]
        
        for item, completed in checks:
            icon = "✅" if completed else "⏳"
            color = "#22c55e" if completed else "#9ca3af"
            st.markdown(f'<span style="color: {color}">{icon} {item}</span>', unsafe_allow_html=True)
    
    def render_quick_actions(self):
        """クイックアクション"""
        st.markdown("---")
        st.markdown("### ⚡ クイックアクション")
        
        # APIキー設定
        if st.button("🔑 APIキー設定", use_container_width=True):
            self.show_api_key_setup()
        
        # データエクスポート
        if st.button("📤 データエクスポート", use_container_width=True):
            self.export_session_data()
        
        # セッションリセット
        if st.button("🔄 セッションリセット", use_container_width=True, type="secondary"):
            if st.session_state.get('confirm_reset'):
                self.state_manager.reset_session()
                st.rerun()
            else:
                st.session_state['confirm_reset'] = True
                st.warning("もう一度押すとセッションがリセットされます")
    
    def render_main_content(self, page: str):
        """メインコンテンツ表示"""
        if page == "home":
            self.render_home_page()
        elif page == "step1":
            self.render_step1()
        elif page == "step2":
            self.render_step2()
        elif page == "step3":
            self.render_step3()
        elif page == "step4":
            self.render_step4()
        elif page == "step5":
            self.render_step5()
        elif page == "step6":
            self.render_step6()
        elif page == "settings":
            self.render_settings()
        else:
            st.error(f"不明なページ: {page}")
    
    def render_home_page(self):
        """ホームページ表示"""
        st.markdown("# 🏠 ホーム")
        st.markdown("完璧な多言語レストランシステムへようこそ")
        
        # システム概要
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3>🤖 AI帝王システム</h3>
                <p>世界最高レベルの食レポーター「帝王」による14言語コンテンツ生成</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3>📊 正太さん形式</h3>
                <p>横型CSV・自動フォルダ作成・完璧なデータ管理システム</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h3>📧 戸塚さん連携</h3>
                <p>無料・有料プラン自動振り分け・完全自動化収益システム</p>
            </div>
            """, unsafe_allow_html=True)
        
        # 進行状況
        current_state = self.state_manager.get_state()
        
        st.markdown("## 📈 進行状況")
        
        progress = current_state.current_step / 6
        st.progress(progress)
        st.write(f"Step {current_state.current_step}/6 完了 ({progress*100:.0f}%)")
        
        # 次のアクション
        st.markdown("## 🎯 次のアクション")
        
        if current_state.current_step == 1:
            st.info("Step1: 店舗基本情報を入力してシステムを開始しましょう")
        elif current_state.current_step == 2:
            st.info("Step2: 店主の想いを15問で詳しく教えてください")
        elif current_state.current_step == 3:
            st.info("Step3: メニュー情報を登録しましょう")
        elif current_state.current_step == 4:
            st.info("Step4: メニューの順序を最適化しましょう")
        elif current_state.current_step == 5:
            st.info("Step5: AI帝王による食レポを生成しましょう")
        elif current_state.current_step == 6:
            st.info("Step6: プランを選択して完了です！")
        else:
            st.success("全ステップ完了！お疲れさまでした")
        
        # 最近の活動
        self.render_recent_activity()
    
    def render_recent_activity(self):
        """最近の活動表示"""
        st.markdown("## 📝 最近の活動")
        
        current_state = self.state_manager.get_state()
        
        activities = []
        
        # セッション開始
        activities.append({
            'time': current_state.created_at,
            'action': 'セッション開始',
            'icon': '🚀'
        })
        
        # ストーリー承認
        if current_state.story_approved_at:
            activities.append({
                'time': current_state.story_approved_at,
                'action': '店主ストーリー承認',
                'icon': '✅'
            })
        
        # プラン選択
        if current_state.plan_selected_at:
            activities.append({
                'time': current_state.plan_selected_at,
                'action': f'プラン選択: {current_state.selected_plan}',
                'icon': '🎯'
            })
        
        # 最新の更新
        activities.append({
            'time': current_state.last_updated,
            'action': '最終更新',
            'icon': '🔄'
        })
        
        # 時系列順にソート
        activities.sort(key=lambda x: x['time'], reverse=True)
        
        for activity in activities[:5]:  # 最新5件表示
            try:
                time_str = datetime.fromisoformat(activity['time'].replace('Z', '+00:00')).strftime('%m/%d %H:%M')
                st.write(f"{activity['icon']} {time_str} - {activity['action']}")
            except:
                st.write(f"{activity['icon']} {activity['action']}")
    
    def render_step1(self):
        """Step1: 店舗基本情報"""
        st.markdown("# 🏪 Step1: 店舗基本情報")
        st.markdown("外国人観光客が安心して来店できる基本情報を収集します")
        
        # メッセージ表示：実装は各ページモジュールで行う
        st.info("この機能は pages/1_店舗基本情報.py で実装されます")
        
        # ナビゲーションボタン
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← ホームに戻る", key="step1_home"):
                st.rerun()
        with col2:
            if st.button("Step2へ進む →", key="step1_next", type="primary"):
                self.state_manager.update_state(current_step=2)
                st.rerun()
    
    def render_step2(self):
        """Step2: 店主ストーリー（プレースホルダー）"""
        st.markdown("# 📝 Step2: 店主ストーリー")
        st.info("この機能は pages/2_店主ストーリー.py で実装されます")
    
    def render_step3(self):
        """Step3: メニュー情報（プレースホルダー）"""
        st.markdown("# 🍽️ Step3: メニュー情報")
        st.info("この機能は pages/3_メニュー情報.py で実装されます")
    
    def render_step4(self):
        """Step4: 順序最適化（プレースホルダー）"""
        st.markdown("# 📊 Step4: 順序最適化")
        st.info("この機能は pages/4_順序最適化.py で実装されます")
    
    def render_step5(self):
        """Step5: AI食レポ（プレースホルダー）"""
        st.markdown("# 🤖 Step5: AI食レポ")
        st.info("この機能は pages/5_AI食レポ.py で実装されます")
    
    def render_step6(self):
        """Step6: 完了・プラン選択（プレースホルダー）"""
        st.markdown("# 🎆 Step6: 完了・プラン選択")
        st.info("この機能は pages/6_完了・プラン選択.py で実装されます")
    
    def render_settings(self):
        """システム設定"""
        st.markdown("# ⚙️ システム設定")
        
        tab1, tab2, tab3 = st.tabs(["APIキー設定", "システム情報", "データ管理"])
        
        with tab1:
            self.render_api_settings()
        
        with tab2:
            self.render_system_info()
        
        with tab3:
            self.render_data_management()
    
    def render_api_settings(self):
        """API設定"""
        st.markdown("### 🔑 APIキー設定")
        
        # OpenAI APIキー
        st.markdown("#### OpenAI API")
        current_key = self.openai.get_api_key()
        key_status = "設定済み" if current_key else "未設定"
        
        st.write(f"現在の状態: {key_status}")
        
        new_key = st.text_input(
            "OpenAI APIキー",
            value="",
            type="password",
            placeholder="sk-..."
        )
        
        if st.button("APIキー更新"):
            if new_key and new_key.startswith("sk-"):
                if self.openai.validate_api_key(new_key):
                    st.session_state["openai_api_key"] = new_key
                    st.success("APIキーを更新しました")
                else:
                    st.error("無効なAPIキーです")
            else:
                st.error("正しいAPIキー形式で入力してください")
    
    def render_system_info(self):
        """システム情報"""
        st.markdown("### 📊 システム情報")
        
        current_state = self.state_manager.get_state()
        
        # システム統計
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("セッション数", 1)
            st.metric("処理ステップ", f"{current_state.current_step}/6")
        
        with col2:
            menu_count = len(current_state.menu) if current_state.menu else 0
            st.metric("メニュー数", menu_count)
            
            answer_count = len([a for a in current_state.imperator_answers.values() if a.strip()]) if current_state.imperator_answers else 0
            st.metric("回答数", f"{answer_count}/15")
        
        with col3:
            lang_count = len(current_state.generated_content) if current_state.generated_content else 0
            st.metric("生成言語", f"{lang_count}/14")
            
            st.metric("承認状況", "済" if current_state.story_approved else "未")
        
        # システム設定表示
        st.markdown("### ⚙️ 設定情報")
        
        settings = {
            "バージョン": "2.0 Diamond Edition",
            "モデル": self.openai.model,
            "対応言語": "14言語",
            "バックアップ": "自動"
        }
        
        for key, value in settings.items():
            st.write(f"**{key}**: {value}")
    
    def render_data_management(self):
        """データ管理"""
        st.markdown("### 💾 データ管理")
        
        # エクスポート
        st.markdown("#### エクスポート")
        if st.button("現在のデータをエクスポート"):
            self.export_session_data()
        
        # インポート
        st.markdown("#### インポート")
        uploaded_file = st.file_uploader(
            "データファイル選択",
            type=['json'],
            help="以前にエクスポートしたJSONファイル"
        )
        
        if uploaded_file and st.button("データをインポート"):
            try:
                import json
                data = json.load(uploaded_file)
                if self.state_manager.import_state(data):
                    st.success("データをインポートしました")
                    st.rerun()
                else:
                    st.error("インポートに失敗しました")
            except Exception as e:
                st.error(f"ファイル読み込みエラー: {e}")
        
        # バックアップ管理
        st.markdown("#### バックアップ管理")
        backup_dir = Path("data/backups")
        if backup_dir.exists():
            backup_files = list(backup_dir.glob("backup_*.json"))
            if backup_files:
                st.write(f"バックアップファイル: {len(backup_files)}件")
                
                # 最新のバックアップファイル表示
                latest_backup = max(backup_files, key=lambda x: x.stat().st_mtime)
                st.write(f"最新バックアップ: {latest_backup.name}")
                
                if st.button("最新バックアップから復元"):
                    if self.state_manager.restore_from_backup(latest_backup):
                        st.success("バックアップから復元しました")
                        st.rerun()
                    else:
                        st.error("復元に失敗しました")
            else:
                st.info("バックアップファイルがありません")
        
        # セッションリセット
        st.markdown("#### 危険な操作")
        st.warning("以下の操作は元に戻せません")
        
        if st.button("全データを削除してリセット", type="secondary"):
            if st.session_state.get('confirm_full_reset'):
                self.state_manager.reset_session()
                st.success("セッションを完全にリセットしました")
                st.rerun()
            else:
                st.session_state['confirm_full_reset'] = True
                st.error("もう一度押すと全データが削除されます")
    
    def render_footer(self):
        """フッター表示"""
        render_tonosama_footer()
    
    def show_api_key_setup(self):
        """APIキー設定モーダル"""
        with st.expander("🔑 APIキー設定", expanded=True):
            st.markdown("システムの完全な機能を使用するにはAPIキーが必要です")
            
            new_key = st.text_input(
                "OpenAI APIキー",
                type="password",
                placeholder="sk-..."
            )
            
            if st.button("設定"):
                if new_key and self.openai.validate_api_key(new_key):
                    st.session_state["openai_api_key"] = new_key
                    st.success("APIキーを設定しました")
                else:
                    st.error("無効なAPIキーです")
    
    def export_session_data(self):
        """セッションデータエクスポート"""
        try:
            data = self.state_manager.export_state()
            
            import json
            json_data = json.dumps(data, ensure_ascii=False, indent=2)
            
            current_state = self.state_manager.get_state()
            filename = f"tonosama_data_{current_state.session_id[:8]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            st.download_button(
                label="📤 データをダウンロード",
                data=json_data,
                file_name=filename,
                mime="application/json"
            )
            
            st.success("エクスポートデータを準備しました")
            
        except Exception as e:
            st.error(f"エクスポートエラー: {e}")

def main():
    """メイン実行関数"""
    try:
        # UI初期化（ダイヤモンド級スタイリング）
        initialize_tonosama_ui()
        
        # アプリケーション初期化
        app = TONOSAMAApp()
        
        # 実行
        app.run()
        
    except Exception as e:
        logger.error(f"アプリケーション実行エラー: {e}")
        
        st.error("システムエラーが発生しました")
        st.exception(e)
        
        if st.button("🔄 アプリケーション再起動"):
            st.rerun()

if __name__ == "__main__":
    main()