import streamlit as st
import google.generativeai as genai

# 1. 頁面設定
st.set_page_config(page_title="AI 多國語言翻譯助手", page_icon="🌐")

# --- Session State 初始化 ---
if 'source_text' not in st.session_state:
    st.session_state.source_text = ""

# 2. 安全讀取 API Key
def get_api_key():
    key = st.secrets.get("GOOGLE_API_KEY")
    return key.strip() if key else None

api_key = get_api_key()

if not api_key:
    st.error("❌ 偵測到無效的 API Key。請在 Streamlit Cloud 的 Secrets 設定中配置 GOOGLE_API_KEY。")
    st.stop()

# 初始化 Gemini
genai.configure(api_key=api_key)

# --- 介面設計 ---
st.title("🌐 Gemini AI 雲端翻譯器")
st.caption("由 Gemini AI 驅動，支援 2026 最新版本多國語言轉換")

with st.sidebar:
    st.header("設定")
    target_lang = st.selectbox("目標語言", ["繁體中文", "English", "日本語", "韓國語", "Français", "Español"])
    tone = st.select_slider("語氣風格", options=["極其口語", "一般", "專業正式"])
    st.divider()
    
    if st.button("💡 帶入西文範例測試"):
        st.session_state.source_text = "El éxito no es la clave de la felicidad. La felicidad es la clave del éxito. Si amas lo que estás haciendo, serás exitoso."
        st.rerun() 

# 主界面輸入框
source_text = st.text_area(
    "輸入原文", 
    value=st.session_state.source_text, 
    placeholder="請輸入要翻譯的文字...", 
    height=200
)

if st.button("開始翻譯", type="primary"):
    if not source_text:
        st.warning("請先輸入內容喔！")
    else:
        with st.spinner("AI 正在進行高精度翻譯..."):
            try:
                # 使用診斷成功的最新模型：Gemini 2.5 Flash
                model = genai.GenerativeModel('models/gemini-2.5-flash')
                
                prompt = (
                    f"你是一位精通各國語言的翻譯大師。請將以下內容翻譯成{target_lang}，"
                    f"並確保語氣符合【{tone}】的設定。請只輸出翻譯結果，不要包含任何解釋：\n\n{source_text}"
                )
                
                response = model.generate_content(prompt)
                
                if response.text:
                    st.success("翻譯完成！")
                    st.markdown("### 翻譯結果：")
                    st.info(response.text)
                else:
                    st.warning("AI 暫時沒有回應，請重新點擊。")
                    
            except Exception as e:
                st.error(f"連線發生問題：{e}")
                st.info("建議檢查 Streamlit Secrets 中的 API Key 是否正確貼上。")

st.divider()
st.caption("🚀 提示：您可以將此頁面網址加入手機主畫面，或嵌入 EEP App 中使用。")
