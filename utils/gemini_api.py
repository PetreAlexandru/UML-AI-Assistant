import re
import json
import google.generativeai as genai
import streamlit as st
from utils.constants import SYSTEM_PROMPT


def call_claude(user_text: str) -> dict:
    """
    Trimite un mesaj catre Gemini si returneaza raspunsul parsat ca dict.
    (Numele functiei ramane call_claude pentru compatibilitate cu app.py)

    Returns:
        dict cu cheile: explanation, diagramType, mermaidCode, suggestions
    """
    api_key = st.session_state.get("api_key", "")

    if not api_key:
        return {
            "explanation": "⚠️ Introdu API key-ul Google Gemini in sidebar.",
            "diagramType": None,
            "mermaidCode": None,
            "suggestions": [],
        }

    try:
        # Configurare client Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            system_instruction=SYSTEM_PROMPT,
        )

        # Construim istoricul conversatiei in formatul Gemini
        history = []
        for msg in st.session_state.api_history:
            role = "user" if msg["role"] == "user" else "model"
            history.append({"role": role, "parts": [msg["content"]]})

        # Cream sesiunea de chat cu istoric
        chat = model.start_chat(history=history)

        # Trimitem mesajul
        response = chat.send_message(user_text)
        raw = response.text

        # Curatam eventualele backticks din raspuns
        clean = re.sub(r"```json|```", "", raw).strip()
        data = json.loads(clean)

        # Salvam in istoricul pentru context
        st.session_state.api_history.append(
            {"role": "user", "content": user_text}
        )
        st.session_state.api_history.append(
            {"role": "assistant", "content": raw}
        )
        return data

    except json.JSONDecodeError:
        return {
            "explanation": raw,
            "diagramType": None,
            "mermaidCode": None,
            "suggestions": [],
        }
    except Exception as e:
        return {
            "explanation": f"❌ Eroare API: {str(e)}",
            "diagramType": None,
            "mermaidCode": None,
            "suggestions": [],
        }