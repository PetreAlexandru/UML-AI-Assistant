# 🎯 UML AI Assistant

> Aplicație de modelare UML asistată de AI, construită cu Python + Streamlit + Claude API.  
> Proiect demo pentru referatul **"Generative AI în UML"** — PSI, ASE CSIE Statistică, Anul 3.

## 🚀 Instalare și rulare

### 1. Clonează repository-ul
git clone https://github.com/PetreAlexandru/uml-ai-assistant.git
cd uml-ai-assistant

### 2. Creează un virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

### 3. Instalează dependențele
pip install -r requirements.txt

### 4. Rulează aplicația
streamlit run app.py

Aplicația se deschide automat la http://localhost:8501

## 🔑 API Key Anthropic
1. Mergi pe [console.anthropic.com](https://console.anthropic.com)
2. Creează un cont și generează un API key
3. Introdu cheia în sidebar-ul aplicației (nu se salvează nicăieri)

## 🗂️ Structura proiectului
uml-ai-assistant/
├── app.py                   # Entry point — UI Streamlit
├── requirements.txt         # Dependențe Python
├── .gitignore
├── README.md
└── utils/
    ├── __init__.py          # Export-uri principale
    ├── constants.py         # Constante, texte, configurări
    ├── claude_api.py        # Logica de comunicare cu API-ul Anthropic
    └── mermaid_renderer.py  # Randarea vizuală a diagramelor

## 📊 Tipuri de diagrame suportate
| Tip | Descriere |
|-----|-----------|
| 🏗️ Class Diagram | Structura claselor și relațiile dintre ele |
| 🔄 Sequence Diagram | Interacțiuni între componente în timp |
| 👤 Use Case Diagram | Cerințele funcționale ale sistemului |
| ⚡ Activity Diagram | Fluxuri de activități și procese |
| 🔀 State Diagram | Tranziții de stare ale unui obiect |
| 🗄️ ER Diagram | Structura bazei de date relaționale |

## 🛠️ Tehnologii
- **Python** — limbaj de programare
- **Streamlit** — framework web rapid pentru aplicații de date
- **Anthropic Claude API** — modelul AI care generează diagramele
- **Mermaid.js** — librărie JavaScript pentru randarea vizuală UML
