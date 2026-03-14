import re
import json
import streamlit as st
from groq import Groq
from utils.constants import SYSTEM_PROMPT


def fix_plantuml(code: str) -> str:
    if not code:
        return code

    code = code.replace('\\n', '\n')
    code = code.replace('\\t', '    ')

    # Fix note pe mai multe linii
    code = re.sub(
        r'note (right|left|top|bottom) of (\w+) : (.+?)\n(.+?)\n',
        r'note \1 of \2 : \3 \4\n', code
    )

    if '@startuml' not in code:
        code = '@startuml\n' + code
    if '@enduml' not in code:
        code = code + '\n@enduml'

    if 'skinparam' not in code:
        code = code.replace('@startuml\n',
            '@startuml\n'
            'skinparam backgroundColor white\n'
            'skinparam classBackgroundColor #f8fafc\n'
            'skinparam classBorderColor #6366f1\n'
            'skinparam classArrowColor #334155\n'
            'skinparam classFontColor #1e293b\n'
            'skinparam actorBackgroundColor #dbeafe\n'
            'skinparam usecaseBackgroundColor #dbeafe\n'
            'skinparam sequenceParticipantBackgroundColor #dbeafe\n'
            'skinparam stateBackgroundColor #dbeafe\n'
            'skinparam entityBackgroundColor #dbeafe\n'
        )

    return code.strip()


def call_claude(user_text: str) -> dict:
    api_key = st.session_state.get("api_key", "")

    if not api_key:
        return {
            "explanation": "⚠️ Introdu API key-ul Groq in sidebar.",
            "diagramType": None,
            "plantUMLCode": None,
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
            temperature=0.2,
            max_tokens=2000,
        )

        raw = response.choices[0].message.content
        clean = re.sub(r"```json|```", "", raw).strip()
        start = clean.find('{')
        end = clean.rfind('}')
        if start != -1 and end != -1:
            clean = clean[start:end+1]

        data = json.loads(clean)

        if data.get("plantUMLCode"):
            data["plantUMLCode"] = fix_plantuml(data["plantUMLCode"])

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
            "plantUMLCode": None,
            "suggestions": [],
        }
    except Exception as e:
        return {
            "explanation": f"❌ Eroare API: {str(e)}",
            "diagramType": None,
            "plantUMLCode": None,
            "suggestions": [],
        }