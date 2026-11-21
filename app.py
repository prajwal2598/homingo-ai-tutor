import streamlit as st
from google import genai
from google.genai import types

# Safely load your API key from Streamlit Secrets (never hardcode keys on GitHub!)
client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"],
    http_options=types.HttpOptions(timeout=20000),
)

st.set_page_config(page_title="MasteryAI", page_icon="🎓", layout="wide")

st.markdown(
    "<style>"
    ".block-container{padding-top:1.5rem;max-width:950px;}"
    ".hero{background:linear-gradient(135deg,#4F46E5,#7C3AED,#EC4899);padding:1.6rem 2rem;border-radius:16px;color:white;margin-bottom:1rem;}"
    ".hero h1{margin:0;font-size:2rem;color:white;} .hero p{margin:0.3rem 0 0 0;color:white;opacity:0.95;}"
    ".pill{display:inline-block;background:#EEF2FF;color:#4338CA;border:1px solid #C7D2FE;padding:4px 12px;border-radius:999px;font-size:0.85rem;font-weight:600;margin:0 6px 10px 0;}"
    ".card{background:#F8FAFC;border:1px solid #E2E8F0;border-left:5px solid #4F46E5;padding:1rem;border-radius:10px;margin-bottom:1rem;color:#1E293B;}"
    ".stButton>button{border-radius:10px;font-weight:600;}"
    "</style>",
    unsafe_allow_html=True,
)


@st.cache_data(ttl=300)
def get_models():
    try:
        m_list = [m.name.replace("models/", "") for m in client.models.list() if "gemini" in m.name and "embedding" not in m.name and "image" not in m.name]
        m_list.sort(key=lambda x: (0 if "lite" in x else (1 if "flash" in x else 2)))
        return m_list
    except Exception:
        return ["gemini-3.8-flash-lite", "gemini-3.8-flash"]


def ask_gemini(prompt, f_bytes=None, f_mime=None):
    contents = [types.Part.from_bytes(data=f_bytes, mime_type=f_mime), prompt] if (f_bytes and f_mime) else prompt
    err = ""
    for m in get_models()[:4]:
        try:
            res = client.models.generate_content(model=m, contents=contents)
            if res.text:
                return res.text
        except Exception as e:
            err = f"{m}: {e}"
    return f"⚠️ Server busy, please try again! ({err})"


for k, v in [("messages", []), ("topic", ""), ("mastered", []), ("quick", "")]:
    if k not in st.session_state:
        st.session_state[k] = v

with st.sidebar:
    st.markdown("## 👤 Learner Profile")
    lang = st.selectbox("🌐 Language", ["English", "Kannada", "Hindi", "Tamil", "Telugu", "Malayalam"])
    level = st.selectbox("🎯 Level", ["School (Class 5–10)", "PUC / Class 11–12", "College / University", "Self-Learner"])
    style = st.selectbox("🧠 Style", ["Real-World Analogies", "Step-by-Step Examples", "Mini-Puzzles", "Exam Revision"])
    easy = st.toggle("✨ Easy-Read Mode", value=True)
    st.divider()
    st.markdown("## 🏆 Mastery Progress")
    cnt = len(st.session_state.mastered)
    c_a, c_b = st.columns(2)
    c_a.metric("Total XP", f"{cnt * 100} ⚡")
    c_b.metric("Mastered", f"{cnt} 🎓")
    st.progress(min(cnt / 5.0, 1.0), text=f"Goal: {cnt}/5 Mastered")
    for item in st.session_state.mastered:
        st.success(f"✅ {item}")

rule = "Short sentences, bullet points, bold keywords, under 120 words." if easy else "Clear & concise, under 150 words."
ctx = f"Language: {lang} | Level: {level} | Style: {style} | Rule: {rule}"

st.markdown("<div class='hero'><h1>🎓 MasteryAI</h1><p>Diagnoses where you're stuck, teaches your way, and proves you learned it.</p></div>", unsafe_allow_html=True)
st.markdown(f"<span class='pill'>🌐 {lang}</span><span class='pill'>🎯 {level}</span><span class='pill'>🧠 {style}</span>", unsafe_allow_html=True)

st.markdown("#### 🔍 Choose a topic or upload your study material:")
b1, b2, b3, b4 = st.columns(4)
if b1.button("🐍 Python Loops", use_container_width=True): st.session_state.quick = "Python Loops"
if b2.button("🌍 Gravity", use_container_width=True): st.session_state.quick = "Gravity"
if b3.button("📐 Fractions", use_container_width=True): st.session_state.quick = "Fractions"
if b4.button("💰 What is GST?", use_container_width=True): st.session_state.quick = "What is GST"

col_t, col_f = st.columns((3, 2))
typed = col_t.text_input("Topic:", value=st.session_state.quick, placeholder="e.g., Photosynthesis, Problem 3 in photo...")
up_file = col_f.file_uploader("📎 Upload Image / PDF", type=["png", "jpg", "jpeg", "webp", "pdf", "txt"])

f_bytes = up_file.getvalue() if up_file else None
f_mime = up_file.type if up_file else None
subj = typed if typed else (up_file.name if up_file else "")

if up_file and f_mime and f_mime.startswith("image/"):
    with st.expander("🖼️ Preview Uploaded Image"):
        st.image(f_bytes, width=320)

if subj and subj != st.session_state.topic:
    st.session_state.topic = subj
    st.session_state.messages = []

tab1, tab2 = st.tabs(["💬 Step 1: Diagnostic Chat", "🏅 Step 2: Prove Mastery"])

with tab1:
    if not subj:
        st.markdown("<div class='card'><b>How it works:</b> Pick a topic or <b>upload a photo/PDF of your notes</b> → Answer 1–2 diagnostic questions → Prove mastery in Step 2!</div>", unsafe_allow_html=True)
    else:
        if not st.session_state.messages:
            st.markdown(f"<div class='card'>Ready to learn <b>{subj}</b> in <b>{lang}</b>!</div>", unsafe_allow_html=True)
            if st.button("🚀 Start Diagnostic Session", type="primary"):
                with st.spinner("Analyzing..."):
                    note = "Look closely at the attached file/image and base your diagnostic question on it. " if f_bytes else ""
                    p = f"Adaptive tutor. {ctx}\nTopic: '{subj}'. {note}Do NOT lecture yet. Greet warmly and ask 1 simple diagnostic question to find where they're stuck."
                    st.session_state.messages.append({"role": "assistant", "content": ask_gemini(p, f_bytes, f_mime)})
                    st.rerun()

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"], avatar="🎓" if msg["role"] == "assistant" else "🧑‍🎓"):
                st.markdown(msg["content"])

        if st.session_state.messages:
            with st.form("reply_form", clear_on_submit=True):
                c_in, c_btn = st.columns((4, 1))
                reply_txt = c_in.text_input("Reply", placeholder="Type your answer or ask a doubt...", label_visibility="collapsed")
                sent = c_btn.form_submit_button("Send ➤", use_container_width=True)
            if sent and reply_txt:
                st.session_state.messages.append({"role": "user", "content": reply_txt})
                hist = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages[-6:]])
                p = f"Patient adaptive tutor. {ctx}\nTopic: '{subj}'.\nChat:\n{hist}\nAnalyze their latest reply (and any uploaded file). Explain any gap simply in their style and ask 1 quick check-in question (or invite them to Step 2 if they got it!)."
                with st.spinner("Checking..."):
                    st.session_state.messages.append({"role": "assistant", "content": ask_gemini(p, f_bytes, f_mime)})
                st.rerun()

with tab2:
    st.markdown(f"<div class='card'><b>🎯 Teach-Back Test ({level}):</b> Explain <b>{subj or 'your topic'}</b> in your own words. Score <b>8/10+</b> to earn +100 XP!</div>", unsafe_allow_html=True)
    exp = st.text_area("Your explanation:", height=140, placeholder="In my own words...")
    if st.button("🏅 Grade My Understanding", type="primary"):
        if subj and exp:
            with st.spinner("Grading..."):
                gp = f"Supportive examiner. {ctx}\nTopic: '{subj}'. Student said: '{exp}'. Grade out of 10 (e.g., **Score: 8/10**), list what they nailed & any missing point. End with 'STATUS: PASSED' if >=8 else 'STATUS: TRY AGAIN'."
                ans = ask_gemini(gp, f_bytes, f_mime)
                st.markdown(ans)
                if "STATUS: PASSED" in ans:
                    st.balloons()
                    if subj not in st.session_state.mastered:
                        st.session_state.mastered.append(subj)
                        st.success(f"🎉 +100 XP! '{subj}' unlocked in your sidebar!")
        else:
            st.warning("Pick a topic or upload a file at the top, and write your explanation first!")
