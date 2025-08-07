"""
🤖 TONOSAMA Professional System - Step5: AI食レポ生成
1兆円ダイヤモンド級品質の帝王（Imperator）AI食レポ生成システム

14言語完全対応・文化的配慮・品質保証完全装備
"""

import streamlit as st
from modules.state_manager import get_state_manager
from modules.openai_integration import get_openai_integration
from modules.csv_generator import get_csv_generator
import logging
import asyncio
from typing import Dict, List
import json
from datetime import datetime

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ページ設定
st.set_page_config(
    page_title="🤖 Step5: AI食レポ生成",
    page_icon="🤖",
    layout="wide"
)

def render_purpose_explanation():
    """目的説明表示"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(34, 197, 94, 0.1), rgba(34, 197, 94, 0.05)); 
                border: 1px solid rgba(34, 197, 94, 0.3); border-radius: 12px; padding: 16px; margin-bottom: 20px;">
        <div style="display: flex; align-items: center; margin-bottom: 10px;">
            <span style="font-size: 24px; margin-right: 10px;">🎯</span>
            <span style="color: #22c55e; font-weight: bold; font-size: 18px;">AI帝王による14言語食レポ生成</span>
        </div>
        <div style="color: #d1d5db;">
            <strong>世界最高レベルのAI帝王（Imperator）が各料理の魅力を14言語で完璧に表現します</strong><br>
            • 店主ストーリー連携 → 料理に込められた想いを各言語で表現<br>
            • 文化的配慮 → 各国の食文化・宗教的背景に配慮した表現<br>
            • 品質保証 → 4時間の処理時間で完璧な品質を追求
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_imperator_introduction():
    """帝王紹介セクション"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(139, 92, 246, 0.15), rgba(139, 92, 246, 0.05)); 
                border: 1px solid rgba(139, 92, 246, 0.4); border-radius: 12px; padding: 20px; margin: 20px 0;">
        <div style="text-align: center;">
            <div style="font-size: 48px; margin-bottom: 10px;">🏮</div>
            <h2 style="color: #8b5cf6; margin-bottom: 15px;">AI帝王（Imperator）</h2>
            <div style="color: #d1d5db; font-size: 16px;">
                世界14言語を完璧に操る最高峰のAI食レポーター<br>
                <strong>品質第一主義</strong> - 4時間の丁寧な処理で完璧な食レポを生成<br>
                <strong>文化的配慮</strong> - 各国の食文化と宗教的背景を深く理解<br>
                <strong>感動創造</strong> - 料理の魅力を心に響く表現で世界に伝達
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_generation_status():
    """生成状況表示"""
    st.markdown("### 📊 AI食レポ生成状況")
    
    state_manager = get_state_manager()
    current_state = state_manager.get_state()
    
    if not current_state.menu:
        st.info("📝 メニューが登録されていません。Step3でメニューを追加してください。")
        return False
    
    # 進捗状況計算
    total_menus = len(current_state.menu)
    generated_count = len([item for item in current_state.menu if item.food_reports])
    progress = generated_count / total_menus if total_menus > 0 else 0
    
    # プログレスバー
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("総メニュー数", total_menus)
    
    with col2:
        st.metric("生成済み", generated_count)
    
    with col3:
        st.metric("進捗率", f"{progress:.0%}")
    
    st.progress(progress, text=f"AI食レポ生成: {generated_count}/{total_menus}")
    
    return total_menus > 0

def render_generation_controls():
    """生成コントロール"""
    st.markdown("### 🤖 AI帝王食レポ生成")
    
    state_manager = get_state_manager()
    current_state = state_manager.get_state()
    
    if not current_state.menu:
        return
    
    # 生成オプション
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ⚙️ 生成設定")
        
        # 品質設定
        quality_mode = st.radio(
            "品質モード",
            options=["diamond", "premium", "standard"],
            format_func=lambda x: {
                "diamond": "💎 ダイヤモンド級（4時間処理）",
                "premium": "👑 プレミアム級（2時間処理）", 
                "standard": "⭐ スタンダード（1時間処理）"
            }[x],
            index=0,
            key="quality_mode"
        )
        
        # 言語選択
        st.markdown("**対象言語選択**")
        all_languages = [
            "日本語", "English", "한국어", "中文（简体）", "中文（繁體）", 
            "粵語", "ไทย", "Filipino", "Tiếng Việt", "Bahasa Indonesia",
            "Español", "Deutsch", "Français", "Italiano"
        ]
        
        selected_languages = st.multiselect(
            "生成する言語を選択",
            options=all_languages,
            default=all_languages,
            key="selected_languages"
        )
        
        # 特別配慮事項
        cultural_considerations = st.text_area(
            "特別配慮事項（オプション）",
            placeholder="例: ハラール対応、ビーガン配慮、地域的な味覚の特徴など",
            key="cultural_considerations"
        )
    
    with col2:
        st.markdown("#### 🔍 生成プレビュー")
        
        # 処理時間目安表示
        time_estimates = {
            "diamond": "約4時間",
            "premium": "約2時間",
            "standard": "約1時間"
        }
        
        st.info(f"""
        **選択設定での処理時間目安**
        
        • 品質モード: {quality_mode}
        • 処理時間: {time_estimates[quality_mode]}
        • 対象言語: {len(selected_languages)}言語
        • メニュー数: {len(current_state.menu)}品
        
        ⚠️ **重要**: 帝王は品質第一主義です。
        時間をかけてでも完璧な食レポを生成いたします。
        """)
    
    # 生成実行ボタン
    st.markdown("---")
    
    col3, col4, col5 = st.columns([2, 1, 2])
    
    with col4:
        if st.button(
            "🏮 AI帝王 食レポ生成開始", 
            type="primary", 
            use_container_width=True
        ):
            if len(selected_languages) == 0:
                st.error("❌ 最低1つの言語を選択してください")
            else:
                start_ai_generation(quality_mode, selected_languages, cultural_considerations)

def start_ai_generation(quality_mode: str, languages: List[str], considerations: str):
    """AI生成開始"""
    async def generate_all_reports():
        state_manager = get_state_manager()
        openai_integration = get_openai_integration()
        current_state = state_manager.get_state()
        
        try:
            # 生成開始メッセージ
            st.success("🏮 AI帝王による食レポ生成を開始します...")
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            total_menus = len(current_state.menu)
            
            # 各メニューの食レポ生成
            for i, menu_item in enumerate(current_state.menu):
                status_text.text(f"🤖 「{menu_item.dish_name}」の食レポを{len(languages)}言語で生成中...")
                
                # 店舗ストーリーと連携
                store_context = {
                    "store_name": current_state.store.store_name_ja,
                    "store_type": current_state.store.store_type,
                    "owner_story": current_state.imperator_story
                }
                
                # メニュー情報
                menu_context = {
                    "dish_name": menu_item.dish_name,
                    "category": menu_item.category,
                    "price": menu_item.price,
                    "description": menu_item.description,
                    "recommendation_level": menu_item.recommendation_level,
                    "allergens": menu_item.allergens
                }
                
                # AI食レポ生成
                food_reports = await openai_integration.generate_food_reports(
                    menu_context=menu_context,
                    store_context=store_context,
                    target_languages=languages,
                    quality_mode=quality_mode,
                    cultural_considerations=considerations
                )
                
                if food_reports:
                    # メニューアイテムに食レポを追加
                    state_manager.update_menu_item_reports(i, food_reports)
                    status_text.text(f"✅ 「{menu_item.dish_name}」完了")
                else:
                    status_text.text(f"❌ 「{menu_item.dish_name}」生成失敗")
                
                # プログレスバー更新
                progress = (i + 1) / total_menus
                progress_bar.progress(progress)
            
            # 完了処理
            progress_bar.progress(1.0)
            status_text.text("🎉 全メニューの食レポ生成が完了しました！")
            
            st.success("✨ AI帝王による14言語食レポ生成が完了しました！")
            st.balloons()
            
            # 状態更新
            state_manager.update_state(food_reports_generated=True)
            st.rerun()
            
        except Exception as e:
            logger.error(f"AI生成エラー: {e}")
            st.error(f"AI食レポ生成中にエラーが発生しました: {e}")
    
    # 非同期実行
    try:
        asyncio.run(generate_all_reports())
    except Exception as e:
        logger.error(f"非同期実行エラー: {e}")
        st.error("システムエラーが発生しました")

def render_generated_reports():
    """生成済み食レポ表示"""
    st.markdown("### 📖 生成された食レポ")
    
    state_manager = get_state_manager()
    current_state = state_manager.get_state()
    
    if not current_state.menu:
        return
    
    # 食レポが生成されたメニューのみ表示
    generated_items = [item for item in current_state.menu if item.food_reports]
    
    if not generated_items:
        st.info("まだ食レポが生成されていません。上記ボタンからAI帝王に食レポ生成を依頼してください。")
        return
    
    for item in generated_items:
        with st.expander(f"🍽️ {item.dish_name} の14言語食レポ", expanded=False):
            
            # タブで言語別表示
            if item.food_reports:
                languages = list(item.food_reports.keys())
                
                if languages:
                    tabs = st.tabs(languages[:6])  # 最初の6言語のみタブ表示
                    
                    for i, (tab, lang) in enumerate(zip(tabs, languages[:6])):
                        with tab:
                            report_content = item.food_reports.get(lang, "")
                            if report_content:
                                st.write(report_content)
                                
                                # 品質チェック
                                word_count = len(report_content)
                                if word_count >= 200:
                                    st.success(f"✅ 高品質食レポ ({word_count}文字)")
                                else:
                                    st.warning(f"⚠️ 短い食レポ ({word_count}文字)")
                            else:
                                st.info("この言語の食レポはまだ生成されていません")
                    
                    # 残りの言語は折りたたみ表示
                    if len(languages) > 6:
                        with st.expander(f"その他の言語 ({len(languages)-6}言語)"):
                            for lang in languages[6:]:
                                st.markdown(f"**{lang}**")
                                report_content = item.food_reports.get(lang, "")
                                if report_content:
                                    st.write(report_content)
                                else:
                                    st.info("この言語の食レポはまだ生成されていません")
                                st.markdown("---")

def render_csv_export():
    """CSV出力セクション"""
    st.markdown("### 📊 14言語食レポCSV出力")
    
    state_manager = get_state_manager()
    csv_generator = get_csv_generator()
    current_state = state_manager.get_state()
    
    # 生成済みレポート確認
    generated_items = [item for item in current_state.menu if item.food_reports] if current_state.menu else []
    
    if not generated_items:
        st.info("食レポが生成されていないため、CSV出力はできません")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **CSV出力準備完了**
        
        • 生成済みメニュー: {len(generated_items)}品
        • 正太さん形式: 横型CSV（言語が列）
        • 文字エンコード: UTF-8 with BOM（Excel対応）
        """)
    
    with col2:
        if st.button("📥 14言語食レポCSVダウンロード", type="primary", use_container_width=True):
            try:
                # CSV生成
                csv_data = csv_generator.generate_multilingual_food_reports_csv(
                    store_name=current_state.store.store_name_ja or "restaurant",
                    menu_items=generated_items
                )
                
                # ダウンロードボタン
                st.download_button(
                    label="📥 ダウンロード実行",
                    data=csv_data,
                    file_name=f"{current_state.store.store_name_ja or 'restaurant'}_14言語食レポ.csv",
                    mime="text/csv"
                )
                
                st.success("✅ 食レポCSVを生成しました")
                
            except Exception as e:
                logger.error(f"CSV生成エラー: {e}")
                st.error("CSV生成に失敗しました")

def render_quality_check():
    """品質チェックセクション"""
    st.markdown("### 🔍 品質チェック・統計")
    
    state_manager = get_state_manager()
    current_state = state_manager.get_state()
    
    if not current_state.menu:
        return
    
    # 統計計算
    total_menus = len(current_state.menu)
    generated_menus = len([item for item in current_state.menu if item.food_reports])
    
    if generated_menus == 0:
        st.info("まだ食レポが生成されていません")
        return
    
    # 詳細統計
    total_reports = 0
    total_words = 0
    language_stats = {}
    
    for item in current_state.menu:
        if item.food_reports:
            for lang, report in item.food_reports.items():
                if report:
                    total_reports += 1
                    word_count = len(report)
                    total_words += word_count
                    
                    if lang not in language_stats:
                        language_stats[lang] = {"count": 0, "words": 0}
                    
                    language_stats[lang]["count"] += 1
                    language_stats[lang]["words"] += word_count
    
    # 統計表示
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("生成完了率", f"{generated_menus/total_menus:.0%}")
    
    with col2:
        st.metric("総食レポ数", total_reports)
    
    with col3:
        avg_words = total_words / total_reports if total_reports > 0 else 0
        st.metric("平均文字数", f"{avg_words:.0f}")
    
    with col4:
        st.metric("対応言語数", len(language_stats))
    
    # 言語別詳細
    if language_stats:
        st.markdown("#### 📊 言語別生成状況")
        
        lang_data = []
        for lang, stats in language_stats.items():
            lang_data.append({
                "言語": lang,
                "生成数": stats["count"],
                "平均文字数": f"{stats['words']/stats['count']:.0f}" if stats["count"] > 0 else "0"
            })
        
        st.dataframe(lang_data, use_container_width=True, hide_index=True)

def render_validation_and_navigation():
    """バリデーションとナビゲーション"""
    st.markdown("---")
    
    state_manager = get_state_manager()
    current_state = state_manager.get_state()
    
    # バリデーション
    if current_state.menu:
        generated_count = len([item for item in current_state.menu if item.food_reports])
        total_count = len(current_state.menu)
        
        if generated_count == total_count and generated_count > 0:
            st.success(f"✅ 全{total_count}品の食レポ生成が完了しています！")
        elif generated_count > 0:
            st.warning(f"⚠️ {total_count}品中{generated_count}品の食レポが生成済みです")
        else:
            st.info("まだ食レポが生成されていません")
    else:
        st.error("メニューが登録されていません")
    
    # ナビゲーションボタン
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("← Step4に戻る", use_container_width=True):
            st.switch_page("pages/4_📊_順序最適化.py")
    
    with col2:
        if st.button("🏠 ホームに戻る", use_container_width=True):
            st.switch_page("app.py")
    
    with col3:
        can_proceed = state_manager.can_proceed_to_step(6)
        
        if st.button(
            "Step6へ進む →", 
            use_container_width=True, 
            type="primary",
            disabled=not can_proceed
        ):
            if can_proceed:
                state_manager.update_state(current_step=6)
                st.switch_page("pages/6_🎆_完了・プラン選択.py")
            else:
                st.error("❌ AI食レポの生成を完了してください\n💡 解決方法: 上記のAI帝王ボタンから全メニューの食レポを生成してください")

def main():
    """メイン関数"""
    try:
        # ページヘッダー
        st.markdown("# 🤖 Step5: AI食レポ・14言語完全対応")
        
        # 目的説明
        render_purpose_explanation()
        
        # 帝王紹介
        render_imperator_introduction()
        
        # 生成状況確認
        if render_generation_status():
            # 生成コントロール
            render_generation_controls()
            
            # 生成済みレポート表示
            render_generated_reports()
            
            # CSV出力
            render_csv_export()
            
            # 品質チェック
            render_quality_check()
        
        # バリデーションとナビゲーション
        render_validation_and_navigation()
        
        # 自動保存通知
        state_manager = get_state_manager()
        current_state = state_manager.get_state()
        
        if current_state.food_reports_generated:
            st.success("💾 AI食レポは自動保存されています")
        
    except Exception as e:
        logger.error(f"Step5ページエラー: {e}")
        st.error("ページ表示エラーが発生しました。再読み込みしてください。")
        st.exception(e)

if __name__ == "__main__":
    main()