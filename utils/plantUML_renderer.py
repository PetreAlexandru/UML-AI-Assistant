import streamlit as st
import base64
import zlib
import requests


def encode_plantuml(text: str) -> str:
    compressed = zlib.compress(text.encode('utf-8'))
    compressed = compressed[2:-4]
    plantuml_alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_'
    standard_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    b64 = base64.b64encode(compressed).decode('ascii')
    result = b64.translate(str.maketrans(standard_alphabet, plantuml_alphabet))
    return result


def get_plantuml_url(code: str, fmt: str = "svg") -> str:
    """Returneaza URL-ul pentru diagrama in formatul dorit."""
    encoded = encode_plantuml(code)
    return f"https://www.plantuml.com/plantuml/{fmt}/{encoded}"


def download_diagram(code: str, fmt: str) -> bytes | None:
    """Descarca diagrama de la serverul PlantUML in formatul dorit."""
    try:
        url = get_plantuml_url(code, fmt)
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.content
        return None
    except Exception:
        return None


def render_plantuml(code: str, key: str, height: int = 500) -> None:
    """Randeaza diagrama PlantUML si ofera optiuni de download."""
    try:
        img_url = get_plantuml_url(code, "svg")
        html = f"""
        <div style="
            background: white;
            border-radius: 12px;
            padding: 20px;
            border: 1px solid #334155;
            text-align: center;
            overflow: auto;
        ">
            <img src="{img_url}"
                 id="{key}"
                 style="max-width:100%; height:auto;"
                 onerror="this.parentElement.innerHTML='<p style=color:#ef4444;padding:20px>Eroare la randarea diagramei. Verifica codul PlantUML.</p>'"
            />
        </div>
        """
        st.components.v1.html(html, height=height, scrolling=True)

        # Butoane download
        st.markdown("**⬇️ Descarca diagrama:**")
        col1, col2, col3 = st.columns(3)
        with col1:
            png_data = download_diagram(code, "png")
            if png_data:
                st.download_button(
                    "🖼️ PNG",
                    data=png_data,
                    file_name="diagram.png",
                    mime="image/png",
                    key=f"png_{key}",
                    use_container_width=True,
                )
        with col2:
            svg_data = download_diagram(code, "svg")
            if svg_data:
                st.download_button(
                    "📐 SVG",
                    data=svg_data,
                    file_name="diagram.svg",
                    mime="image/svg+xml",
                    key=f"svg_{key}",
                    use_container_width=True,
                )
        with col3:
            pdf_data = download_diagram(code, "pdf")
            if pdf_data:
                st.download_button(
                    "📄 PDF",
                    data=pdf_data,
                    file_name="diagram.pdf",
                    mime="application/pdf",
                    key=f"pdf_{key}",
                    use_container_width=True,
                )

    except Exception as e:
        st.error(f"Eroare renderer: {str(e)}")


# Compatibilitate cu app.py
def render_mermaid(code: str, key: str, height: int = 500) -> None:
    render_plantuml(code, key, height)