import re
import json
import streamlit as st
from groq import Groq
from utils.constants import SYSTEM_PROMPT


def fix_mermaid(code: str) -> str:
    if not code:
        return code
    # Convertim \n literal in newline real (in caz ca json.loads nu l-a procesat)
    code = code.replace('\\n', '\n')
    code = code.replace('\\t', '    ')
    # Fix -->|text|> B -> -->|text| B
    code = re.sub(r'\|>\s*([A-Za-z])', r'| \1', code)
    return code.strip()


def call_claude(user_text: str) -> dict:
    """
    Trimite un mesaj catre Groq (Llama 3) si returneaza raspunsul parsat ca dict.
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

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

        for msg in st.session_state.api_history:
            messages.append({
                "role": msg["role"] if msg["role"] == "user" else "assistant",
                "content": msg["content"]
            })

        messages.append({"role": "user", "content": user_text})

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.3,
            max_tokens=2000,
        )

        raw = response.choices[0].message.content
        
        # Extragem JSON-ul din raspuns
        clean = re.sub(r"```json|```", "", raw).strip()
        start = clean.find('{')
        end = clean.rfind('}')
        if start != -1 and end != -1:
            clean = clean[start:end+1]
        
        # Uneori Llama pune \n literal ca text in JSON
        # json.loads il trateaza corect, dar verificam si fix_mermaid
        data = json.loads(clean)

        # Aplicam fix-ul pe codul Mermaid
        if data.get("mermaidCode"):
            data["mermaidCode"] = fix_mermaid(data["mermaidCode"])

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