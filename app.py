import streamlit as st
import google.generativeai as genai

# 1. 頁面設定
st.set_page_config(page_title="AI 多國語言翻譯助手", page_icon="🌐")

# 2. 安全讀取 API Key 並過濾無效字元
def get_api_key():
    # 優先從 Streamlit Secrets 讀取，若無則嘗試環境變數或手動輸入
    key = st.secrets.get("GOOGLE_API_KEY")
    if not key:
        # 這裡的 "你的_GEMINI_API_KEY" 僅供本地測試，上傳 GitHub 建議留空
        key = "你的_GEMINI_API_KEY"
    
    # 重要：使用 .strip() 去除所有前後可能的換行或空格
    return key.strip() if key else None

api_key = get_api_key()

if not api_key or "你的" in api_key:
    st.error("❌ 偵測到無效的 API Key。請在 Streamlit Cloud 的 Secrets 設定中配置 GOOGLE_API_KEY。")
    st.stop()

# 初始化 Gemini
genai.configure(api_key=api_key)

# --- 介面設計 ---
st.title("🌐 Gemini AI 雲端翻譯器")
st.caption("由 Gemini AI 驅動，支援多國語言與語氣轉換")

with st.sidebar:
    st.header("設定")
    target_lang = st.selectbox("目標語言", ["繁體中文", "English", "日本語", "한국어", "Français", "Español"])
    tone = st.select_slider("語氣風格", options=["極其口語", "一般", "專業正式"])
    st.divider()
    st.info("💡 提示：在手機 EEP 上開啟此網頁即可使用。")

source_text = st.text_area("輸入原文", placeholder="請輸入要翻譯的文字...", height=200)

# 加入你剛才要求的西文測試按鈕（選填）
if st.button("帶入西文範例測試"):
    st.session_state.source_text = "El éxito no es la clave de la felicidad. La felicidad es la clave del éxito."
    # 註：需搭配下方 text_area 的 value=st.session_state.get('source_text', '') 使用

if st.button("開始翻譯", type="primary"):
    if not source_text:
        st.warning("請先輸入內容喔！")
    else:
        with st.spinner("AI 正在翻譯中..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = (
                    f"你是一位專業的翻譯官。請將以下內容翻譯成{target_lang}，"
                    f"語氣設定為【{tone}】。請直接輸出翻譯結果，不要有額外評論：\n\n{source_text}"
                )
                
                response = model.generate_content(prompt)
                
                if response.text:
                    st.success("翻譯完成！")
                    st.markdown("### 翻譯結果：")
                    st.info(response.text)
                else:
                    st.error("AI 回傳內容為空，請稍後再試。")
            except Exception as e:
                # 這裡會捕捉並顯示錯誤，幫助我們確認是否還有 Header 問題
                st.error(f"連線錯誤：{e}")

st.divider()
