import streamlit as st
from query import ask

st.set_page_config(page_title="בטוח בבית", page_icon="🏠")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rubik:wght@400;500;700&display=swap');

/* כיוון, גופן ורקע */
.stApp {
    direction: rtl;
    text-align: right;
    font-family: 'Rubik', sans-serif;
    background: linear-gradient(180deg, #EAF1FA 0%, #F7FAFD 40%, #FFFFFF 100%);
}
.stMarkdown, textarea, .stChatMessage {
    direction: rtl;
    text-align: right;
}

/* הסתרת התפריט והכיתוב של Streamlit */
#MainMenu, footer, header {
    visibility: hidden;
}

/* כרטיס הכותרת */
.hero {
    background: linear-gradient(135deg, #123A66, #1F5A96, #3D7FC9);
    color: white;
    padding: 28px 28px 24px;
    border-radius: 22px;
    box-shadow: 0 10px 30px rgba(18, 58, 102, 0.25);
    margin-bottom: 14px;
}
.hero .name {
    color: white;
    font-size: 2.2rem;
    font-weight: 700;
}
.hero p {
    margin: 6px 0 0;
    font-size: 1.05rem;
}

/* שלוש קופסאות נתונים */
.stats {
    display: flex;
    gap: 10px;
    margin-bottom: 18px;
}
.stat {
    flex: 1;
    background: white;
    border-radius: 16px;
    padding: 12px;
    text-align: center;
    box-shadow: 0 2px 10px rgba(18, 58, 102, 0.08);
}
.stat b {
    display: block;
    font-size: 1.4rem;
    color: #1F5A96;
}
.stat span {
    font-size: 0.85rem;
    color: #66768A;
}

/* בועות הצ'אט */
.stChatMessage {
    background: white;
    border-radius: 18px;
    padding: 14px 18px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
    border-right: 4px solid #3D7FC9;
}
.stChatMessage:has([aria-label="Chat message from user"]) {
    background: #E1ECF8;
    border-right: 4px solid #123A66;
}

/* כפתורי השאלות המוכנות */
.stButton button {
    border-radius: 999px;
    border: 1px solid #1F5A96;
    color: #1F5A96;
    background: white;
}
.stButton button:hover {
    background: #1F5A96;
    border-color: #1F5A96;
    color: white;
}

/* סרגל הצד */
[data-testid="stSidebar"] {
    direction: rtl;
    text-align: right;
    background: #E8F0FA;
    border-left: 1px solid #CFDDEE;
}
[data-testid="stSidebar"] h2 {
    color: #123A66;
}
</style>
""", unsafe_allow_html=True)

# כרטיס הכותרת
st.markdown("""
<div class="hero">
    <div class="name">🏠 Safe-home </div>
    <p>העוזר החכם שעונה על כל שאלה על השירות</p>
</div>
""", unsafe_allow_html=True)

# קופסאות נתונים
st.markdown("""
<div class="stats">
    <div class="stat"><b>3</b><span>חיישנים בבית</span></div>
    <div class="stat"><b>400 ₪</b><span>רכישה והתקנה</span></div>
    <div class="stat"><b>19 ₪</b><span>מנוי חודשי</span></div>
</div>
""", unsafe_allow_html=True)

# סרגל הצד
with st.sidebar:
    st.header("📞 שירות לקוחות")
    st.write("טלפון: 5050*")
    st.write("ימים א'–ה', 9:00–13:00")
    st.header("ℹ️ על הבוט")
    st.write("הבוט עונה רק מתוך המידע הרשמי של החברה.")

# זיכרון השיחה
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "שלום! 👋 אני העוזר של בטוח בבית. במה אפשר לעזור?"}
    ]

avatars = {"user": "👤", "assistant": "🏠"}

for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=avatars[msg["role"]]):
        st.write(msg["content"])

# שאלות מוכנות, רק בתחילת השיחה
clicked = None
if len(st.session_state.messages) == 1:
    suggestions = ["כמה עולה המנוי?", "מה קורה בשבת?", "איך עובדות ההתראות?"]
    cols = st.columns(3)
    for col, s in zip(cols, suggestions):
        if col.button(s, use_container_width=True):
            clicked = s

question = st.chat_input("שאלי שאלה על השירות...") or clicked

if question:
    with st.chat_message("user", avatar="👤"):
        st.write(question)

    with st.chat_message("assistant", avatar="🏠"):
        try:
            with st.spinner("מחפש תשובה..."):
                answer = ask(question)
            st.write(answer)
        except Exception:
            answer = "מצטערים, השירות עמוס כרגע או שנגמרה המכסה היומית. נסו שוב בעוד כמה דקות."
            st.error(answer)

    st.session_state.messages.append({"role": "user", "content": question})
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()
