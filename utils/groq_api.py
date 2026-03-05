import re
import json
import streamlit as st
from groq import Groq
from utils.constants import SYSTEM_PROMPT


def call_claude(user_text: str) -> dict:
    """
    Trimite un mesaj catre Groq (Llama 3) si returneaza raspunsul parsat ca dict.
    Numele functiei ramane call_claude pentru compatibilitate cu app.py.

    Returns:
        dict cu cheile: explanation, diagramType, mermaidCode, suggestions
    """
    api_key = st.session_state.get("api_key", "")

    if not api_key:
        return {
            "explanation": "⚠️ Introdu API key-ul Groq in sidebar.",
            "diagramType": None,
            "mermaidCode": None,
            "suggestions": [],
        }

    try:
        client = Groq(api_key=api_key)

        # Construim istoricul conversatiei
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

        for msg in st.session_state.api_history:
            messages.append({
                "role": msg["role"] if msg["role"] == "user" else "assistant",
                "content": msg["content"]
            })

        messages.append({"role": "user", "content": user_text})

        # Apel API Groq
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=1500,
        )

        raw = response.choices[0].message.content

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
            "explanation": f"Debug - raspuns brut: {raw}",
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