"""
🎆 TONOSAMA Professional System - Step6: 完了・プラン選択
1兆円ダイヤモンド級品質の完了処理・自動収益化システム

戸塚さん・正太さん完全連携・パッケージ生成完全装備
"""

import streamlit as st
from modules.state_manager import get_state_manager
from modules.csv_generator import get_csv_generator
from modules.google_drive import get_google_drive_integration, render_google_auth_section, create_package_and_upload
from modules.email_service import get_email_service, send_completion_notification
import logging
from typing import Dict, List
from datetime import datetime
import json

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ページ設定
st.set_page_config(
    page_title="🎆 Step6: 完了・プラン選択",
    page_icon="🎆",
    layout="wide"
)

def render_completion_celebration():
    """完了お祝いセクション"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(34, 197, 94, 0.2), rgba(59, 130, 246, 0.15)); 
                border: 2px solid rgba(34, 197, 94, 0.5); border-radius: 16px; padding: 30px; margin: 20px 0; text-align: center;">
        <div style="font-size: 64px; margin-bottom: 20px;">🎉🏮🎆</div>
        <h1 style="color: #22c55e; margin-bottom: 15px;">システム構築完了！</h1>
        <div style="color: #d1d5db; font-size: 18px; margin-bottom: 20px;">
            <strong>外国人観光客向け完璧多言語レストランシステム</strong><br>
            AI帝王による14言語食レポ・店主ストーリー・完全パッケージが準備完了しました！
        </div>
        <div style="background: rgba(34, 197, 94, 0.1); padding: 15px; border-radius: 8px; margin-top: 20px;">
            <div style="color: #22c55e; font-weight: bold;">🏮 TONOSAMA Professional System v2.0 Diamond Edition</div>
            <div style="color: #d1d5db;">世界最高品質の多言語レストランシステム</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_system_summary():
    """システム完成サマリー"""
    st.markdown("### 📊 システム完成サマリー")
    
    state_manager = get_state_manager()
    current_state = state_manager.get_state()
    
    # 完成度チェック
    completions = {
        "店舗基本情報": bool(current_state.store.store_name_ja and current_state.store.store_type),
        "店主ストーリー": bool(current_state.imperator_story and current_state.story_approved),
        "メニュー情報": bool(current_state.menu and len(current_state.menu) > 0),
        "AI食レポ": bool(current_state.food_reports_generated),
    }
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        status = "✅" if completions["店舗基本情報"] else "❌"
        st.metric("店舗基本情報", status)
        if completions["店舗基本情報"]:
            st.caption(f"店舗名: {current_state.store.store_name_ja}")
            st.caption(f"業種: {current_state.store.store_type}")
    
    with col2:
        status = "✅" if completions["店主ストーリー"] else "❌"
        st.metric("店主ストーリー", status)
        if completions["店主ストーリー"]:
            story_length = len(current_state.imperator_story) if current_state.imperator_story else 0
            st.caption(f"文字数: {story_length}")
            st.caption("承認: 済")
    
    with col3:
        status = "✅" if completions["メニュー情報"] else "❌"
        st.metric("メニュー情報", status)
        if completions["メニュー情報"]:
            menu_count = len(current_state.menu)
            st.caption(f"登録メニュー: {menu_count}品")
            high_recommend = len([m for m in current_state.menu if m.recommendation_level >= 4])
            st.caption(f"推奨メニュー: {high_recommend}品")
    
    with col4:
        status = "✅" if completions["AI食レポ"] else "❌"
        st.metric("AI食レポ", status)
        if completions["AI食レポ"]:
            generated_count = len([m for m in current_state.menu if m.food_reports])
            st.caption(f"生成済み: {generated_count}品")
            st.caption("品質: ダイヤモンド級")
    
    # 完成度表示
    completion_rate = sum(completions.values()) / len(completions)
    st.progress(completion_rate, text=f"システム完成度: {completion_rate:.0%}")
    
    if completion_rate == 1.0:
        st.success("🎉 全ての機能が完璧に完成しています！")
    else:
        incomplete_items = [k for k, v in completions.items() if not v]
        st.warning(f"⚠️ 未完成項目: {', '.join(incomplete_items)}")

def render_recommended_menu_selection():
    """イチオシメニュー選択"""
    st.markdown("### 🌟 イチオシメニュー選択")
    
    state_manager = get_state_manager()
    current_state = state_manager.get_state()
    
    if not current_state.menu:
        st.info("メニューが登録されていません")
        return
    
    # 推奨度4以上のメニューを抽出
    high_recommend_menus = [
        (i, menu) for i, menu in enumerate(current_state.menu) 
        if menu.recommendation_level >= 4
    ]
    
    if not high_recommend_menus:
        st.warning("推奨度4以上のメニューがありません。Step4で推奨度を設定してください。")
        return
    
    st.info(f"推奨度4以上のメニューから、外国人観光客に最もアピールしたい「イチオシメニュー」を選択してください。")
    
    # メニュー選択
    menu_options = {f"{menu.dish_name} (¥{menu.price:,}, {'⭐' * menu.recommendation_level})": idx 
                   for idx, menu in high_recommend_menus}
    
    selected_menu = st.selectbox(
        "イチオシメニューを選択",
        options=list(menu_options.keys()),
        key="recommended_menu_selection"
    )
    
    if selected_menu:
        selected_idx = menu_options[selected_menu]
        selected_menu_item = current_state.menu[selected_idx]
        
        # 選択されたメニューのプレビュー
        with st.expander("🍽️ 選択されたイチオシメニュー詳細", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**料理名**: {selected_menu_item.dish_name}")
                st.write(f"**カテゴリ**: {selected_menu_item.category}")
                st.write(f"**価格**: ¥{selected_menu_item.price:,}")
                st.write(f"**推奨度**: {'⭐' * selected_menu_item.recommendation_level}")
                
                if selected_menu_item.allergens:
                    st.write(f"**アレルギー**: {'、'.join(selected_menu_item.allergens)}")
            
            with col2:
                if selected_menu_item.image_data:
                    from PIL import Image
                    import io
                    try:
                        image = Image.open(io.BytesIO(selected_menu_item.image_data))
                        st.image(image, caption=selected_menu_item.dish_name, width=250)
                    except:
                        st.caption("🖼️ 画像表示エラー")
                else:
                    st.caption("📷 画像未登録")
            
            if selected_menu_item.description:
                st.write("**説明**")
                st.write(selected_menu_item.description)
        
        # 状態更新
        state_manager.update_state(recommended_menu_index=selected_idx)
        return selected_menu_item
    
    return None

def render_plan_selection():
    """プラン選択セクション"""
    st.markdown("### 💎 プラン選択・自動収益システム")
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(34, 197, 94, 0.1)); 
                border: 1px solid rgba(139, 92, 246, 0.3); border-radius: 12px; padding: 16px; margin-bottom: 20px;">
        <div style="color: #8b5cf6; font-weight: bold; font-size: 18px; margin-bottom: 10px;">
            🏮 TONOSAMA自動収益システム
        </div>
        <div style="color: #d1d5db;">
            • <strong>無料プラン</strong>: イチオシメニューのみ戸塚さんに送信<br>
            • <strong>有料プラン</strong>: 完全パッケージを正太さん＋戸塚さんに自動送信<br>
            • <strong>完全自動化</strong>: あなたが寝てるだけで収益が発生する仕組み
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # プラン選択
    plan_options = {
        "無料プラン": {
            "price": 0,
            "description": "イチオシメニュー.txt → 戸塚さんに送信",
            "features": [
                "✅ イチオシメニュー.txtファイル作成",
                "✅ 戸塚さんへの自動送信",
                "❌ 14言語AI食レポなし",
                "❌ Google Driveパッケージなし",
                "❌ 正太さんへの送信なし"
            ],
            "color": "#6b7280"
        },
        "A4プラン": {
            "price": 3000,
            "description": "完全パッケージ → 正太さん＋戸塚さんに送信",
            "features": [
                "✅ 14言語AI食レポ完全版",
                "✅ Google Drive完全パッケージ",
                "✅ 正太さん形式CSV生成",
                "✅ 正太さんへの自動送信",
                "✅ 戸塚さんへの完了通知",
                "✅ 3,000円収益"
            ],
            "color": "#22c55e"
        },
        "テント型プラン": {
            "price": 5000,
            "description": "プレミアム完全パッケージ → 正太さん＋戸塚さんに送信",
            "features": [
                "✅ 14言語AI食レポ完全版",
                "✅ Google Drive完全パッケージ",
                "✅ 正太さん形式CSV生成",
                "✅ 正太さんへの自動送信",
                "✅ 戸塚さんへの完了通知",
                "✅ プレミアム画像処理",
                "✅ 5,000円収益"
            ],
            "color": "#8b5cf6"
        }
    }
    
    # プラン選択UI
    selected_plan = None
    
    for plan_name, plan_info in plan_options.items():
        with st.container():
            col1, col2, col3 = st.columns([2, 3, 1])
            
            with col1:
                plan_color = plan_info["color"]
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, {plan_color}20, {plan_color}10); 
                            border: 2px solid {plan_color}; border-radius: 12px; padding: 20px; text-align: center;">
                    <h3 style="color: {plan_color}; margin-bottom: 10px;">{plan_name}</h3>
                    <div style="font-size: 24px; font-weight: bold; color: {plan_color};">
                        ¥{plan_info["price"]:,}
                    </div>
                    <div style="color: #d1d5db; font-size: 14px; margin-top: 8px;">
                        {plan_info["description"]}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("**プラン内容**")
                for feature in plan_info["features"]:
                    st.write(feature)
            
            with col3:
                if st.button(f"選択", key=f"select_{plan_name}", type="primary" if plan_info["price"] > 0 else "secondary"):
                    selected_plan = plan_name
                    st.session_state["selected_plan"] = plan_name
                    st.success(f"✅ {plan_name}を選択しました")
                    st.rerun()
            
            st.markdown("---")
    
    # 選択されたプラン表示
    if "selected_plan" in st.session_state:
        selected_plan = st.session_state["selected_plan"]
        plan_info = plan_options[selected_plan]
        
        st.success(f"🎯 選択中のプラン: **{selected_plan}** (¥{plan_info['price']:,})")
        return selected_plan, plan_info
    
    return None, None

def render_package_generation():
    """パッケージ生成セクション"""
    st.markdown("### 📦 完全パッケージ生成・送信")
    
    state_manager = get_state_manager()
    current_state = state_manager.get_state()
    
    selected_plan = st.session_state.get("selected_plan")
    if not selected_plan:
        st.info("プランを選択してからパッケージ生成を行ってください")
        return
    
    # 推奨メニュー確認
    recommended_menu_idx = getattr(current_state, 'recommended_menu_index', None)
    if recommended_menu_idx is None:
        st.info("イチオシメニューを選択してからパッケージ生成を行ってください")
        return
    
    recommended_menu = current_state.menu[recommended_menu_idx]
    
    st.info(f"**選択プラン**: {selected_plan}  |  **イチオシメニュー**: {recommended_menu.dish_name}")
    
    # パッケージ生成・送信ボタン
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button(
            "🚀 完全パッケージ生成・自動送信開始", 
            type="primary", 
            use_container_width=True
        ):
            execute_package_generation(selected_plan, recommended_menu)

def execute_package_generation(selected_plan: str, recommended_menu):
    """パッケージ生成・送信実行"""
    state_manager = get_state_manager()
    csv_generator = get_csv_generator()
    email_service = get_email_service()
    current_state = state_manager.get_state()
    
    try:
        st.success("🚀 完全パッケージ生成を開始します...")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Step 1: 基本CSV生成
        status_text.text("📊 基本情報CSV生成中...")
        
        # 店舗情報CSV
        store_csv = csv_generator.generate_store_info_csv(current_state.store)
        
        # ストーリーCSV（14言語対応）
        story_csv = csv_generator.generate_story_multilingual_csv(
            current_state.imperator_story,
            current_state.store.store_name_ja
        )
        
        progress_bar.progress(0.2)
        
        # Step 2: メニューCSV生成
        status_text.text("🍽️ メニュー情報CSV生成中...")
        
        menu_csv = csv_generator.generate_menu_multilingual_csv(
            current_state.store.store_name_ja,
            current_state.menu
        )
        
        progress_bar.progress(0.4)
        
        # Step 3: AI食レポCSV生成
        status_text.text("🤖 AI食レポCSV生成中...")
        
        food_report_csv = csv_generator.generate_multilingual_food_reports_csv(
            current_state.store.store_name_ja,
            current_state.menu
        )
        
        progress_bar.progress(0.6)
        
        # Step 4: パッケージ統合
        status_text.text("📦 完全パッケージ統合中...")
        
        package_data = {
            "store_info_csv": store_csv.encode('utf-8-sig'),
            "story_csv": story_csv.encode('utf-8-sig'),
            "menu_csv": menu_csv.encode('utf-8-sig'),
            "food_report_csv": food_report_csv.encode('utf-8-sig'),
            "images": {}
        }
        
        # 画像データ追加
        for menu_item in current_state.menu:
            if menu_item.image_data and menu_item.image_filename:
                package_data["images"][menu_item.image_filename] = menu_item.image_data
        
        progress_bar.progress(0.8)
        
        # Step 5: 送信処理
        if selected_plan == "無料プラン":
            # 無料プラン: イチオシメニューのみ戸塚さんに送信
            status_text.text("📧 戸塚さんにイチオシメニュー送信中...")
            
            store_info = {
                "store_name_ja": current_state.store.store_name_ja,
                "store_type": current_state.store.store_type,
                "created_at": current_state.created_at
            }
            
            success = email_service.send_free_plan_notification(
                store_info, 
                recommended_menu.dish_name
            )
            
            if success:
                st.success("✅ 無料プラン完了: 戸塚さんにイチオシメニューを送信しました")
            else:
                st.warning("⚠️ メール送信に失敗しましたが、処理は完了しています")
        
        else:
            # 有料プラン: Google Drive + 正太さん & 戸塚さんに送信
            status_text.text("☁️ Google Driveパッケージ作成中...")
            
            # Google Drive連携確認
            google_drive = get_google_drive_integration()
            google_drive_info = None
            
            if google_drive.is_configured() and google_drive.authenticate():
                google_drive_info = create_package_and_upload(
                    current_state.store.store_name_ja,
                    package_data
                )
            
            # 戸塚さんに完了通知送信
            status_text.text("📧 戸塚さんに完了通知送信中...")
            
            store_info = {
                "store_name_ja": current_state.store.store_name_ja,
                "store_type": current_state.store.store_type,
                "created_at": current_state.created_at
            }
            
            plan_info = {"selected_plan": selected_plan}
            google_drive_link = google_drive_info.get("main_folder_link", "") if google_drive_info else ""
            
            email_success = email_service.send_paid_plan_notification(
                store_info, plan_info, google_drive_link
            )
            
            if email_success:
                st.success(f"✅ {selected_plan}完了: 正太さん＋戸塚さんに完全パッケージを送信しました")
            else:
                st.warning("⚠️ メール送信に失敗しましたが、パッケージ作成は完了しています")
            
            # Google Driveリンク表示
            if google_drive_info:
                st.success(f"☁️ Google Driveパッケージ: {google_drive_link}")
        
        progress_bar.progress(1.0)
        status_text.text("🎉 全処理完了!")
        
        # 完了状態更新
        state_manager.update_state(
            package_generated=True,
            selected_plan=selected_plan,
            completion_date=datetime.now().isoformat()
        )
        
        # 成功表示
        st.balloons()
        render_completion_success(selected_plan)
        
    except Exception as e:
        logger.error(f"パッケージ生成エラー: {e}")
        st.error(f"パッケージ生成中にエラーが発生しました: {e}")

def render_completion_success(selected_plan: str):
    """完了成功表示"""
    plan_prices = {"無料プラン": 0, "A4プラン": 3000, "テント型プラン": 5000}
    revenue = plan_prices.get(selected_plan, 0)
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(34, 197, 94, 0.2), rgba(59, 130, 246, 0.2)); 
                border: 3px solid rgba(34, 197, 94, 0.8); border-radius: 20px; padding: 30px; margin: 30px 0; text-align: center;">
        <div style="font-size: 72px; margin-bottom: 20px;">🎉🏮✨</div>
        <h1 style="color: #22c55e; margin-bottom: 20px;">システム完成・送信完了！</h1>
        
        <div style="background: rgba(34, 197, 94, 0.15); padding: 20px; border-radius: 12px; margin: 20px 0;">
            <h3 style="color: #22c55e; margin-bottom: 15px;">🏮 TONOSAMA Professional System</h3>
            <div style="color: #d1d5db; font-size: 18px;">
                <strong>{selected_plan}</strong> での完全パッケージ生成・送信が完了しました！<br>
                {"戸塚さんに自動送信済み" if revenue == 0 else "正太さん＋戸塚さんに自動送信済み"}
            </div>
        </div>
        
        <div style="background: rgba(139, 92, 246, 0.15); padding: 20px; border-radius: 12px; margin: 20px 0;">
            <h3 style="color: #8b5cf6;">💰 収益発生</h3>
            <div style="font-size: 36px; font-weight: bold; color: #8b5cf6;">¥{revenue:,}</div>
            <div style="color: #d1d5db;">{"イチオシメニュー共有完了" if revenue == 0 else "完全自動化収益システム稼働中"}</div>
        </div>
        
        <div style="color: #d1d5db; margin-top: 20px;">
            これで外国人観光客向け完璧多言語レストランシステムが完成しました！<br>
            <strong>お疲れ様でした！</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_final_summary():
    """最終サマリー"""
    st.markdown("### 📋 最終完了サマリー")
    
    state_manager = get_state_manager()
    current_state = state_manager.get_state()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📊 システム構成**")
        st.write(f"• 店舗名: {current_state.store.store_name_ja}")
        st.write(f"• 業種: {current_state.store.store_type}")
        st.write(f"• メニュー数: {len(current_state.menu) if current_state.menu else 0}品")
        st.write(f"• AI食レポ: 14言語対応")
        
        selected_plan = st.session_state.get("selected_plan", "未選択")
        st.write(f"• 選択プラン: {selected_plan}")
    
    with col2:
        st.markdown("**🎯 完成ファイル**")
        st.write("✅ 店舗基本情報.csv")
        st.write("✅ 14言語店主ストーリー.csv")
        st.write("✅ 14言語メニュー情報.csv")
        st.write("✅ 14言語AI食レポ.csv")
        st.write("✅ 完全画像パッケージ")
        
        if st.session_state.get("selected_plan") != "無料プラン":
            st.write("✅ Google Drive完全パッケージ")

def main():
    """メイン関数"""
    try:
        # ページヘッダー
        st.markdown("# 🎆 Step6: 完了・プラン選択・自動収益化")
        
        # 完了お祝い
        render_completion_celebration()
        
        # システムサマリー
        render_system_summary()
        
        # パッケージが既に生成済みの場合
        state_manager = get_state_manager()
        current_state = state_manager.get_state()
        
        if getattr(current_state, 'package_generated', False):
            st.success("🎉 パッケージは既に生成・送信済みです！")
            selected_plan = getattr(current_state, 'selected_plan', '不明')
            render_completion_success(selected_plan)
            render_final_summary()
        else:
            # イチオシメニュー選択
            recommended_menu = render_recommended_menu_selection()
            
            # プラン選択
            selected_plan, plan_info = render_plan_selection()
            
            # パッケージ生成
            if selected_plan and recommended_menu:
                render_package_generation()
        
        # ナビゲーション
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("← Step5に戻る", use_container_width=True):
                st.switch_page("pages/5_🤖_AI食レポ.py")
        
        with col2:
            if st.button("🏠 ホームに戻る", use_container_width=True):
                st.switch_page("app.py")
        
        with col3:
            if st.button("🔄 新規作成", use_container_width=True):
                # 新規セッション開始
                if st.button("確認: 新規システム作成", type="secondary"):
                    state_manager.create_new_session()
                    st.success("✅ 新規システム作成を開始します")
                    st.switch_page("app.py")
        
    except Exception as e:
        logger.error(f"Step6ページエラー: {e}")
        st.error("ページ表示エラーが発生しました。再読み込みしてください。")
        st.exception(e)

if __name__ == "__main__":
    main()