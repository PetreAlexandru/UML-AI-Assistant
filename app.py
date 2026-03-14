import streamlit as st
import json
import os
from datetime import datetime
from utils import call_claude, render_mermaid
from utils import DIAGRAM_TYPES, BADGE_COLORS, STARTER_SUGGESTIONS

st.set_page_config(
    page_title="DiagramFlow",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Teme ───────────────────────────────────────────────────────────────────────
THEMES = {
    "Violet": {"primary": "#6366f1", "secondary": "#8b5cf6", "bg": "#0f172a", "sidebar": "#020617", "card": "#1e293b", "border": "#334155", "text": "#e2e8f0", "subtext": "#94a3b8"},
    "Blue":   {"primary": "#0ea5e9", "secondary": "#3b82f6", "bg": "#0c1a2e", "sidebar": "#071120", "card": "#0f2744", "border": "#1e3a5f", "text": "#e2e8f0", "subtext": "#93c5fd"},
    "Green":  {"primary": "#10b981", "secondary": "#059669", "bg": "#042f2e", "sidebar": "#021a1a", "card": "#064e3b", "border": "#065f46", "text": "#e2e8f0", "subtext": "#6ee7b7"},
    "Pink":   {"primary": "#ec4899", "secondary": "#db2777", "bg": "#1a0a14", "sidebar": "#0f0610", "card": "#2d1425", "border": "#4a1942", "text": "#e2e8f0", "subtext": "#f9a8d4"},
    "Orange": {"primary": "#f97316", "secondary": "#ea580c", "bg": "#1a0f00", "sidebar": "#0f0800", "card": "#2d1a00", "border": "#4a2800", "text": "#e2e8f0", "subtext": "#fed7aa"},
    "Red":    {"primary": "#ef4444", "secondary": "#dc2626", "bg": "#1a0a0a", "sidebar": "#0f0505", "card": "#2d1010", "border": "#4a1515", "text": "#e2e8f0", "subtext": "#fca5a5"},
    "Teal":   {"primary": "#14b8a6", "secondary": "#0d9488", "bg": "#021a18", "sidebar": "#010f0e", "card": "#042f2c", "border": "#064e4a", "text": "#e2e8f0", "subtext": "#5eead4"},
    "Gold":   {"primary": "#eab308", "secondary": "#ca8a04", "bg": "#1a1500", "sidebar": "#0f0d00", "card": "#2d2400", "border": "#4a3c00", "text": "#e2e8f0", "subtext": "#fde047"},
}

# ── Fisier pentru conversatii persistente ──────────────────────────────────────
CONVERSATIONS_FILE = "conversations.json"


def load_conversations_from_file() -> list:
    if os.path.exists(CONVERSATIONS_FILE):
        try:
            with open(CONVERSATIONS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data.get("conversations", [])
                return data  # compatibilitate cu formatul vechi
        except Exception:
            return []
    return []


def save_conversations_to_file(conversations: list) -> None:
    try:
        existing = {}
        if os.path.exists(CONVERSATIONS_FILE):
            with open(CONVERSATIONS_FILE, "r", encoding="utf-8") as f:
                content = json.load(f)
                if isinstance(content, dict):
                    existing = content
        existing["conversations"] = conversations
        with open(CONVERSATIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.error(f"Eroare salvare: {e}")

def load_api_key_from_file() -> str:
    if os.path.exists(CONVERSATIONS_FILE):
        try:
            with open(CONVERSATIONS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("api_key", "") if isinstance(data, dict) else ""
        except Exception:
            return ""
    return ""

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
    st.session_state.theme = "Violet"
if "conversations" not in st.session_state:
    st.session_state.conversations = load_conversations_from_file()
if "api_key" not in st.session_state:
    st.session_state.api_key = load_api_key_from_file()
if "active_conv_id" not in st.session_state:
    st.session_state.active_conv_id = None
if "editing_conv_id" not in st.session_state:
    st.session_state.editing_conv_id = None

T = THEMES[st.session_state.theme]

# ── CSS ────────────────────────────────────────────────────────────────────────
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
    .stTextInput input {{
        background-color: {T['card']} !important;
        color: {T['text']} !important;
        border-color: {T['border']} !important;
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
    st.session_state.editing_conv_id = None


def set_input(text):
    st.session_state.user_input = text
    st.session_state.trigger_send = True


def save_current_conversation():
    if not st.session_state.messages:
        return
    first_msg = next(
        (m["content"] for m in st.session_state.messages if m["role"] == "user"),
        "Conversatie noua"
    )
    title = first_msg[:40] + "..." if len(first_msg) > 40 else first_msg
    conv_id = st.session_state.active_conv_id

    if conv_id is not None:
        for conv in st.session_state.conversations:
            if conv["id"] == conv_id:
                conv["messages"] = st.session_state.messages.copy()
                conv["api_history"] = st.session_state.api_history.copy()
                if conv.get("title", "").endswith("...") or conv["title"] == "Conversatie noua":
                    conv["title"] = title
                break
    else:
        new_id = int(datetime.now().timestamp() * 1000)
        st.session_state.conversations.insert(0, {
            "id": new_id,
            "title": title,
            "messages": st.session_state.messages.copy(),
            "api_history": st.session_state.api_history.copy(),
            "date": datetime.now().strftime("%d.%m.%Y %H:%M"),
        })
        st.session_state.active_conv_id = new_id

    save_conversations_to_file(st.session_state.conversations)

def save_api_key_to_file(api_key: str) -> None:
    try:
        existing = {}
        if os.path.exists(CONVERSATIONS_FILE):
            with open(CONVERSATIONS_FILE, "r", encoding="utf-8") as f:
                content = json.load(f)
                if isinstance(content, dict):
                    existing = content
                else:
                    existing = {"conversations": content}
        existing["api_key"] = api_key
        with open(CONVERSATIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def load_conversation(conv_id):
    for conv in st.session_state.conversations:
        if conv["id"] == conv_id:
            st.session_state.messages = conv["messages"].copy()
            st.session_state.api_history = conv["api_history"].copy()
            st.session_state.active_conv_id = conv_id
            st.session_state.user_input = ""
            st.session_state.trigger_send = False
            st.session_state.editing_conv_id = None
            break


def delete_conversation(conv_id):
    st.session_state.conversations = [
        c for c in st.session_state.conversations if c["id"] != conv_id
    ]
    save_conversations_to_file(st.session_state.conversations)
    if st.session_state.active_conv_id == conv_id:
        clear_chat()


def rename_conversation(conv_id, new_title):
    for conv in st.session_state.conversations:
        if conv["id"] == conv_id:
            conv["title"] = new_title
            break
    save_conversations_to_file(st.session_state.conversations)
    st.session_state.editing_conv_id = None


# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://ase.ro/app/uploads/2024/06/sigla-ase-alb-mic-nou.png", width=100)
    with col2:
        st.image("https://csie.ase.ro/wp-content/uploads/2020/10/cropped-CSIE_new-300x132.png", width=80)

    st.markdown("## 🎯 UML AI Assistant")
    st.caption("Powered by Groq · ASE CSIE Statistica")
    st.divider()

    api_key_input = st.text_input(
        "🔑 Groq API Key",
        type="password",
        placeholder="gsk_...",
        help="Cheia se salveaza automat local",
        key="api_key",
    )
    if api_key_input and api_key_input != load_api_key_from_file():
        save_api_key_to_file(api_key_input)
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
            is_editing = conv["id"] == st.session_state.editing_conv_id

            if is_editing:
                # Mod editare titlu
                new_title = st.text_input(
                    "Redenumeste",
                    value=conv["title"],
                    key=f"rename_{conv['id']}",
                    label_visibility="collapsed",
                )
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("✓", key=f"save_rename_{conv['id']}", use_container_width=True):
                        rename_conversation(conv["id"], new_title)
                        st.rerun()
                with c2:
                    if st.button("✗", key=f"cancel_rename_{conv['id']}", use_container_width=True):
                        st.session_state.editing_conv_id = None
                        st.rerun()
            else:
                c1, c2, c3 = st.columns([5, 1, 1])
                with c1:
                    label = f"{'▶ ' if is_active else '💬 '}{conv['title']}"
                    if st.button(label, key=f"conv_{conv['id']}",
                                 use_container_width=True,
                                 help=f"Data: {conv.get('date', '')}"):
                        save_current_conversation()
                        load_conversation(conv["id"])
                        st.rerun()
                with c2:
                    if st.button("✏", key=f"edit_{conv['id']}"):
                        st.session_state.editing_conv_id = conv["id"]
                        st.rerun()
                with c3:
                    if st.button("🗑", key=f"del_{conv['id']}"):
                        delete_conversation(conv["id"])
                        st.rerun()

    st.divider()
    st.caption("PSI · ASE CSIE Statistica · 2026")


# ── MAIN ───────────────────────────────────────────────────────────────────────
st.markdown("### 🤖 Asistent UML cu Generative AI")
st.caption("Descrie un sistem si voi genera automat diagrama UML corespunzatoare")
st.divider()

if not st.session_state.messages:
    st.markdown(f"""
    <div style='text-align:center; padding:30px 0 20px 0;'>
        <div style='font-size:52px; margin-bottom:12px;'>🤖</div>
        <h3 style='color:{T['text']}; margin-bottom:8px;'>Bine ai venit!</h3>
        <p style='color:{T['subtext']}; font-size:14px; line-height:1.8;'>
            Descrie un sistem, o aplicatie sau un proces.<br/>
            Poti oferi detalii specifice despre entitati, relatii,<br/>
            actori sau fluxuri si voi genera diagrama UML potrivita.
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

# Istoricul conversatiei
for i, msg in enumerate(st.session_state.messages):
    if msg["role"] == "user":
        st.markdown(
            f'<div class="user-msg">🧑 {msg["content"]}</div>',
            unsafe_allow_html=True,
        )
        continue

    data          = msg.get("data", {})
    explanation   = data.get("explanation", "")
    diagram_type  = data.get("diagramType")
    plantuml_code = data.get("plantUMLCode")
    suggestions   = data.get("suggestions", [])

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

    if plantuml_code:
        tab1, tab2 = st.tabs(["👁️ Preview diagrama", "📄 Cod PlantUML"])
        with tab1:
            render_mermaid(plantuml_code, key=f"plantuml_{i}")
        with tab2:
            st.code(plantuml_code, language="text")
            st.download_button(
                "⬇️ Descarca .puml",
                data=plantuml_code,
                file_name="diagram.puml",
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

st.markdown(f"<p style='color:{T['subtext']}; font-size:12px; margin-bottom:4px;'>💡 Poti oferi detalii specifice — entitati, atribute, relatii, actori, fluxuri etc.</p>", unsafe_allow_html=True)

user_input = st.text_area(
    "Mesaj",
    value=st.session_state.user_input,
    placeholder='Ex: "Genereaza o diagrama de clase pentru un sistem de biblioteca cu entitatile: Carte (titlu, autor, ISBN), Membru (nume, email, dataInscriere), Imprumut (dataStart, dataReturn). Cartea poate fi imprumutata de mai multi membri."',
    height=120,
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
    save_current_conversation()
    st.rerun()