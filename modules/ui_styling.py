"""
🎨 TONOSAMA Professional System - UI Styling
1兆円ダイヤモンド級品質のカスタムCSS・スタイリングシステム

完璧な視覚体験とユーザビリティを実現
"""

import streamlit as st

def inject_diamond_css():
    """ダイヤモンド級カスタムCSS注入"""
    st.markdown("""
    <style>
    /* ==============================================
       🏮 TONOSAMA Diamond Grade Global Styling
       ============================================== */
    
    /* 全体的な背景とテーマ */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f9fafb;
    }
    
    /* メインコンテナ */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* ヘッダースタイル */
    h1 {
        background: linear-gradient(135deg, #22c55e, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        font-weight: bold;
        font-size: 2.5rem;
        margin-bottom: 2rem;
        text-shadow: 0 0 30px rgba(34, 197, 94, 0.3);
    }
    
    h2 {
        color: #22c55e;
        border-bottom: 2px solid #22c55e;
        padding-bottom: 0.5rem;
        margin: 2rem 0 1rem 0;
    }
    
    h3 {
        color: #3b82f6;
        margin: 1.5rem 0 1rem 0;
    }
    
    /* ==============================================
       🌟 Button Styling
       ============================================== */
    
    /* プライマリボタン */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #22c55e, #16a34a);
        border: none;
        border-radius: 12px;
        color: white;
        font-weight: bold;
        padding: 0.75rem 1.5rem;
        box-shadow: 0 10px 25px rgba(34, 197, 94, 0.3);
        transition: all 0.3s ease;
        text-transform: none;
        font-size: 1rem;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #16a34a, #15803d);
        box-shadow: 0 15px 35px rgba(34, 197, 94, 0.4);
        transform: translateY(-2px);
    }
    
    /* セカンダリボタン */
    .stButton > button[kind="secondary"] {
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        border: none;
        border-radius: 12px;
        color: white;
        font-weight: bold;
        padding: 0.75rem 1.5rem;
        box-shadow: 0 10px 25px rgba(59, 130, 246, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
        box-shadow: 0 15px 35px rgba(59, 130, 246, 0.4);
        transform: translateY(-2px);
    }
    
    /* 通常ボタン */
    .stButton > button {
        background: linear-gradient(135deg, #6b7280, #4b5563);
        border: 1px solid #374151;
        border-radius: 8px;
        color: white;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #4b5563, #374151);
        border-color: #22c55e;
        transform: translateY(-1px);
    }
    
    /* ==============================================
       📊 Form Elements
       ============================================== */
    
    /* 入力フィールド */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background-color: #1f2937;
        border: 2px solid #374151;
        border-radius: 8px;
        color: #f9fafb;
        padding: 0.75rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #22c55e;
        box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.1);
        outline: none;
    }
    
    /* セレクトボックス */
    .stSelectbox > div > div {
        background-color: #1f2937;
        border-radius: 8px;
    }
    
    /* マルチセレクト */
    .stMultiSelect > div > div {
        background-color: #1f2937;
        border-radius: 8px;
    }
    
    /* 数値入力 */
    .stNumberInput > div > div > input {
        background-color: #1f2937;
        border: 2px solid #374151;
        border-radius: 8px;
        color: #f9fafb;
    }
    
    /* ==============================================
       📈 Metrics & Progress
       ============================================== */
    
    /* メトリクス */
    .metric-container {
        background: linear-gradient(135deg, rgba(31, 41, 55, 0.8), rgba(17, 24, 39, 0.9));
        border: 1px solid #374151;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        backdrop-filter: blur(10px);
    }
    
    /* プログレスバー */
    .stProgress > div > div > div {
        background: linear-gradient(135deg, #22c55e, #16a34a);
        border-radius: 10px;
    }
    
    /* ==============================================
       🎨 Cards & Containers
       ============================================== */
    
    /* カスタムカード */
    .diamond-card {
        background: linear-gradient(135deg, rgba(31, 41, 55, 0.9), rgba(17, 24, 39, 0.8));
        border: 1px solid rgba(34, 197, 94, 0.3);
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        backdrop-filter: blur(15px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .diamond-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.4);
        border-color: rgba(34, 197, 94, 0.5);
    }
    
    /* 成功メッセージ */
    .element-container .stAlert > div[data-baseweb="notification"] {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.15), rgba(34, 197, 94, 0.05));
        border: 1px solid rgba(34, 197, 94, 0.4);
        border-radius: 12px;
    }
    
    /* 情報メッセージ */
    .element-container .stInfo > div {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(59, 130, 246, 0.05));
        border: 1px solid rgba(59, 130, 246, 0.4);
        border-radius: 12px;
    }
    
    /* 警告メッセージ */
    .element-container .stWarning > div {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.15), rgba(245, 158, 11, 0.05));
        border: 1px solid rgba(245, 158, 11, 0.4);
        border-radius: 12px;
    }
    
    /* エラーメッセージ */
    .element-container .stError > div {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15), rgba(239, 68, 68, 0.05));
        border: 1px solid rgba(239, 68, 68, 0.4);
        border-radius: 12px;
    }
    
    /* ==============================================
       🎯 Navigation & Sidebar
       ============================================== */
    
    /* サイドバー */
    .css-1d391kg {
        background: linear-gradient(180deg, #111827 0%, #1f2937 100%);
        border-right: 1px solid #374151;
    }
    
    /* サイドバーナビゲーション */
    .css-17lntkn {
        color: #f9fafb;
        font-weight: 500;
    }
    
    .css-17lntkn:hover {
        color: #22c55e;
        background: rgba(34, 197, 94, 0.1);
        border-radius: 8px;
    }
    
    /* ==============================================
       📊 Data Display
       ============================================== */
    
    /* データフレーム */
    .stDataFrame {
        background: rgba(31, 41, 55, 0.8);
        border-radius: 12px;
        overflow: hidden;
        backdrop-filter: blur(10px);
    }
    
    /* テーブル */
    .stTable {
        background: rgba(31, 41, 55, 0.8);
        border-radius: 12px;
    }
    
    /* ==============================================
       🎨 Special Effects
       ============================================== */
    
    /* グロー効果 */
    .glow {
        box-shadow: 0 0 20px rgba(34, 197, 94, 0.4);
    }
    
    /* パルス効果 */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    /* フェードイン効果 */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }
    
    /* ==============================================
       🏮 TONOSAMA Brand Elements
       ============================================== */
    
    /* ブランドカラー */
    .tonosama-primary {
        color: #22c55e;
    }
    
    .tonosama-secondary {
        color: #3b82f6;
    }
    
    .tonosama-accent {
        color: #8b5cf6;
    }
    
    /* ダイヤモンドグラデーション */
    .diamond-gradient {
        background: linear-gradient(135deg, #22c55e, #3b82f6, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* ==============================================
       📱 Responsive Design
       ============================================== */
    
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
        }
        
        h1 {
            font-size: 2rem;
        }
        
        .diamond-card {
            padding: 1rem;
        }
    }
    
    /* ==============================================
       🎯 File Uploader
       ============================================== */
    
    .stFileUploader > section {
        background: linear-gradient(135deg, rgba(31, 41, 55, 0.8), rgba(17, 24, 39, 0.9));
        border: 2px dashed #22c55e;
        border-radius: 12px;
        padding: 2rem;
        transition: all 0.3s ease;
    }
    
    .stFileUploader > section:hover {
        border-color: #16a34a;
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.05), rgba(31, 41, 55, 0.9));
    }
    
    /* ==============================================
       🌟 Loading & Spinner
       ============================================== */
    
    .stSpinner > div {
        border-top-color: #22c55e;
        border-right-color: #3b82f6;
        border-bottom-color: #8b5cf6;
        border-left-color: transparent;
    }
    
    /* ==============================================
       🎨 Custom Scrollbar
       ============================================== */
    
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1f2937;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #22c55e, #16a34a);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #16a34a, #15803d);
    }
    
    /* ==============================================
       🏮 Footer Branding
       ============================================== */
    
    .tonosama-footer {
        text-align: center;
        padding: 2rem;
        border-top: 1px solid #374151;
        margin-top: 3rem;
        background: linear-gradient(135deg, rgba(17, 24, 39, 0.9), rgba(31, 41, 55, 0.8));
    }
    
    .tonosama-footer .diamond-gradient {
        font-weight: bold;
        font-size: 1.1rem;
    }
    </style>
    """, unsafe_allow_html=True)

def render_tonosama_header():
    """TONOSAMA ヘッダー表示"""
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🏮</div>
        <div class="diamond-gradient" style="font-size: 2.5rem; font-weight: bold; margin-bottom: 0.5rem;">
            TONOSAMA Professional System
        </div>
        <div style="color: #8b5cf6; font-size: 1.2rem; font-weight: 500;">
            1兆円ダイヤモンド級品質 - v2.0 Diamond Edition
        </div>
        <div style="color: #6b7280; margin-top: 0.5rem;">
            外国人観光客向け完璧多言語レストランシステム
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_diamond_divider():
    """ダイヤモンド級区切り線"""
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <div style="height: 2px; background: linear-gradient(135deg, transparent, #22c55e, #3b82f6, #8b5cf6, transparent); margin: 1rem 0;"></div>
        <div style="color: #22c55e; font-size: 1.5rem;">💎</div>
        <div style="height: 2px; background: linear-gradient(135deg, transparent, #8b5cf6, #3b82f6, #22c55e, transparent); margin: 1rem 0;"></div>
    </div>
    """, unsafe_allow_html=True)

def render_success_celebration(title: str, message: str):
    """成功お祝い表示"""
    st.markdown(f"""
    <div class="diamond-card glow fade-in" style="text-align: center; border-color: #22c55e;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🎉✨🏮</div>
        <h2 style="color: #22c55e; margin-bottom: 1rem;">{title}</h2>
        <div style="color: #d1d5db; font-size: 1.1rem;">
            {message}
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_step_progress(current_step: int, total_steps: int = 6):
    """ステップ進捗表示"""
    progress_items = []
    
    for i in range(1, total_steps + 1):
        if i < current_step:
            # 完了済み
            status = "✅"
            color = "#22c55e"
        elif i == current_step:
            # 現在のステップ
            status = "🔄"
            color = "#3b82f6"
        else:
            # 未実施
            status = "⭕"
            color = "#6b7280"
        
        progress_items.append(f'<span style="color: {color}; font-size: 1.5rem; margin: 0 0.5rem;">{status}</span>')
    
    progress_html = ''.join(progress_items)
    
    st.markdown(f"""
    <div style="text-align: center; margin: 2rem 0; padding: 1rem; background: rgba(31, 41, 55, 0.8); border-radius: 12px;">
        <div style="color: #d1d5db; margin-bottom: 0.5rem;">進捗状況</div>
        <div>{progress_html}</div>
        <div style="color: #8b5cf6; margin-top: 0.5rem;">Step {current_step} / {total_steps}</div>
    </div>
    """, unsafe_allow_html=True)

def render_quality_badge():
    """品質バッジ表示"""
    st.markdown("""
    <div style="position: fixed; top: 20px; right: 20px; z-index: 1000;">
        <div style="background: linear-gradient(135deg, #22c55e, #16a34a); color: white; padding: 0.5rem 1rem; border-radius: 25px; font-weight: bold; font-size: 0.9rem; box-shadow: 0 10px 25px rgba(34, 197, 94, 0.3);">
            💎 Diamond Grade
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_tonosama_footer():
    """TONOSAMA フッター"""
    st.markdown("""
    <div class="tonosama-footer">
        <div class="diamond-gradient">🏮 TONOSAMA Professional System v2.0</div>
        <div style="color: #6b7280; margin-top: 0.5rem;">
            1兆円ダイヤモンド級品質 | 外国人観光客向け完璧多言語レストランシステム
        </div>
        <div style="color: #4b5563; margin-top: 1rem; font-size: 0.9rem;">
            © 2024 TONOSAMA Professional - All Rights Reserved
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_loading_screen(message: str = "システム初期化中..."):
    """ローディング画面"""
    st.markdown(f"""
    <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(15, 23, 42, 0.95); display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 9999;">
        <div style="font-size: 4rem; margin-bottom: 2rem; animation: pulse 2s infinite;">🏮</div>
        <div class="diamond-gradient" style="font-size: 2rem; font-weight: bold; margin-bottom: 1rem;">
            TONOSAMA Professional
        </div>
        <div style="color: #22c55e; font-size: 1.2rem; margin-bottom: 2rem;">
            {message}
        </div>
        <div class="pulse" style="width: 200px; height: 4px; background: linear-gradient(135deg, #22c55e, #3b82f6, #8b5cf6); border-radius: 2px;"></div>
    </div>
    """, unsafe_allow_html=True)

def inject_custom_metrics_style():
    """カスタムメトリクス用スタイル"""
    st.markdown("""
    <style>
    /* メトリクス専用スタイル */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(31, 41, 55, 0.8), rgba(17, 24, 39, 0.9));
        border: 1px solid #374151;
        border-radius: 12px;
        padding: 1rem;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    [data-testid="metric-container"]:hover {
        border-color: #22c55e;
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(34, 197, 94, 0.2);
    }
    
    [data-testid="metric-container"] [data-testid="metric-value"] {
        color: #22c55e;
        font-weight: bold;
    }
    
    [data-testid="metric-container"] [data-testid="metric-label"] {
        color: #d1d5db;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)