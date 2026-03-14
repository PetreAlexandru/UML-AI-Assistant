import streamlit as st
import base64
import zlib


def encode_plantuml(text: str) -> str:
    """
    Encodeaza codul PlantUML in formatul acceptat de serverul public.
    Foloseste compresia zlib + encoding specific PlantUML.
    """
    # Compresie zlib
    compressed = zlib.compress(text.encode('utf-8'))
    # Eliminam header-ul zlib (primii 2 bytes) si checksum-ul (ultimii 4 bytes)
    compressed = compressed[2:-4]

    # Alphabet specific PlantUML (diferit de base64 standard)
    plantuml_alphabet = (
        '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_'
    )
    standard_alphabet = (
        'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    )

    # Encodam in base64 standard
    b64 = base64.b64encode(compressed).decode('ascii')

    # Translatam in alphabet PlantUML
    result = b64.translate(str.maketrans(standard_alphabet, plantuml_alphabet))
    return result


def render_plantuml(code: str, key: str, height: int = 500) -> None:
    """
    Randeaza o diagrama PlantUML folosind serverul public plantuml.com.

    Args:
        code:   codul PlantUML (cu @startuml/@enduml)
        key:    ID unic pentru element
        height: inaltimea containerului
    """
    try:
        encoded = encode_plantuml(code)
        img_url = f"https://www.plantuml.com/plantuml/svg/{encoded}"

        html = f"""
        <div style="
            background: #1e293b;
            border-radius: 12px;
            padding: 20px;
            border: 1px solid #334155;
            text-align: center;
            overflow: auto;
        ">
            <img src="{img_url}"
                 id="{key}"
                 style="max-width:100%; height:auto;"
                 onerror="this.parentElement.innerHTML='<p style=color:#ef4444>Eroare la randarea diagramei. Verifica codul PlantUML.</p>'"
            />
        </div>
        """
        st.components.v1.html(html, height=height, scrolling=True)

    except Exception as e:
        st.error(f"Eroare renderer: {str(e)}")


# Pastram si numele vechi pentru compatibilitate
def render_mermaid(code: str, key: str, height: int = 500) -> None:
    render_plantuml(code, key, height)