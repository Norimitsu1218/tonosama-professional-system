"""
📊 TONOSAMA Professional System - Step4: 順序最適化
1兆円ダイヤモンド級品質のメニュー順序最適化システム

AI提案・ドラッグ&ドロップ対応・外国人観光客配慮
"""

import streamlit as st
from modules.state_manager import get_state_manager
from modules.openai_integration import get_openai_integration
import logging
import asyncio
from typing import List, Dict
from PIL import Image
import io

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ページ設定
st.set_page_config(
    page_title="📊 Step4: 順序最適化",
    page_icon="📊",
    layout="wide"
)

def render_purpose_explanation():
    """目的説明表示"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(34, 197, 94, 0.1), rgba(34, 197, 94, 0.05)); 
                border: 1px solid rgba(34, 197, 94, 0.3); border-radius: 12px; padding: 16px; margin-bottom: 20px;">
        <div style="display: flex; align-items: center; margin-bottom: 10px;">
            <span style="font-size: 24px; margin-right: 10px;">🎯</span>
            <span style="color: #22c55e; font-weight: bold; font-size: 18px;">なぜこの順序最適化が必要？</span>
        </div>
        <div style="color: #d1d5db;">
            <strong>外国人観光客が注文しやすいメニュー順序を戦略的に設計します</strong><br>
            • 推奨度順 → イチオシメニューを最初に表示<br>
            • カテゴリ整理 → 前菜→メイン→デザート の自然な流れ<br>
            • AI提案 → 文化的配慮と価格帯バランス最適化
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_current_order_display():
    """現在の順序表示"""
    st.markdown("### 📋 現在のメニュー順序")
    
    state_manager = get_state_manager()
    current_state = state_manager.get_state()
    
    if not current_state.menu or len(current_state.menu) == 0:
        st.info("📝 メニューが登録されていません。Step3でメニューを追加してください。")
        return
    
    # 現在の順序を表形式で表示
    menu_data = []
    for i, item in enumerate(current_state.menu):
        menu_data.append({
            "順番": i + 1,
            "料理名": item.dish_name,
            "カテゴリ": item.category,
            "価格": f"¥{item.price:,}",
            "推奨度": "⭐" * item.recommendation_level,
            "説明": item.description[:30] + "..." if len(item.description or "") > 30 else (item.description or "")
        })
    
    st.dataframe(
        menu_data,
        use_container_width=True,
        hide_index=True
    )

def render_optimization_options():
    """最適化オプション"""
    st.markdown("### 🔧 自動最適化オプション")
    
    state_manager = get_state_manager()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("⭐ 推奨度順", use_container_width=True, type="secondary"):
            state_manager.sort_menu_by_recommendation()
            st.success("✅ 推奨度順に並び替えました")
            st.rerun()
    
    with col2:
        if st.button("💰 価格順", use_container_width=True, type="secondary"):
            state_manager.sort_menu_by_price()
            st.success("✅ 価格順に並び替えました")
            st.rerun()
    
    with col3:
        if st.button("🏷️ カテゴリ順", use_container_width=True, type="secondary"):
            state_manager.sort_menu_by_category()
            st.success("✅ カテゴリ順に並び替えました")
            st.rerun()
    
    with col4:
        if st.button("🤖 AI最適化", use_container_width=True, type="primary"):
            optimize_with_ai()

def optimize_with_ai():
    """AI による順序最適化"""
    async def ai_optimize():
        state_manager = get_state_manager()
        openai_integration = get_openai_integration()
        current_state = state_manager.get_state()
        
        try:
            with st.spinner("🤖 AI が外国人観光客向けに最適な順序を分析中..."):
                # メニューデータ準備
                menu_items = []
                for item in current_state.menu:
                    menu_items.append({
                        "dish_name": item.dish_name,
                        "category": item.category,
                        "price": item.price,
                        "description": item.description,
                        "recommendation_level": item.recommendation_level,
                        "allergens": item.allergens
                    })
                
                # 店舗情報
                store_info = {
                    "store_name": current_state.store.store_name_ja,
                    "store_type": current_state.store.store_type,
                    "price_band": current_state.store.price_band
                }
                
                # AI順序最適化実行
                optimized_order = await openai_integration.optimize_menu_order(
                    menu_items, store_info
                )
                
                if optimized_order:
                    # 最適化された順序を適用
                    state_manager.apply_optimized_order(optimized_order)
                    st.success("✨ AI最適化が完了しました！外国人観光客に最適な順序に並び替えられました")
                else:
                    st.error("AI最適化に失敗しました")
                
                st.rerun()
                
        except Exception as e:
            logger.error(f"AI最適化エラー: {e}")
            st.error("AI最適化中にエラーが発生しました")
    
    # 非同期実行
    try:
        asyncio.run(ai_optimize())
    except Exception as e:
        logger.error(f"非同期実行エラー: {e}")
        st.error("システムエラーが発生しました")

def render_manual_sorting():
    """手動並び替えセクション"""
    st.markdown("### ✋ 手動並び替え")
    st.info("📝 **使用方法**: 下記のメニューをドラッグ&ドロップして順序を調整してください")
    
    state_manager = get_state_manager()
    current_state = state_manager.get_state()
    
    if not current_state.menu:
        return
    
    # 並び替え可能なリスト表示
    with st.container():
        sortable_items = []
        
        for i, item in enumerate(current_state.menu):
            container = st.container()
            
            with container:
                col1, col2, col3, col4, col5 = st.columns([1, 3, 2, 2, 1])
                
                with col1:
                    # 上下移動ボタン
                    if i > 0:
                        if st.button("⬆️", key=f"up_{i}", help="上に移動"):
                            state_manager.move_menu_item(i, i - 1)
                            st.rerun()
                    
                    if i < len(current_state.menu) - 1:
                        if st.button("⬇️", key=f"down_{i}", help="下に移動"):
                            state_manager.move_menu_item(i, i + 1)
                            st.rerun()
                
                with col2:
                    st.markdown(f"**{i + 1}. {item.dish_name}**")
                    st.caption(f"{item.category} | {'⭐' * item.recommendation_level}")
                
                with col3:
                    st.metric("価格", f"¥{item.price:,}")
                
                with col4:
                    # 画像サムネイル
                    if item.image_data:
                        try:
                            image = Image.open(io.BytesIO(item.image_data))
                            st.image(image, width=80)
                        except:
                            st.caption("🖼️ 画像")
                    else:
                        st.caption("📷 画像なし")
                
                with col5:
                    # 詳細表示
                    if st.button("👁️", key=f"view_{i}", help="詳細表示"):
                        show_item_details(item)
            
            st.markdown("---")

def show_item_details(item):
    """アイテム詳細表示"""
    with st.expander(f"📋 {item.dish_name} の詳細", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**カテゴリ**: {item.category}")
            st.write(f"**価格**: ¥{item.price:,}")
            st.write(f"**推奨度**: {'⭐' * item.recommendation_level}")
            
            if item.allergens:
                st.write(f"**アレルギー**: {'、'.join(item.allergens)}")
        
        with col2:
            if item.image_data:
                try:
                    image = Image.open(io.BytesIO(item.image_data))
                    st.image(image, caption=item.dish_name, width=200)
                except:
                    st.caption("画像表示エラー")
        
        if item.description:
            st.write("**説明**")
            st.write(item.description)

def render_optimization_preview():
    """最適化プレビュー"""
    st.markdown("### 👁️ 順序最適化プレビュー")
    st.info("現在の順序で外国人観光客にどのように表示されるかのプレビューです")
    
    state_manager = get_state_manager()
    current_state = state_manager.get_state()
    
    if not current_state.menu:
        return
    
    # 外国人観光客向け表示プレビュー
    st.markdown("#### 🌍 外国人観光客向け表示イメージ")
    
    with st.container():
        # 擬似メニュー表示
        st.markdown("""
        <div style="background: #1f2937; padding: 20px; border-radius: 12px; margin: 10px 0;">
            <h3 style="color: #22c55e; text-align: center; margin-bottom: 20px;">
                🏮 RESTAURANT MENU / レストランメニュー
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        for i, item in enumerate(current_state.menu[:5]):  # 最初の5つのみプレビュー
            with st.container():
                col1, col2, col3 = st.columns([1, 2, 1])
                
                with col1:
                    if item.image_data:
                        try:
                            image = Image.open(io.BytesIO(item.image_data))
                            st.image(image, width=120)
                        except:
                            st.write("🍽️")
                    else:
                        st.write("🍽️")
                
                with col2:
                    st.markdown(f"**{i + 1}. {item.dish_name}**")
                    st.write(f"*{item.category}*")
                    
                    if item.description:
                        preview_desc = item.description[:80] + "..." if len(item.description) > 80 else item.description
                        st.caption(preview_desc)
                    
                    if item.allergens:
                        st.caption(f"⚠️ Contains: {', '.join(item.allergens)}")
                
                with col3:
                    st.markdown(f"**¥{item.price:,}**")
                    st.caption(f"{'⭐' * item.recommendation_level}")
                
                st.markdown("---")
        
        if len(current_state.menu) > 5:
            st.caption(f"... その他 {len(current_state.menu) - 5} 品")

def render_statistics():
    """統計情報表示"""
    st.markdown("### 📊 メニュー統計")
    
    state_manager = get_state_manager()
    current_state = state_manager.get_state()
    
    if not current_state.menu:
        return
    
    # 統計計算
    total_items = len(current_state.menu)
    avg_price = sum(item.price for item in current_state.menu) / total_items
    high_recommend = len([item for item in current_state.menu if item.recommendation_level >= 4])
    
    # カテゴリ別統計
    category_counts = {}
    for item in current_state.menu:
        category = item.category or "その他"
        category_counts[category] = category_counts.get(category, 0) + 1
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("総メニュー数", total_items)
    
    with col2:
        st.metric("平均価格", f"¥{avg_price:.0f}")
    
    with col3:
        st.metric("推奨メニュー", f"{high_recommend}/{total_items}")
    
    with col4:
        st.metric("カテゴリ数", len(category_counts))
    
    # カテゴリ別内訳
    col5, col6 = st.columns(2)
    
    with col5:
        st.markdown("#### 📊 カテゴリ別内訳")
        for category, count in category_counts.items():
            st.write(f"• {category}: {count}品")
    
    with col6:
        st.markdown("#### 💰 価格帯分布")
        price_ranges = {"〜1,000円": 0, "1,000-3,000円": 0, "3,000円〜": 0}
        
        for item in current_state.menu:
            if item.price < 1000:
                price_ranges["〜1,000円"] += 1
            elif item.price < 3000:
                price_ranges["1,000-3,000円"] += 1
            else:
                price_ranges["3,000円〜"] += 1
        
        for range_name, count in price_ranges.items():
            st.write(f"• {range_name}: {count}品")

def render_validation_and_navigation():
    """バリデーションとナビゲーション"""
    st.markdown("---")
    
    state_manager = get_state_manager()
    current_state = state_manager.get_state()
    
    # バリデーション状況
    menu_count = len(current_state.menu) if current_state.menu else 0
    
    if menu_count == 0:
        st.error("⚠️ メニューが登録されていません")
        st.info("Step3に戻ってメニューを登録してください")
    else:
        st.success(f"✅ {menu_count}品のメニュー順序が設定されています")
    
    # ナビゲーションボタン
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("← Step3に戻る", use_container_width=True):
            st.switch_page("pages/3_🍽️_メニュー情報.py")
    
    with col2:
        if st.button("🏠 ホームに戻る", use_container_width=True):
            st.switch_page("app.py")
    
    with col3:
        can_proceed = state_manager.can_proceed_to_step(5)
        
        if st.button(
            "Step5へ進む →", 
            use_container_width=True, 
            type="primary",
            disabled=not can_proceed
        ):
            if can_proceed:
                state_manager.update_state(current_step=5)
                st.switch_page("pages/5_🤖_AI食レポ.py")
            else:
                st.error("❌ メニューの順序を確認してください\n💡 解決方法: メニューを登録し、順序を最適化してからお進みください")

def main():
    """メイン関数"""
    try:
        # ページヘッダー
        st.markdown("# 📊 Step4: 順序最適化・外国人観光客配慮")
        
        # 目的説明
        render_purpose_explanation()
        
        # 現在の順序表示
        render_current_order_display()
        
        # 最適化オプション
        render_optimization_options()
        
        # 手動並び替え
        render_manual_sorting()
        
        # プレビュー
        render_optimization_preview()
        
        # 統計情報
        render_statistics()
        
        # バリデーションとナビゲーション
        render_validation_and_navigation()
        
        # 自動保存通知
        state_manager = get_state_manager()
        current_state = state_manager.get_state()
        
        if current_state.menu and len(current_state.menu) > 0:
            st.success("💾 順序情報は自動保存されています")
        
    except Exception as e:
        logger.error(f"Step4ページエラー: {e}")
        st.error("ページ表示エラーが発生しました。再読み込みしてください。")
        st.exception(e)

if __name__ == "__main__":
    main()