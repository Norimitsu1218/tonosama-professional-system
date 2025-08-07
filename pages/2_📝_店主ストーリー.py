"""
📝 TONOSAMA Professional System - Step2: 店主ストーリー
1兆円ダイヤモンド級品質の店主想い収集・AI統合システム

帝王（Imperator）による感動的なストーリー生成
"""

import streamlit as st
import asyncio
from modules.state_manager import get_state_manager, initialize_tonosama_ui
from modules.openai_integration import get_openai_integration
import logging

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ページ設定
st.set_page_config(
    page_title="📝 Step2: 店主ストーリー",
    page_icon="📝",
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
            <strong>あなたのお店の「心」を世界に伝える感動的なストーリーを作成します</strong><br>
            • 創業の想い → 外国人観光客の共感と信頼獲得<br>
            • こだわり → 料理の背景ストーリーでブランド価値向上<br>
            • おもてなし → 日本文化の素晴らしさを海外に発信
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_voice_input_guide():
    """音声入力ガイド"""
    st.info("🎤 **スマートフォンのマイクボタンを押して、音声で回答することも可能です。** 質問に答えて、お店の想いを教えてください")

def render_phrase_buttons():
    """定型文ボタン"""
    st.markdown("### 💡 よく使う表現")
    
    phrases = [
        "こだわりの", "伝統的な", "自家製の", "季節の", 
        "厳選した", "心を込めて", "お客様に愛される", "おもてなしの心で"
    ]
    
    cols = st.columns(4)
    for i, phrase in enumerate(phrases):
        with cols[i % 4]:
            if st.button(phrase, key=f"phrase_{i}"):
                st.session_state[f'phrase_selected'] = phrase
                st.success(f"「{phrase}」をコピーしました。テキストボックスに貼り付けてください。")

def render_store_image_upload():
    """店舗代表画像アップロード"""
    st.markdown("### 📸 お店を代表する画像をアップロード")
    
    state_manager = get_state_manager()
    current_state = state_manager.get_state()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**お店の外観・内観・料理など代表的な画像を選択してください**")
        
        uploaded_file = st.file_uploader(
            "",
            type=['jpg', 'jpeg', 'png'],
            key="store_representative_image",
            help="※ 外国人観光客が最初に目にする重要な画像です"
        )
        
        if uploaded_file:
            # 画像をセッション状態に保存
            state_manager.update_state(store_representative_image=uploaded_file)
            st.success("✅ 代表画像をアップロードしました")
    
    with col2:
        # プレビュー表示
        if uploaded_file:
            st.image(uploaded_file, caption="代表画像プレビュー", width=300)
        elif current_state.store_representative_image:
            st.image(current_state.store_representative_image, caption="代表画像プレビュー", width=300)

def render_progress_indicator():
    """進捗インジケーター"""
    state_manager = get_state_manager()
    current_state = state_manager.get_state()
    
    # 回答済み数を計算
    answered_count = len([a for a in current_state.imperator_answers.values() if a and a.strip()])
    total_questions = 15
    
    # プログレスバー
    progress = answered_count / total_questions
    st.progress(progress, text=f"回答済み: {answered_count}/15")
    
    if answered_count >= 10:
        st.success(f"✅ {answered_count}問回答完了！AI統合ストーリー生成が可能です")
    else:
        st.info(f"ℹ️ 最低10問の回答でAI統合ストーリー生成が可能になります（現在: {answered_count}問）")

def render_question_section(question_id: int, title: str, question_text: str, placeholder: str, color: str):
    """質問セクション表示"""
    state_manager = get_state_manager()
    current_state = state_manager.get_state()
    
    st.markdown(f"""
    <div style="background: #1f2937; padding: 20px; border-radius: 12px; border-left: 4px solid {color}; margin-bottom: 25px;">
        <h3 style="color: {color}; margin-bottom: 15px;">{title}</h3>
        <label style="display: block; font-weight: bold; margin-bottom: 8px;">{question_text}</label>
    </div>
    """, unsafe_allow_html=True)
    
    # 回答入力
    answer_key = f"q{question_id}"
    current_answer = current_state.imperator_answers.get(answer_key, "")
    
    answer = st.text_area(
        "",
        value=current_answer,
        placeholder=placeholder,
        height=120,
        key=f"imperator_answer_{question_id}"
    )
    
    # 回答が変更された場合、状態を更新
    if answer != current_answer:
        state_manager.update_imperator_answer(answer_key, answer)
        st.rerun()

def render_all_questions():
    """全15問表示"""
    questions_data = [
        {
            "title": "🌋 0. 創業当時のご自身を振り返って",
            "question": "創業当時、一番ご苦労されたことは何でしたか？どのような困難を乗り越え、どのようなお気持ちで続けてこられたのでしょうか？",
            "placeholder": "回答例: 開業当初は資金繰りが一番の悩みでした。看板も出せず、ほとんど宣伝もできなかったので、最初の3ヶ月はお客様が一桁の日もありました。ただ、その中でも「美味しい」と言ってくれた一人一人の声が支えになりました。必死に厨房に立ち、ひと皿ひと皿に全力を込めました。",
            "color": "#f59e0b"
        },
        {
            "title": "🏪 1. お店の名前の由来",
            "question": "お店の名前には、どのような想いや由来が込められておりますか？",
            "placeholder": "回答例: 「結び庵（むすびあん）」という名前には、「人と人、食と心を結ぶ場所にしたい」という想いを込めました。ご縁を大切にし、ここで出会ったお客様が心安らぐひと時を過ごしていただければと願っています。",
            "color": "#22c55e"
        },
        {
            "title": "🔄 2. 開業以来の変化",
            "question": "開業以来、ご自身で「変わったな」と感じることはございますか？",
            "placeholder": "回答例: 昔は料理の腕一本で勝負する気持ちが強かったのですが、今は「人をもてなす」ことの意味を深く実感しています。お客様の笑顔に心が動くようになりました。",
            "color": "#22c55e"
        },
        {
            "title": "📍 3. この場所を選んだ理由",
            "question": "この場所をお選びになった理由があれば、お聞かせいただけますか？",
            "placeholder": "回答例: もともとこの商店街の空気が好きで、「いつかここで店を出したい」と思っていました。昔ながらの風情が残り、常連さんとの距離も近く、人情に溢れた場所だったからです。",
            "color": "#22c55e"
        },
        {
            "title": "🚀 4. お店を始められたきっかけ",
            "question": "そもそもこのお店を始められた「きっかけ」は何だったのでしょうか？あの時「やろう」と決められたご自身に、今ならどのような言葉をかけてあげたいですか？",
            "placeholder": "回答例: 母の味を残したくて、思い切って始めました。あの頃は不安しかありませんでしたが、「信じてくれてありがとう。ちゃんと続けてるぞ」と伝えたいです。",
            "color": "#3b82f6"
        },
        {
            "title": "💝 5. お客様にお伝えしたいこと",
            "question": "お店を通して、「これだけはお客様にお伝えしたい」と思っておられることは何でしょうか？",
            "placeholder": "回答例: 「食べることは生きること」。美味しさの奥にある、誰かの手間や優しさを感じてもらいたいと思っています。安心して食べられる空間と、心に残る味を大切にしています。",
            "color": "#3b82f6"
        },
        {
            "title": "😊 6. 最も嬉しい瞬間",
            "question": "お客様が帰られる際、どのような表情であれば「今日もやって良かった」と感じられますか？",
            "placeholder": "回答例: ほっとした顔、満たされた顔、それから「また来るね」と言っていただけると心から報われます。食後の笑顔こそが、私たちのやりがいです。",
            "color": "#3b82f6"
        },
        {
            "title": "🍽️ 7. 看板料理のストーリー",
            "question": "お店の看板とも言える一品と、その料理に込められたストーリーを教えていただけますか？",
            "placeholder": "回答例: 「鯛茶漬け」です。母が毎週日曜日に作ってくれた味を、丁寧に再現しています。出汁や胡麻ダレにもこだわり、「家族の温かさ」が伝わるように仕上げています。",
            "color": "#10b981"
        },
        {
            "title": "⚖️ 8. 譲れない軸",
            "question": "メニューを考える際、特に大切にしていること・譲れない軸はございますか？",
            "placeholder": "回答例: 「旬であること」と「嘘のない味」です。奇をてらうよりも、素材の力と正直な調理法で勝負したい。食べてくださる人の顔を思い浮かべながら考えます。",
            "color": "#10b981"
        },
        {
            "title": "🌍 9. 海外からのお客様へ",
            "question": "外国からのお客様には、どのような体験を持ち帰っていただきたいとお考えですか？",
            "placeholder": "回答例: 「まるで誰かの家でご飯をいただいたような温かい気持ち」を持ち帰っていただけたら嬉しいです。日本のもてなしの心を感じていただけたら本望です。",
            "color": "#8b5cf6"
        },
        {
            "title": "🗾 10. 日本らしさ",
            "question": "あなたが最も伝えたい「日本らしさ」や、文化的な要素があれば教えてください。",
            "placeholder": "回答例: 「四季を味わう」こと、日本人が大切にしている感性だと思っています。その季節にしか味わえない料理を通して、自然とのつながりを感じてほしいです。",
            "color": "#8b5cf6"
        },
        {
            "title": "🌎 11. 世界への一言",
            "question": "世界中の方々に向けて、お店や料理を一言でご紹介するとしたら、どのような言葉になりますか？",
            "placeholder": "回答例: 「ようこそ、日本の心が宿る食卓へ。」",
            "color": "#8b5cf6"
        },
        {
            "title": "🏛️ 12. これからの場所像",
            "question": "このお店を、これからどのような場所にしていきたいとお考えでしょうか？",
            "placeholder": "回答例: 世代や国籍を超えて、誰もが安心して立ち寄れる「街の止まり木」のような場所にしたいです。地域とも連携しながら、あたたかい交流の場を育てていきたいです。",
            "color": "#f59e0b"
        },
        {
            "title": "🔮 13. 5-10年後の理想",
            "question": "5年後・10年後、「この道を選んで良かった」と思える未来は、どのような姿でしょうか？",
            "placeholder": "回答例: 「あの味、あのお店、まだ続いてるね」と言ってもらえること。長く続けることが信頼に繋がると信じているので、10年後もブレずにここにいたいです。",
            "color": "#f59e0b"
        },
        {
            "title": "🙏 14. お客様への感謝",
            "question": "これまでお越しいただいたすべてのお客様に対して、いま改めてお伝えになりたい一言があれば、ぜひお聞かせください。",
            "placeholder": "回答例: 「来てくださって、本当にありがとうございました。皆さまのおかげで、今日も暖簾を掲げることができています。」",
            "color": "#f59e0b"
        }
    ]
    
    for i, q_data in enumerate(questions_data):
        render_question_section(
            i, q_data["title"], q_data["question"], 
            q_data["placeholder"], q_data["color"]
        )

def render_ai_story_generation():
    """AI統合ストーリー生成セクション"""
    st.markdown("### 🤖 AI統合ストーリー生成")
    
    state_manager = get_state_manager()
    current_state = state_manager.get_state()
    
    # 回答数チェック
    answered_count = len([a for a in current_state.imperator_answers.values() if a and a.strip()])
    
    col1, col2 = st.columns(2)
    
    with col1:
        # ストーリー生成ボタン
        can_generate = answered_count >= 10
        
        if st.button(
            "🏮 300字以上の統合ストーリーを生成",
            disabled=not can_generate,
            type="primary",
            use_container_width=True
        ):
            if can_generate:
                generate_story_async()
            else:
                st.error(f"❌ 最低10問は回答してから生成してください\n💡 解決方法: Step2の15問のうち最低10問以上に回答を入力してください。音声入力も可能です")
    
    with col2:
        st.info(f"現在の回答数: {answered_count}/15問\n最低10問で生成可能")
    
    # 生成されたストーリー表示・編集
    story_text = st.text_area(
        "生成されたストーリー（編集可能）",
        value=current_state.imperator_story,
        height=200,
        placeholder="15問の回答からAIが統合した店主の想いが表示されます...",
        key="imperator_story_display"
    )
    
    # ストーリーが変更された場合、状態を更新
    if story_text != current_state.imperator_story:
        state_manager.update_state(imperator_story=story_text)
    
    # 品質チェック
    if story_text:
        story_length = len(story_text)
        keywords = ['想い', '心', '料理', 'お客様', '食材', '味', '技術', '伝統', '感謝', '笑顔']
        found_keywords = [k for k in keywords if k in story_text]
        
        col3, col4 = st.columns(2)
        
        with col3:
            if story_length >= 300 and len(found_keywords) >= 3:
                st.success(f"✅ 品質OK: {story_length}字、キーワード{len(found_keywords)}個")
            else:
                st.warning(f"⚠️ 品質要改善: {story_length}字（300字以上必要）、キーワード{len(found_keywords)}個")
        
        with col4:
            # 承認ボタン
            can_approve = story_length >= 300
            
            if st.button(
                "✅ 店主承認（300字以上必須）",
                disabled=not can_approve,
                type="secondary" if can_approve else "secondary"
            ):
                if can_approve:
                    state_manager.set_story_approved(story_text)
                    st.success("🎉 ストーリーを店主承認しました！これで14言語食レポ生成が可能になります")
                    st.rerun()
                else:
                    st.error("❌ 300字以上のストーリーが必要です\n💡 解決方法: ストーリー欄を編集して300字以上になるよう内容を追加してください")
    
    # 承認状況表示
    if current_state.story_approved:
        st.success(f"✅ 承認済み - 承認日時: {current_state.story_approved_at[:19]}")
    else:
        st.info("未承認 - 300字以上のストーリーを作成し、承認してください")

def generate_story_async():
    """非同期ストーリー生成"""
    async def generate():
        state_manager = get_state_manager()
        openai_integration = get_openai_integration()
        current_state = state_manager.get_state()
        
        try:
            with st.spinner("🤖 Imperator式統合ストーリーを生成中..."):
                # 店舗情報を辞書形式で準備
                store_info = {
                    'store_name_ja': current_state.store.store_name_ja,
                    'store_type': current_state.store.store_type
                }
                
                # AI生成実行
                story = await openai_integration.generate_story(
                    current_state.imperator_answers, 
                    store_info
                )
                
                # 状態更新
                state_manager.update_state(imperator_story=story)
                
                st.success("✨ 統合ストーリーを生成しました！内容を確認し承認してください")
                st.rerun()
                
        except Exception as e:
            logger.error(f"ストーリー生成エラー: {e}")
            st.error("❌ ストーリー生成に失敗しました")
    
    # 非同期実行
    try:
        asyncio.run(generate())
    except Exception as e:
        logger.error(f"非同期実行エラー: {e}")
        st.error("システムエラーが発生しました")

def render_validation_and_navigation():
    """バリデーションとナビゲーション"""
    st.markdown("---")
    
    state_manager = get_state_manager()
    current_state = state_manager.get_state()
    
    # 進捗メトリクス
    col1, col2, col3 = st.columns(3)
    
    with col1:
        answered_count = len([a for a in current_state.imperator_answers.values() if a and a.strip()])
        st.metric("回答数", f"{answered_count}/15")
    
    with col2:
        story_length = len(current_state.imperator_story) if current_state.imperator_story else 0
        st.metric("ストーリー文字数", story_length)
    
    with col3:
        st.metric("承認状況", "済" if current_state.story_approved else "未")
    
    # ナビゲーションボタン
    col4, col5, col6 = st.columns([1, 1, 1])
    
    with col4:
        if st.button("← Step1に戻る", use_container_width=True):
            st.switch_page("pages/1_🏪_店舗基本情報.py")
    
    with col5:
        if st.button("🏠 ホームに戻る", use_container_width=True):
            st.switch_page("app.py")
    
    with col6:
        can_proceed = state_manager.can_proceed_to_step(3)
        
        if st.button(
            "Step3へ進む →", 
            use_container_width=True, 
            type="primary",
            disabled=not can_proceed
        ):
            if can_proceed:
                state_manager.update_state(current_step=3)
                st.switch_page("pages/3_🍽️_メニュー情報.py")
            else:
                st.error("❌ 店主ストーリーを承認してください\n💡 解決方法: Step2で15問回答→ストーリー生成→店主承認を完了してください")

def main():
    """メイン関数"""
    try:
        
        # UI初期化（緊急対応）
        initialize_tonosama_ui()
        # ページヘッダー
        st.markdown("# 📝 Step2: 店主ストーリー・15問インタビュー")
        
        # 目的説明
        render_purpose_explanation()
        
        # 音声入力ガイド
        render_voice_input_guide()
        
        # 定型文ボタン
        render_phrase_buttons()
        
        # 店舗代表画像アップロード
        render_store_image_upload()
        
        # 進捗インジケーター
        render_progress_indicator()
        
        # 15問表示
        render_all_questions()
        
        # AI統合ストーリー生成
        render_ai_story_generation()
        
        # バリデーションとナビゲーション
        render_validation_and_navigation()
        
        # 自動保存通知
        st.success("💾 回答内容は自動保存されています")
        
    except Exception as e:
        logger.error(f"Step2ページエラー: {e}")
        st.error("ページ表示エラーが発生しました。再読み込みしてください。")
        st.exception(e)

if __name__ == "__main__":
    main()