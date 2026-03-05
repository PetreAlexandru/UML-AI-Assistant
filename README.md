# 🎯 UML AI Assistant

> Aplicație de modelare UML asistată de AI, construită cu Python + Streamlit + Groq API (Llama 3).  
> Proiect demo pentru referatul **"Generative AI în UML"** — PSI, ASE CSIE Statistică, Anul 3.

## 🚀 Instalare și rulare

### 1. Clonează repository-ul
```bash
git clone https://github.com/PetreAlexandru/uml-ai-assistant.git
cd uml-ai-assistant
```

### 2. Creează un virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Instalează dependențele
```bash
pip install streamlit groq
```

### 4. Rulează aplicația
```bash
streamlit run app.py
```
Aplicația se deschide automat la `http://localhost:8501`

## 🔑 API Key Groq (gratuit)
1. Mergi pe [console.groq.com](https://console.groq.com)
2. Creează un cont și generează un API key
3. Introdu cheia (`gsk_...`) în sidebar-ul aplicației

## 🗂️ Structura proiectului
```
uml-ai-assistant/
├── app.py                   # Entry point — UI Streamlit
├── requirements.txt         # Dependențe Python
├── .gitignore
├── README.md
└── utils/
    ├── __init__.py          # Export-uri principale
    ├── constants.py         # Constante, texte, system prompt
    ├── groq_api.py        # Logica de comunicare cu Groq API
    └── mermaid_renderer.py  # Randarea vizuală a diagramelor
├── assets/ 
```

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
- **Streamlit** — framework web pentru interfața utilizator
- **Groq API (Llama 3.3 70B)** — modelul AI care generează diagramele
- **Mermaid.js** — librărie JavaScript pentru randarea vizuală UML