"""
🏪 TONOSAMA Professional System - Step1: 店舗基本情報
1兆円ダイヤモンド級品質の店舗情報管理システム

外国人観光客が安心して来店できる基本情報を完璧に収集
"""

import streamlit as st
from modules.state_manager import get_state_manager, initialize_tonosama_ui
import logging

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ページ設定
st.set_page_config(
    page_title="🏪 Step1: 店舗基本情報",
    page_icon="🏪",
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
            <strong>外国人観光客が安心して来店できる基本情報を収集します</strong><br>
            • 店名・業種 → AI翻訳とメニュー生成の精度向上<br>
            • アクセス情報 → Googleマップ連携と道案内<br>
            • 設備情報 → 車椅子・ハラール・アレルギー対応の事前案内
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_hint_button(hint_text: str, key: str):
    """ヒントボタン表示"""
    if st.button("💡", key=f"hint_{key}", help=hint_text):
        st.info(f"💡 **ヒント**: {hint_text}")

def render_basic_info_section():
    """基本情報セクション"""
    st.markdown("### 🏪 基本情報")
    
    try:
        state_manager = get_state_manager()
        current_state = state_manager.get_state()
    except Exception as e:
        st.error(f"状態取得エラー: {e}")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 店舗名（日本語）
        st.markdown("**店舗名（日本語）** 💡")
        with st.expander("ヒント: 店舗の正式名称", expanded=False):
            st.write("店舗の正式名称を入力してください。略称ではなくお客様に表示される名前を記入してください。")
        
        store_name_ja = st.text_input(
            "",
            value=current_state.store.store_name_ja,
            placeholder="例: 旬彩和膳 たかはし",
            key="store_name_ja"
        )
        
        if store_name_ja != current_state.store.store_name_ja:
            state_manager.update_store_info(store_name_ja=store_name_ja)
    
    with col2:
        # 店舗名（ローマ字）
        st.markdown("**店舗名（ローマ字）** 💡")
        with st.expander("ヒント: 外国人観光客向けの表示名", expanded=False):
            st.write("外国人観光客向けの表示名です。Google翻訳でも構いません。例: Takahashi → タカハシ")
        
        store_name_romaji = st.text_input(
            "",
            value=current_state.store.store_name_romaji,
            placeholder="例: Shunsai Wazen Takahashi",
            key="store_name_romaji"
        )
        
        if store_name_romaji != current_state.store.store_name_romaji:
            state_manager.update_store_info(store_name_romaji=store_name_romaji)
    
    col3, col4 = st.columns(2)
    
    with col3:
        # 業種
        st.markdown("**業種** 💡")
        with st.expander("ヒント: AI翻訳の精度向上に重要", expanded=False):
            st.write("お店の料理ジャンルを選択。「その他」の場合は後で詳しく教えてください。")
        
        store_type = st.selectbox(
            "",
            options=["", "和食", "寿司", "ラーメン", "焼き鳥", "居酒屋", "天ぷら", "その他"],
            index=0 if not current_state.store.store_type else ["", "和食", "寿司", "ラーメン", "焼き鳥", "居酒屋", "天ぷら", "その他"].index(current_state.store.store_type) if current_state.store.store_type in ["", "和食", "寿司", "ラーメン", "焼き鳥", "居酒屋", "天ぷら", "その他"] else 0,
            key="store_type"
        )
        
        if store_type != current_state.store.store_type:
            state_manager.update_store_info(store_type=store_type)
    
    with col4:
        # 価格帯
        st.markdown("**価格帯** 💡")
        with st.expander("ヒント: 外国人観光客の予算選択に重要", expanded=False):
            st.write("主力メニューの平均的な価格帯を選択してください。外国人観光客の予算選択に重要です。")
        
        price_band = st.selectbox(
            "",
            options=["", "リーズナブル(1000円以下)", "標準(1000-3000円)", "高級(3000円以上)"],
            index=0 if not current_state.store.price_band else ["", "リーズナブル(1000円以下)", "標準(1000-3000円)", "高級(3000円以上)"].index(current_state.store.price_band) if current_state.store.price_band in ["", "リーズナブル(1000円以下)", "標準(1000-3000円)", "高級(3000円以上)"] else 0,
            key="price_band"
        )
        
        if price_band != current_state.store.price_band:
            state_manager.update_store_info(price_band=price_band)

def render_contact_info_section():
    """連絡先情報セクション"""
    st.markdown("### 📞 連絡先・WEB情報")
    
    try:
        state_manager = get_state_manager()
        current_state = state_manager.get_state()
    except Exception as e:
        st.error(f"状態取得エラー: {e}")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 住所
        st.markdown("**住所** 💡")
        with st.expander("ヒント: Googleマップ連携", expanded=False):
            st.write("お店の所在地を正確に記入してください。郵便番号から記載すると外国人観光客がGoogleマップで検索しやすくなります。")
        
        address = st.text_input(
            "",
            value=current_state.store.address,
            placeholder="〒123-4567 東京都千代田区...",
            key="address"
        )
        
        if address != current_state.store.address:
            state_manager.update_store_info(address=address)
    
    with col2:
        # 電話番号
        st.markdown("**電話番号（+81形式推奨）** 💡")
        with st.expander("ヒント: 国際電話対応", expanded=False):
            st.write("海外からかける場合「+81」が必要です。例: +81-3-1234-5678 (03-1234-5678の場合)")
        
        tel = st.text_input(
            "",
            value=current_state.store.tel,
            placeholder="+81-3-1234-5678",
            key="tel"
        )
        
        if tel != current_state.store.tel:
            state_manager.update_store_info(tel=tel)
    
    # WEB情報
    col3, col4 = st.columns(2)
    
    with col3:
        # ウェブサイト
        st.markdown("**ウェブサイト** 💡")
        with st.expander("ヒント: 外国人観光客へのWEB情報提供", expanded=False):
            st.write("お店の公式サイトがあれば入力してください。食べログやぐるなび等でも構いません。なければ空欄でOKです。")
        
        website = st.text_input(
            "",
            value=current_state.store.website,
            placeholder="https://example.com",
            key="website"
        )
        
        if website != current_state.store.website:
            state_manager.update_store_info(website=website)
    
    with col4:
        # メールアドレス
        st.markdown("**メールアドレス（請求書・領収書送信用）** 💡")
        with st.expander("ヒント: 有料プランの請求書送信", expanded=False):
            st.write("有料プランの場合、このアドレスに請求書と領収書を送信します。お店の正式なメールアドレスを記入してください。")
        
        email = st.text_input(
            "",
            value=current_state.store.email,
            placeholder="restaurant@example.com",
            key="email"
        )
        
        if email != current_state.store.email:
            state_manager.update_store_info(email=email)
    
    # SNS情報
    col5, col6 = st.columns(2)
    
    with col5:
        # Instagram
        st.markdown("**Instagram** 💡")
        with st.expander("ヒント: 料理写真による視覚的アピール", expanded=False):
            st.write("お店のInstagramがあれば入力してください。料理写真は外国人観光客の来店判断に重要な要素です。")
        
        instagram = st.text_input(
            "",
            value=current_state.store.instagram,
            placeholder="https://instagram.com/...",
            key="instagram"
        )
        
        if instagram != current_state.store.instagram:
            state_manager.update_store_info(instagram=instagram)
    
    with col6:
        # Facebook
        st.markdown("**Facebook** 💡")
        with st.expander("ヒント: 海外SNSでの情報発信", expanded=False):
            st.write("お店のFacebookページがあれば入力してください。多くの外国人観光客がFacebookで情報収集します。")
        
        facebook = st.text_input(
            "",
            value=current_state.store.facebook,
            placeholder="https://facebook.com/...",
            key="facebook"
        )
        
        if facebook != current_state.store.facebook:
            state_manager.update_store_info(facebook=facebook)

def render_access_info_section():
    """アクセス情報セクション"""
    st.markdown("### 📍 アクセス・営業時間情報")
    
    try:
        state_manager = get_state_manager()
        current_state = state_manager.get_state()
    except Exception as e:
        st.error(f"状態取得エラー: {e}")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 最寄り駅
        st.markdown("**最寄り駅（日英併記）/ 路線名** 💡")
        with st.expander("ヒント: 外国人観光客の電車利用", expanded=False):
            st.write("外国人観光客が電車で来店する際の重要情報です。駅名を英語併記し、路線名も記載してください。")
        
        nearest_station = st.text_input(
            "",
            value=current_state.store.nearest_station,
            placeholder="例: 新宿駅 (Shinjuku Station) / 山手線",
            key="nearest_station"
        )
        
        if nearest_station != current_state.store.nearest_station:
            state_manager.update_store_info(nearest_station=nearest_station)
    
    with col2:
        # 徒歩時間
        st.markdown("**徒歩時間（分）** 💡")
        with st.expander("ヒント: 実際の歩行時間", expanded=False):
            st.write("駅から店舗まで実際に歩いた場合の時間を分単位で入力してください。目安時間は外国人観光客の計画立てに重要です。")
        
        walk_time = st.number_input(
            "",
            min_value=0,
            value=int(current_state.store.walk_time) if current_state.store.walk_time else 0,
            key="walk_time"
        )
        
        if str(walk_time) != current_state.store.walk_time:
            state_manager.update_store_info(walk_time=str(walk_time))
    
    # 詳しいアクセス方法
    st.markdown("**詳しいアクセス方法** 💡")
    with st.expander("ヒント: 外国人観光客向けの詳細案内", expanded=False):
        st.write("外国人観光客向けに分かりやすく道順を説明してください。出口名、目印となる建物、階段・エスカレーターの有無など具体的に記載。")
    
    access_detail = st.text_area(
        "",
        value=current_state.store.access_detail,
        placeholder="改札口、道順、目印、階段の有無など",
        height=100,
        key="access_detail"
    )
    
    if access_detail != current_state.store.access_detail:
        state_manager.update_store_info(access_detail=access_detail)
    
    # 営業情報
    col3, col4 = st.columns(2)
    
    with col3:
        # 営業時間
        st.markdown("**営業時間** 💡")
        with st.expander("ヒント: 24時間表記推奨", expanded=False):
            st.write("営業時間を24時間表記で記入してください。ランチとディナーが分かれている場合は両方記載してください。")
        
        if st.button("📋 標準設定", key="business_template"):
            state_manager.update_store_info(open_hours="11:30-14:00, 17:30-22:00")
            st.rerun()
        
        open_hours = st.text_input(
            "",
            value=current_state.store.open_hours,
            placeholder="例: 11:30-14:00, 17:30-22:00",
            key="open_hours"
        )
        
        if open_hours != current_state.store.open_hours:
            state_manager.update_store_info(open_hours=open_hours)
    
    with col4:
        # 定休日
        st.markdown("**定休日** 💡")
        with st.expander("ヒント: 外国人観光客の来店計画", expanded=False):
            st.write("毎週の定休日を記入してください。不定休の場合は「不定休」と記載。外国人観光客の来店計画に必要な情報です。")
        
        closed_days = st.text_input(
            "",
            value=current_state.store.closed_days,
            placeholder="例: 月曜日",
            key="closed_days"
        )
        
        if closed_days != current_state.store.closed_days:
            state_manager.update_store_info(closed_days=closed_days)

def render_facility_info_section():
    """設備情報セクション"""
    st.markdown("### ♿ 対応・設備情報（AI処理最適化）")
    st.info("この情報は外国人観光客の事前計画と、AI食レポ生成の精度向上に使用されます")
    
    try:
        state_manager = get_state_manager()
        current_state = state_manager.get_state()
    except Exception as e:
        st.error(f"状態取得エラー: {e}")
        return
    
    # 車椅子対応
    st.markdown("#### 🚪 バリアフリー対応")
    wheelchair = st.radio(
        "車椅子での来店",
        options=["unknown", "available", "partial", "not_available"],
        format_func=lambda x: {
            "unknown": "❓ 不明・未確認",
            "available": "♿ 車椅子対応あり",
            "partial": "🔄 一部対応可能", 
            "not_available": "❌ 車椅子対応なし"
        }[x],
        index=["unknown", "available", "partial", "not_available"].index(current_state.store.wheelchair) if current_state.store.wheelchair else 0,
        key="wheelchair"
    )
    
    if wheelchair != current_state.store.wheelchair:
        state_manager.update_store_info(wheelchair=wheelchair)
    
    # 食事制限対応
    st.markdown("#### 🥗 食事制限対応")
    dietary_restrictions = st.radio(
        "ベジタリアン・ビーガン対応",
        options=["unknown", "full", "limited", "none"],
        format_func=lambda x: {
            "unknown": "❓ 不明・未確認",
            "full": "✅ ビーガン・ベジタリアン対応",
            "limited": "🔄 一部対応可能",
            "none": "❌ 対応メニューなし"
        }[x],
        index=["unknown", "full", "limited", "none"].index(current_state.store.dietary_restrictions) if current_state.store.dietary_restrictions else 0,
        key="dietary_restrictions"
    )
    
    if dietary_restrictions != current_state.store.dietary_restrictions:
        state_manager.update_store_info(dietary_restrictions=dietary_restrictions)
    
    # ハラール対応
    st.markdown("#### 🕌 ハラール対応")
    halal_support = st.radio(
        "ハラール・イスラム教対応",
        options=["unknown", "certified", "friendly", "not_available"],
        format_func=lambda x: {
            "unknown": "❓ 不明・未確認",
            "certified": "🏅 ハラール認証済み",
            "friendly": "🤝 ムスリムフレンドリー",
            "not_available": "❌ 対応なし"
        }[x],
        index=["unknown", "certified", "friendly", "not_available"].index(current_state.store.halal_support) if current_state.store.halal_support else 0,
        key="halal_support"
    )
    
    if halal_support != current_state.store.halal_support:
        state_manager.update_store_info(halal_support=halal_support)
    
    # アレルギー表示
    st.markdown("#### 🏷️ アレルギー情報表示")
    allergy_info = st.radio(
        "アレルギー成分表示",
        options=["unknown", "detailed", "basic", "none"],
        format_func=lambda x: {
            "unknown": "❓ 不明・未確認",
            "detailed": "📋 詳細なアレルギー表示",
            "basic": "📝 基本的なアレルギー情報",
            "none": "❌ アレルギー表示なし"
        }[x],
        index=["unknown", "detailed", "basic", "none"].index(current_state.store.allergy_info) if current_state.store.allergy_info else 0,
        key="allergy_info"
    )
    
    if allergy_info != current_state.store.allergy_info:
        state_manager.update_store_info(allergy_info=allergy_info)

def render_validation_and_navigation():
    """バリデーションとナビゲーション"""
    st.markdown("---")
    
    try:
        state_manager = get_state_manager()
        current_state = state_manager.get_state()
    except Exception as e:
        st.error(f"状態取得エラー: {e}")
        return
    
    # バリデーション
    errors = state_manager.validate_state()
    step1_errors = [e for e in errors if "店舗名" in e or "業種" in e]
    
    if step1_errors:
        st.error("⚠️ 以下の項目を入力してください:")
        for error in step1_errors:
            st.write(f"• {error}")
    else:
        st.success("✅ Step1の必須項目がすべて入力されています！")
    
    # ナビゲーションボタン
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🏠 ホームに戻る", use_container_width=True):
            st.switch_page("app.py")
    
    with col2:
        # 現在の入力状況表示
        completed_fields = 0
        total_fields = 4  # 必須フィールド数
        
        if current_state.store.store_name_ja:
            completed_fields += 1
        if current_state.store.store_type:
            completed_fields += 1
        if current_state.store.address:
            completed_fields += 1
        if current_state.store.tel:
            completed_fields += 1
        
        st.metric(
            label="入力完了", 
            value=f"{completed_fields}/{total_fields}",
            delta=None
        )
    
    with col3:
        can_proceed = state_manager.can_proceed_to_step(2)
        
        if st.button(
            "Step2へ進む →", 
            use_container_width=True, 
            type="primary",
            disabled=not can_proceed
        ):
            if can_proceed:
                state_manager.update_state(current_step=2)
                st.switch_page("pages/2_📝_店主ストーリー.py")
            else:
                st.error("必須項目を入力してからお進みください")

def main():
    """メイン関数"""
    try:
        # UI初期化（緊急対応）
        initialize_tonosama_ui()
        
        # ページヘッダー
        st.markdown("# 🏪 Step1: 店舗基本情報・アクセス登録")
        
        # 状態管理確認
        try:
            state_manager = get_state_manager()
        except Exception as e:
            st.error(f"状態管理エラー: {e}")
            return
        
        if not state_manager:
            st.error("状態管理システムの初期化に失敗しました")
            return
        
        # 目的説明
        render_purpose_explanation()
        
        # 各セクション表示
        render_basic_info_section()
        render_contact_info_section()
        render_access_info_section()
        render_facility_info_section()
        
        # バリデーションとナビゲーション
        render_validation_and_navigation()
        
        # 自動保存通知
        if st.session_state.get("store_name_ja") or st.session_state.get("store_type"):
            st.success("💾 入力内容は自動保存されています")
        
    except Exception as e:
        logger.error(f"Step1ページエラー: {e}")
        st.error("ページ表示エラーが発生しました。再読み込みしてください。")
        st.exception(e)

if __name__ == "__main__":
    main()