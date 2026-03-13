import streamlit as st
from utils import call_claude, render_mermaid
from utils import DIAGRAM_TYPES, BADGE_COLORS, STARTER_SUGGESTIONS
import json
from datetime import datetime

st.set_page_config(
    page_title="UML AI Assistant",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Teme de culori ─────────────────────────────────────────────────────────────
THEMES = {
    "Violet (default)": {
        "primary": "#6366f1",
        "secondary": "#8b5cf6",
        "bg": "#0f172a",
        "sidebar": "#020617",
        "card": "#1e293b",
        "border": "#334155",
        "text": "#e2e8f0",
        "subtext": "#94a3b8",
    },
    "Blue": {
        "primary": "#0ea5e9",
        "secondary": "#3b82f6",
        "bg": "#0c1a2e",
        "sidebar": "#071120",
        "card": "#0f2744",
        "border": "#1e3a5f",
        "text": "#e2e8f0",
        "subtext": "#93c5fd",
    },
    "Green": {
        "primary": "#10b981",
        "secondary": "#059669",
        "bg": "#042f2e",
        "sidebar": "#021a1a",
        "card": "#064e3b",
        "border": "#065f46",
        "text": "#e2e8f0",
        "subtext": "#6ee7b7",
    },
    "Pink": {
        "primary": "#ec4899",
        "secondary": "#db2777",
        "bg": "#1a0a14",
        "sidebar": "#0f0610",
        "card": "#2d1425",
        "border": "#4a1942",
        "text": "#e2e8f0",
        "subtext": "#f9a8d4",
    },
    "Orange": {
        "primary": "#f97316",
        "secondary": "#ea580c",
        "bg": "#1a0f00",
        "sidebar": "#0f0800",
        "card": "#2d1a00",
        "border": "#4a2800",
        "text": "#e2e8f0",
        "subtext": "#fed7aa",
    },
}

# ── Session state ──────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "api_history" not in st.session_state:
    st.session_state.api_history = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "trigger_send" not in st.session_state:
    st.session_state.trigger_send = False
if "theme" not in st.session_state:
    st.session_state.theme = "Violet (default)"
if "conversations" not in st.session_state:
    # Lista de conversatii salvate: [{id, title, messages, api_history, date}]
    st.session_state.conversations = []
if "active_conv_id" not in st.session_state:
    st.session_state.active_conv_id = None

# ── Tema activa ────────────────────────────────────────────────────────────────
T = THEMES[st.session_state.theme]

# ── CSS dinamic bazat pe tema ──────────────────────────────────────────────────
st.markdown(f"""
<style>
    .stApp {{ background-color: {T['bg']}; color: {T['text']}; }}
    section[data-testid="stSidebar"] {{
        background-color: {T['sidebar']} !important;
        border-right: 1px solid {T['border']};
    }}
    [data-testid="collapsedControl"] {{
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        background-color: {T['card']} !important;
        border: 1px solid {T['border']} !important;
        border-radius: 8px !important;
    }}
    #MainMenu {{ visibility: hidden; }}
    footer {{ visibility: hidden; }}
    .user-msg {{
        background: linear-gradient(135deg, {T['primary']}, {T['secondary']});
        color: white;
        border-radius: 18px 18px 4px 18px;
        padding: 12px 18px;
        margin: 8px 0 8px auto;
        max-width: 75%;
        font-size: 14px;
        line-height: 1.6;
        box-shadow: 0 4px 15px {T['primary']}44;
    }}
    .assistant-msg {{
        background: {T['card']};
        border: 1px solid {T['border']};
        border-radius: 4px 18px 18px 18px;
        padding: 16px 20px;
        margin: 8px 0;
        font-size: 14px;
        line-height: 1.7;
        color: {T['text']};
    }}
    .badge {{
        display: inline-block;
        border-radius: 20px;
        padding: 3px 12px;
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 8px;
    }}
    .conv-item {{
        background: {T['card']};
        border: 1px solid {T['border']};
        border-radius: 8px;
        padding: 8px 12px;
        margin-bottom: 4px;
        cursor: pointer;
        font-size: 12px;
        color: {T['subtext']};
    }}
    .conv-item:hover {{
        border-color: {T['primary']};
        color: {T['text']};
    }}
    .conv-item-active {{
        border-color: {T['primary']} !important;
        background: {T['primary']}22 !important;
        color: {T['text']} !important;
    }}
    .stButton > button {{
        background: linear-gradient(135deg, {T['primary']}, {T['secondary']}) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }}
    .stTabs [aria-selected="true"] {{
        background: {T['primary']} !important;
        color: white !important;
        border-radius: 6px !important;
    }}
    hr {{ border-color: {T['border']}; }}
    .stTextArea textarea {{
        background-color: {T['card']} !important;
        color: {T['text']} !important;
        border: 1px solid {T['border']} !important;
        border-radius: 10px !important;
    }}
    div[data-baseweb="select"] > div {{
        background-color: {T['card']} !important;
        border-color: {T['border']} !important;
        color: {T['text']} !important;
    }}
</style>
""", unsafe_allow_html=True)


# ── Helpers ────────────────────────────────────────────────────────────────────
def clear_chat():
    st.session_state.messages = []
    st.session_state.api_history = []
    st.session_state.user_input = ""
    st.session_state.trigger_send = False
    st.session_state.active_conv_id = None


def set_input(text):
    st.session_state.user_input = text
    st.session_state.trigger_send = True


def save_current_conversation():
    """Salveaza conversatia curenta in istoric."""
    if not st.session_state.messages:
        return

    # Titlul conversatiei = primul mesaj al utilizatorului (trunchiat)
    first_msg = next(
        (m["content"] for m in st.session_state.messages if m["role"] == "user"),
        "Conversatie noua"
    )
    title = first_msg[:40] + "..." if len(first_msg) > 40 else first_msg

    conv_id = st.session_state.active_conv_id

    if conv_id is not None:
        # Actualizam conversatia existenta
        for conv in st.session_state.conversations:
            if conv["id"] == conv_id:
                conv["messages"] = st.session_state.messages.copy()
                conv["api_history"] = st.session_state.api_history.copy()
                conv["title"] = title
                break
    else:
        # Cream o conversatie noua
        new_id = len(st.session_state.conversations)
        st.session_state.conversations.insert(0, {
            "id": new_id,
            "title": title,
            "messages": st.session_state.messages.copy(),
            "api_history": st.session_state.api_history.copy(),
            "date": datetime.now().strftime("%d.%m %H:%M"),
        })
        st.session_state.active_conv_id = new_id


def load_conversation(conv_id):
    """Incarca o conversatie din istoric."""
    for conv in st.session_state.conversations:
        if conv["id"] == conv_id:
            st.session_state.messages = conv["messages"].copy()
            st.session_state.api_history = conv["api_history"].copy()
            st.session_state.active_conv_id = conv_id
            st.session_state.user_input = ""
            st.session_state.trigger_send = False
            break


def delete_conversation(conv_id):
    """Sterge o conversatie din istoric."""
    st.session_state.conversations = [
        c for c in st.session_state.conversations if c["id"] != conv_id
    ]
    if st.session_state.active_conv_id == conv_id:
        clear_chat()


# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://ase.ro/app/uploads/2024/06/sigla-ase-alb-mic-nou.png", width=100)
    with col2:
        st.image("https://csie.ase.ro/wp-content/uploads/2020/10/cropped-CSIE_new-300x132.png", width=80)

    st.markdown(f"## 🎯 UML AI Assistant")
    st.caption("Powered by Groq · ASE CSIE Statistica")
    st.divider()

    # API Key
    st.text_input(
        "🔑 Groq API Key",
        type="password",
        placeholder="gsk_...",
        help="Obtine cheia de pe console.groq.com",
        key="api_key",
    )
    if st.session_state.get("api_key"):
        st.success("API Key setat ✅")
    else:
        st.warning("⚠️ Introdu API key-ul")

    st.divider()

    # Tema
    st.markdown("**🎨 Tema**")
    selected_theme = st.selectbox(
        "Tema",
        options=list(THEMES.keys()),
        index=list(THEMES.keys()).index(st.session_state.theme),
        label_visibility="collapsed",
        key="theme_select",
    )
    if selected_theme != st.session_state.theme:
        st.session_state.theme = selected_theme
        st.rerun()

    st.divider()

    # Conversatie noua + tipuri diagrame
    if st.button("✏️ Conversatie noua", use_container_width=True):
        save_current_conversation()
        clear_chat()
        st.rerun()

    st.markdown("**Tipuri de diagrame**")
    for icon, name, desc in DIAGRAM_TYPES:
        if st.button(f"{icon} {name}", key=f"sidebar_{name}",
                     use_container_width=True, help=desc):
            set_input(f"Genereaza o {name} pentru un sistem de gestiune studenti")
            st.rerun()

    st.divider()

    # Istoric conversatii
    st.markdown("**🕐 Istoric conversatii**")
    if not st.session_state.conversations:
        st.caption("Nicio conversatie salvata inca.")
    else:
        for conv in st.session_state.conversations:
            is_active = conv["id"] == st.session_state.active_conv_id
            col_title, col_del = st.columns([5, 1])
            with col_title:
                css_class = "conv-item-active" if is_active else "conv-item"
                if st.button(
                    f"💬 {conv['title']}",
                    key=f"conv_{conv['id']}",
                    use_container_width=True,
                    help=f"Data: {conv['date']}",
                ):
                    save_current_conversation()
                    load_conversation(conv["id"])
                    st.rerun()
            with col_del:
                if st.button("🗑", key=f"del_{conv['id']}"):
                    delete_conversation(conv["id"])
                    st.rerun()

    st.divider()
    st.caption(f"PSI · ASE CSIE Statistica · 2026")


# ── MAIN ───────────────────────────────────────────────────────────────────────
st.markdown("### 🤖 Asistent UML cu Generative AI")
st.caption("Descrie un sistem si voi genera automat diagrama UML corespunzatoare")
st.divider()

# Ecran bun venit
if not st.session_state.messages:
    st.markdown(f"""
    <div style='text-align:center; padding:30px 0 20px 0;'>
        <div style='font-size:52px; margin-bottom:12px;'>🤖</div>
        <h3 style='color:{T['text']}; margin-bottom:8px;'>Bine ai venit!</h3>
        <p style='color:{T['subtext']}; font-size:14px; line-height:1.8;'>
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

# Istoricul conversatiei curente
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

# ── INPUT ──────────────────────────────────────────────────────────────────────
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
        save_current_conversation()
        clear_chat()
        st.rerun()

st.caption("⚠️ Diagramele generate de AI pot contine erori. Verifica intotdeauna rezultatele.")

# ── PROCESARE ──────────────────────────────────────────────────────────────────
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
    # Salvam automat conversatia dupa fiecare mesaj
    save_current_conversation()
    st.rerun()