import streamlit as st


def render_mermaid(code: str, key: str, height: int = 420) -> None:
    """
    Randează o diagramă Mermaid într-un iframe HTML.

    Args:
        code:   codul Mermaid (fără backticks)
        key:    ID unic pentru elementul HTML
        height: înălțimea în pixeli a containerului
    """
    html = f"""
    <div style="
        background: #1e293b;
        border-radius: 12px;
        padding: 16px;
        border: 1px solid #334155;
    ">
        <div class="mermaid" id="{key}">
{code}
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script>
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'dark',
            securityLevel: 'loose'
        }});
    </script>
    """
    st.components.v1.html(html, height=height, scrolling=True)