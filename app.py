import streamlit as st
import google.generativeai as genai

# 設定頁面資訊
st.set_page_config(page_title="AI 多國語言翻譯助手", page_icon="🌐")

# 在 Streamlit Cloud 部署時，建議將 API Key 放在 Secrets 中
# 本地測試可以直接填入字串，但上傳 GitHub 前請移除
GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY", "你的_GEMINI_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

st.title("🌐 Gemini AI 雲端翻譯器")
st.caption("由 Gemini AI 驅動，支援多國語言與語氣轉換")

# 側邊欄設定
with st.sidebar:
    st.header("設定")
    target_lang = st.selectbox("目標語言", ["繁體中文", "English", "日本語", "한국어", "Français"])
    tone = st.select_slider("語氣風格", options=["極其口語", "一般", "專業正式"])

# 主界面
source_text = st.text_area("輸入原文", placeholder="請輸入要翻譯的文字...", height=200)

if st.button("開始翻譯"):
    if not source_text:
        st.warning("請先輸入內容喔！")
    else:
        with st.spinner("AI 正在思考中..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = f"你是一位專業的翻譯官。請將以下內容翻譯成{target_lang}，語氣設定為【{tone}】。只需回傳翻譯後的內容：\n\n{source_text}"
                
                response = model.generate_content(prompt)
                
                st.success("翻譯完成！")
                st.markdown("### 翻譯結果：")
                st.info(response.text)
            except Exception as e:
                st.error(f"發生錯誤：{e}")

st.divider()
st.caption("💡 提示：在手機 EEP 上打開網址，即可隨身使用！")