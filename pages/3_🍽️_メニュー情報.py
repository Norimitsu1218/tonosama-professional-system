"""
🍽️ TONOSAMA Professional System - Step3: メニュー情報
1兆円ダイヤモンド級品質のメニュー管理システム

ドラッグ&ドロップ対応・画像処理完全装備
"""

import streamlit as st
from modules.state_manager import get_state_manager
from modules.csv_generator import get_csv_generator
import logging
from typing import List, Dict
from PIL import Image
import io

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ページ設定
st.set_page_config(
    page_title="🍽️ Step3: メニュー情報",
    page_icon="🍽️",
    layout="wide"
)

def render_purpose_explanation():
    """目的説明表示"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(34, 197, 94, 0.1), rgba(34, 197, 94, 0.05)); 
                border: 1px solid rgba(34, 197, 94, 0.3); border-radius: 12px; padding: 16px; margin-bottom: 20px;">
        <div style="display: flex; align-items: center; margin-bottom: 10px;">
            <span style="font-size: 24px; margin-right: 10px;">🎯</span>
            <span style="color: #22c55e; font-weight: bold; font-size: 18px;">なぜこの入力が必要？</span>
        </div>
        <div style="color: #d1d5db;">
            <strong>外国人観光客が注文しやすい14言語メニューを作成します</strong><br>
            • メニュー情報 → AI翻訳で正確な14言語表示<br>
            • 価格・カテゴリ → 予算と嗜好に合わせた検索機能<br>
            • 料理画像 → 視覚的アピールで言語の壁を解消
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_menu_input_section():
    """メニュー入力セクション"""
    st.markdown("### 🍽️ メニュー情報入力")
    
    state_manager = get_state_manager()
    current_state = state_manager.get_state()
    
    # 新規メニュー追加フォーム
    with st.expander("➕ 新しいメニューを追加", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            # 料理名
            st.markdown("**料理名（日本語）** 💡")
            with st.expander("ヒント: AI翻訳の精度向上", expanded=False):
                st.write("正確な料理名を入力してください。略語や独特な名称の場合は、解説も併記すると翻訳精度が向上します。")
            
            dish_name = st.text_input(
                "",
                placeholder="例: 特製醤油ラーメン",
                key="new_dish_name"
            )
            
            # カテゴリ
            st.markdown("**カテゴリ** 💡")
            with st.expander("ヒント: メニュー整理とナビゲーション", expanded=False):
                st.write("外国人観光客がメニューを探しやすくするためのカテゴリ分けです。")
            
            category = st.selectbox(
                "",
                options=["", "前菜", "メイン", "ご飯・麺", "デザート", "ドリンク", "その他"],
                key="new_category"
            )
        
        with col2:
            # 価格
            st.markdown("**価格（円）** 💡")
            with st.expander("ヒント: 外国人観光客の予算判断", expanded=False):
                st.write("税込価格を入力してください。外国人観光客の予算判断に重要な情報です。")
            
            price = st.number_input(
                "",
                min_value=0,
                step=100,
                key="new_price"
            )
            
            # アレルギー情報
            st.markdown("**アレルギー表示** 💡")
            with st.expander("ヒント: 安心・安全な食事提供", expanded=False):
                st.write("主要なアレルギー成分を選択してください。外国人観光客の安全な食事選択をサポートします。")
            
            allergens = st.multiselect(
                "",
                options=["小麦", "卵", "乳", "そば", "落花生", "えび", "かに", "その他"],
                key="new_allergens"
            )
        
        # 説明文
        st.markdown("**料理説明（日本語）** 💡")
        with st.expander("ヒント: 魅力的な料理紹介", expanded=False):
            st.write("料理の特徴、調理法、使用食材などを簡潔に説明してください。AI翻訳でより魅力的な外国語表示になります。")
        
        description = st.text_area(
            "",
            placeholder="例: 厳選した醤油ダレと自家製麺を使用した当店の看板メニュー。豚骨スープとのバランスが絶妙です。",
            height=80,
            key="new_description"
        )
        
        # 推奨度
        st.markdown("**推奨度（1-5スター）** 💡")
        with st.expander("ヒント: イチオシメニューの判定", expanded=False):
            st.write("1=普通、5=絶対おすすめ。この値は後でメニューの順序最適化とイチオシメニュー選定に使用されます。")
        
        recommendation_level = st.select_slider(
            "",
            options=[1, 2, 3, 4, 5],
            value=3,
            format_func=lambda x: "⭐" * x,
            key="new_recommendation"
        )
        
        # 画像アップロード
        st.markdown("**料理画像** 💡")
        with st.expander("ヒント: 視覚的アピールの重要性", expanded=False):
            st.write("料理の画像は外国人観光客の注文判断に最も重要な要素です。美味しそうな写真をアップロードしてください。")
        
        uploaded_image = st.file_uploader(
            "",
            type=['jpg', 'jpeg', 'png'],
            key="new_menu_image",
            help="※ 推奨サイズ: 1200x800px以上"
        )
        
        # 画像プレビュー
        if uploaded_image:
            col_img1, col_img2 = st.columns(2)
            with col_img1:
                st.image(uploaded_image, caption="アップロード画像", width=200)
            with col_img2:
                # 画像情報表示
                image = Image.open(uploaded_image)
                st.info(f"""
                **画像情報**
                • サイズ: {image.size[0]} x {image.size[1]}px
                • フォーマット: {image.format}
                • ファイル名: {uploaded_image.name}
                """)
        
        # 追加ボタン
        col_add1, col_add2, col_add3 = st.columns([2, 1, 1])
        
        with col_add2:
            if st.button("➕ メニュー追加", type="primary", use_container_width=True):
                if dish_name and category and price > 0:
                    # 新メニューをデータに追加
                    add_menu_item(
                        dish_name, category, price, description, 
                        recommendation_level, allergens, uploaded_image
                    )
                    st.success(f"✅ 「{dish_name}」を追加しました")
                    st.rerun()
                else:
                    st.error("❌ 料理名、カテゴリ、価格は必須項目です\n💡 解決方法: すべての必須項目を入力してから追加してください")
        
        with col_add3:
            if st.button("🗑️ フォームクリア", use_container_width=True):
                # セッション状態をクリア
                for key in ["new_dish_name", "new_category", "new_price", "new_description", "new_recommendation", "new_allergens", "new_menu_image"]:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()

def add_menu_item(dish_name: str, category: str, price: int, description: str, 
                 recommendation_level: int, allergens: List[str], image_file):
    """メニューアイテム追加"""
    state_manager = get_state_manager()
    
    # 画像処理
    image_data = None
    image_filename = None
    
    if image_file:
        try:
            # 画像を読み込み・最適化
            image = Image.open(image_file)
            
            # サイズ調整（最大1200x800）
            max_size = (1200, 800)
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # JPEG形式で保存
            img_buffer = io.BytesIO()
            if image.mode in ("RGBA", "P"):
                image = image.convert("RGB")
            image.save(img_buffer, format="JPEG", quality=85)
            image_data = img_buffer.getvalue()
            
            # ファイル名生成
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            image_filename = f"{dish_name}_{timestamp}.jpg"
            
        except Exception as e:
            logger.error(f"画像処理エラー: {e}")
            st.error(f"画像処理に失敗しました: {e}")
    
    # メニューアイテム作成
    menu_item = {
        "dish_name": dish_name,
        "category": category,
        "price": price,
        "description": description,
        "recommendation_level": recommendation_level,
        "allergens": allergens,
        "image_filename": image_filename,
        "image_data": image_data
    }
    
    # 状態管理に追加
    state_manager.add_menu_item(menu_item)

def render_menu_list():
    """現在のメニューリスト表示"""
    st.markdown("### 📋 現在のメニューリスト")
    
    state_manager = get_state_manager()
    current_state = state_manager.get_state()
    
    if not current_state.menu or len(current_state.menu) == 0:
        st.info("📝 まだメニューが追加されていません。上記フォームから料理を追加してください。")
        return
    
    # カテゴリ別表示
    categories = {}
    for item in current_state.menu:
        category = item.category or "その他"
        if category not in categories:
            categories[category] = []
        categories[category].append(item)
    
    for category, items in categories.items():
        st.markdown(f"#### 🏷️ {category}")
        
        for i, item in enumerate(items):
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                
                with col1:
                    # 料理名・説明
                    st.markdown(f"**{item.dish_name}**")
                    if item.description:
                        st.caption(item.description[:50] + "..." if len(item.description) > 50 else item.description)
                    
                    # アレルギー表示
                    if item.allergens and len(item.allergens) > 0:
                        allergen_text = "、".join(item.allergens)
                        st.caption(f"⚠️ アレルギー: {allergen_text}")
                
                with col2:
                    # 価格・推奨度
                    st.metric("価格", f"¥{item.price:,}")
                    st.caption(f"推奨度: {'⭐' * item.recommendation_level}")
                
                with col3:
                    # 画像表示
                    if item.image_data:
                        try:
                            image = Image.open(io.BytesIO(item.image_data))
                            st.image(image, width=150)
                        except Exception as e:
                            st.caption("画像表示エラー")
                    else:
                        st.caption("📷 画像なし")
                
                with col4:
                    # 編集・削除ボタン
                    if st.button("✏️", key=f"edit_{category}_{i}", help="編集"):
                        edit_menu_item(item, i)
                    
                    if st.button("🗑️", key=f"delete_{category}_{i}", help="削除"):
                        state_manager.delete_menu_item(i)
                        st.success(f"「{item.dish_name}」を削除しました")
                        st.rerun()
                
                st.markdown("---")

def edit_menu_item(item, index: int):
    """メニュー編集モーダル"""
    st.session_state[f'edit_menu_{index}'] = True

def render_bulk_operations():
    """一括操作セクション"""
    st.markdown("### 🔄 一括操作")
    
    state_manager = get_state_manager()
    current_state = state_manager.get_state()
    
    if not current_state.menu or len(current_state.menu) == 0:
        st.info("メニューが登録されていないため、一括操作は利用できません")
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📊 CSV出力", use_container_width=True):
            generate_menu_csv()
    
    with col2:
        if st.button("📋 全メニューコピー", use_container_width=True):
            copy_all_menus()
    
    with col3:
        if st.button("🔄 順序リセット", use_container_width=True):
            reset_menu_order()
    
    with col4:
        if st.button("🗑️ 全削除", use_container_width=True):
            clear_all_menus()

def generate_menu_csv():
    """メニューCSV生成"""
    state_manager = get_state_manager()
    csv_generator = get_csv_generator()
    current_state = state_manager.get_state()
    
    try:
        # 基本メニューCSV生成
        menu_data = []
        for item in current_state.menu:
            menu_data.append({
                "料理名": item.dish_name,
                "カテゴリ": item.category,
                "価格": item.price,
                "説明": item.description,
                "推奨度": item.recommendation_level,
                "アレルギー": "、".join(item.allergens) if item.allergens else ""
            })
        
        csv_content = csv_generator._generate_basic_csv(menu_data, "メニュー情報")
        
        # ダウンロードボタン
        st.download_button(
            label="📥 メニューCSVダウンロード",
            data=csv_content,
            file_name=f"{current_state.store.store_name_ja or 'menu'}_menu.csv",
            mime="text/csv"
        )
        
        st.success("✅ メニューCSVを生成しました")
        
    except Exception as e:
        logger.error(f"CSV生成エラー: {e}")
        st.error("CSV生成に失敗しました")

def copy_all_menus():
    """全メニューをクリップボードにコピー"""
    state_manager = get_state_manager()
    current_state = state_manager.get_state()
    
    menu_text = "【メニュー一覧】\n\n"
    
    for i, item in enumerate(current_state.menu, 1):
        menu_text += f"{i}. {item.dish_name} - ¥{item.price:,}\n"
        if item.description:
            menu_text += f"   {item.description}\n"
        if item.allergens:
            menu_text += f"   アレルギー: {'、'.join(item.allergens)}\n"
        menu_text += "\n"
    
    st.text_area(
        "コピー用テキスト",
        value=menu_text,
        height=200,
        key="menu_copy_text"
    )
    
    st.success("✅ メニューテキストを生成しました。上記をコピーしてください。")

def reset_menu_order():
    """メニュー順序リセット"""
    if st.button("確認: 順序をリセット", type="secondary"):
        state_manager = get_state_manager()
        # 推奨度順でソート
        state_manager.sort_menu_by_recommendation()
        st.success("✅ メニュー順序を推奨度順にリセットしました")
        st.rerun()

def clear_all_menus():
    """全メニュー削除"""
    st.warning("⚠️ この操作は元に戻せません")
    
    if st.button("確認: 全メニューを削除", type="secondary"):
        state_manager = get_state_manager()
        state_manager.clear_all_menus()
        st.success("✅ 全メニューを削除しました")
        st.rerun()

def render_validation_and_navigation():
    """バリデーションとナビゲーション"""
    st.markdown("---")
    
    state_manager = get_state_manager()
    current_state = state_manager.get_state()
    
    # バリデーション
    menu_count = len(current_state.menu) if current_state.menu else 0
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("登録メニュー数", menu_count)
    
    with col2:
        if menu_count > 0:
            avg_price = sum(item.price for item in current_state.menu) / menu_count
            st.metric("平均価格", f"¥{avg_price:.0f}")
        else:
            st.metric("平均価格", "未計算")
    
    with col3:
        if menu_count > 0:
            high_recommend_count = len([item for item in current_state.menu if item.recommendation_level >= 4])
            st.metric("推奨メニュー数", high_recommend_count)
        else:
            st.metric("推奨メニュー数", 0)
    
    # ナビゲーションボタン
    col4, col5, col6 = st.columns([1, 1, 1])
    
    with col4:
        if st.button("← Step2に戻る", use_container_width=True):
            st.switch_page("pages/2_📝_店主ストーリー.py")
    
    with col5:
        if st.button("🏠 ホームに戻る", use_container_width=True):
            st.switch_page("app.py")
    
    with col6:
        can_proceed = state_manager.can_proceed_to_step(4)
        
        if st.button(
            "Step4へ進む →", 
            use_container_width=True, 
            type="primary",
            disabled=not can_proceed
        ):
            if can_proceed:
                state_manager.update_state(current_step=4)
                st.switch_page("pages/4_📊_順序最適化.py")
            else:
                st.error("❌ 最低1つのメニューを登録してください\n💡 解決方法: 上記フォームから料理情報を入力し、メニューを追加してください")

def main():
    """メイン関数"""
    try:
        # ページヘッダー
        st.markdown("# 🍽️ Step3: メニュー情報・料理管理")
        
        # 目的説明
        render_purpose_explanation()
        
        # メニュー入力セクション
        render_menu_input_section()
        
        # 現在のメニューリスト
        render_menu_list()
        
        # 一括操作
        render_bulk_operations()
        
        # バリデーションとナビゲーション
        render_validation_and_navigation()
        
        # 自動保存通知
        state_manager = get_state_manager()
        current_state = state_manager.get_state()
        
        if current_state.menu and len(current_state.menu) > 0:
            st.success("💾 メニュー情報は自動保存されています")
        
    except Exception as e:
        logger.error(f"Step3ページエラー: {e}")
        st.error("ページ表示エラーが発生しました。再読み込みしてください。")
        st.exception(e)

if __name__ == "__main__":
    main()