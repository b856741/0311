import streamlit as st
import google.generativeai as genai

# 1. 頁面設定
st.set_page_config(page_title="AI 多國語言翻譯助手", page_icon="🌐")

# --- Session State 初始化 (修正點：處理按鈕帶入文字) ---
if 'source_text' not in st.session_state:
    st.session_state.source_text = ""

# 2. 安全讀取 API Key
def get_api_key():
    key = st.secrets.get("GOOGLE_API_KEY")
    if not key:
        key = "" # 建議不要在此寫死 Key，請用 Streamlit Secrets
    return key.strip()

api_key = get_api_key()

if not api_key:
    st.error("❌ 偵測到無效的 API Key。請在 Streamlit Cloud 的 Secrets 設定中配置 GOOGLE_API_KEY。")
    st.stop()

# 初始化 Gemini
genai.configure(api_key=api_key)

# --- 介面設計 ---
st.title("🌐 Gemini AI 雲端翻譯器")
st.caption("由 Gemini AI 驅動，支援多國語言與語氣轉換")

with st.sidebar:
    st.header("設定")
    target_lang = st.selectbox("目標語言", ["繁體中文", "English", "日本語", "韓國語", "Français", "Español"])
    tone = st.select_slider("語氣風格", options=["極其口語", "一般", "專業正式"])
    st.divider()
    
    # 修正點：點擊後更新 state 並強制 rerun，文字才會顯示在輸入框
    if st.button("💡 帶入西文範例測試"):
        st.session_state.source_text = "El éxito no es la clave de la felicidad. La felicidad es la clave del éxito."
        st.rerun() 

# 主界面輸入框 (修正點：連結 value 到 session_state)
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
        with st.spinner("AI 正在翻譯中..."):
            try:
                # 診斷代碼：列出你的 Key 目前能用的所有模型（如果還是 404 可以檢查這裡）
                # models_list = [m.name for m in genai.list_models()]
                # st.write(f"系統偵測模型：{models_list}") 

                # 嘗試使用正式版名稱
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # 修正提示：如果上面的 model 建立失敗，改用下方的替代方案
                # model = genai.GenerativeModel('models/gemini-1.5-flash')
                
                prompt = (
                    f"你是一位專業的翻譯官。請將以下內容翻譯成{target_lang}，"
                    f"語氣設定為【{tone}】。請直接輸出翻譯結果，不要有額外評論：\n\n{source_text}"
                )
                
                response = model.generate_content(prompt)
                
                if response.text:
                    st.success("翻譯完成！")
                    st.markdown("### 翻譯結果：")
                    st.info(response.text)
            except Exception as e:
                st.error(f"連線錯誤：{e}")
                # 這裡是一個自動救援邏輯：如果 flash 失敗，改試試 pro
                if "404" in str(e):
                    st.info("正在嘗試備用模型 (gemini-1.5-pro)...")
                    try:
                        model_backup = genai.GenerativeModel('gemini-1.5-pro')
                        response = model_backup.generate_content(prompt)
                        st.info(response.text)
                    except:
                        st.error("所有模型均無法連線，請檢查 API Key 是否在 Google AI Studio 申請。")

st.divider()
st.caption("🚀 部署完成後，將此網址貼進 EEP 即可在手機使用。")
