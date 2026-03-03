import streamlit as st
from utils import call_claude, render_mermaid
from utils import DIAGRAM_TYPES, BADGE_COLORS, STARTER_SUGGESTIONS

st.set_page_config(
    page_title="UML AI Assistant",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .stApp { background-color: #0f172a; color: #e2e8f0; }
    section[data-testid="stSidebar"] {
        background-color: #020617 !important;
        border-right: 1px solid #1e293b;
    }
    [data-testid="collapsedControl"] {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
    }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .user-msg {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white;
        border-radius: 18px 18px 4px 18px;
        padding: 12px 18px;
        margin: 8px 0 8px auto;
        max-width: 75%;
        font-size: 14px;
        line-height: 1.6;
    }
    .assistant-msg {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 4px 18px 18px 18px;
        padding: 16px 20px;
        margin: 8px 0;
        font-size: 14px;
        line-height: 1.7;
        color: #cbd5e1;
    }
    .badge {
        display: inline-block;
        border-radius: 20px;
        padding: 3px 12px;
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 8px;
    }
    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }
    .stTabs [aria-selected="true"] {
        background: #6366f1 !important;
        color: white !important;
        border-radius: 6px !important;
    }
    hr { border-color: #1e293b; }
    .stTextArea textarea {
        background-color: #1e293b !important;
        color: #e2e8f0 !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "api_history" not in st.session_state:
    st.session_state.api_history = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "trigger_send" not in st.session_state:
    st.session_state.trigger_send = False


def clear_chat():
    st.session_state.messages = []
    st.session_state.api_history = []
    st.session_state.user_input = ""
    st.session_state.trigger_send = False


def set_input(text):
    st.session_state.user_input = text
    st.session_state.trigger_send = True


with st.sidebar:
    st.markdown("## 🎯 UML AI Assistant")
    st.caption("Powered by Claude · ASE CSIE Statistica")
    st.divider()

    st.text_input(
        "🔑 Google Gemini API Key",
        type="password",
        placeholder="AIza...",
        help="Obtine cheia de pe aistudio.google.com",
        key="api_key",
    )

    if st.session_state.get("api_key"):
        st.success("API Key setat ✅")
    else:
        st.warning("⚠️ Introdu API key-ul pentru a continua")

    st.divider()

    if st.button("✏️ Conversatie noua", use_container_width=True):
        clear_chat()
        st.rerun()

    st.divider()
    st.markdown("**Tipuri de diagrame**")

    for icon, name, desc in DIAGRAM_TYPES:
        if st.button(f"{icon} {name}", key=f"sidebar_{name}",
                     use_container_width=True, help=desc):
            set_input(f"Genereaza o {name} pentru un sistem de gestiune studenti")
            st.rerun()

    st.divider()
    st.caption("PSI · ASE CSIE Statistica · 2025")


st.markdown("### 🤖 Asistent UML cu Generative AI")
st.caption("Descrie un sistem si voi genera automat diagrama UML corespunzatoare")
st.divider()

if not st.session_state.messages:
    st.markdown("""
    <div style='text-align:center; padding:30px 0 20px 0;'>
        <div style='font-size:52px; margin-bottom:12px;'>🤖</div>
        <h3 style='color:#e2e8f0; margin-bottom:8px;'>Bine ai venit!</h3>
        <p style='color:#64748b; font-size:14px; line-height:1.8;'>
            Descrie un sistem, o aplicatie sau un proces<br/>
            si voi genera automat diagrama UML potrivita.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### 💡 Incearca una din sugestii:")
    cols = st.columns(2)
    for i, suggestion in enumerate(STARTER_SUGGESTIONS):
        with cols[i % 2]:
            if st.button(suggestion, key=f"starter_{i}", use_container_width=True):
                set_input(suggestion)
                st.rerun()

for i, msg in enumerate(st.session_state.messages):
    if msg["role"] == "user":
        st.markdown(
            f'<div class="user-msg">🧑 {msg["content"]}</div>',
            unsafe_allow_html=True,
        )
        continue

    data         = msg.get("data", {})
    explanation  = data.get("explanation", "")
    diagram_type = data.get("diagramType")
    mermaid_code = data.get("mermaidCode")
    suggestions  = data.get("suggestions", [])

    badge_html = ""
    if diagram_type:
        color, bg = BADGE_COLORS.get(diagram_type, ("#64748b", "#f1f5f9"))
        badge_html = (
            f'<span class="badge" style="background:{bg}22;'
            f'color:{color};border:1px solid {color}44;">'
            f'{diagram_type}</span><br/>'
        )

    st.markdown(
        f'<div class="assistant-msg">{badge_html}🤖 {explanation}</div>',
        unsafe_allow_html=True,
    )

    if mermaid_code:
        tab1, tab2 = st.tabs(["👁️ Preview diagrama", "📄 Cod Mermaid"])
        with tab1:
            render_mermaid(mermaid_code, key=f"mermaid_{i}")
        with tab2:
            st.code(mermaid_code, language="text")
            st.download_button(
                "⬇️ Descarca .mmd",
                data=mermaid_code,
                file_name="diagram.mmd",
                mime="text/plain",
                key=f"dl_{i}",
            )

    if suggestions:
        st.markdown("**💡 Sugestii de continuare:**")
        scols = st.columns(min(len(suggestions), 3))
        for j, s in enumerate(suggestions):
            with scols[j % 3]:
                if st.button(s, key=f"sugg_{i}_{j}", use_container_width=True):
                    set_input(s)
                    st.rerun()

st.divider()

user_input = st.text_area(
    "Mesaj",
    value=st.session_state.user_input,
    placeholder="Descrie sistemul pentru care vrei o diagrama UML...",
    height=100,
    label_visibility="collapsed",
    key="text_area_input",
)

col1, col2, col3 = st.columns([4, 1, 1])
with col2:
    send_clicked = st.button("➤ Trimite", use_container_width=True,
                             disabled=not user_input.strip())
with col3:
    if st.button("🗑️ Sterge", use_container_width=True):
        clear_chat()
        st.rerun()

st.caption("⚠️ Diagramele generate de AI pot contine erori. Verifica intotdeauna rezultatele.")

should_send = send_clicked or st.session_state.trigger_send
final_text  = user_input.strip() or st.session_state.user_input.strip()

if should_send and final_text:
    st.session_state.trigger_send = False
    st.session_state.user_input   = ""
    st.session_state.messages.append({"role": "user", "content": final_text})
    with st.spinner("🤖 Analizez si generez diagrama..."):
        data = call_claude(final_text)
    st.session_state.messages.append(
        {"role": "assistant", "content": "", "data": data}
    )
    st.rerun()