# 🎯 UML AI Assistant
# DiagramFlow

> Aplicatie de modelare UML asistata de AI, construita cu Python + Streamlit + Groq API (Llama 3.3).
> Proiect demo pentru referatul **"Generative AI in UML"** — PSI, ASE CSIE Statistica, Anul 3.
> Nume aplicatie: DiagramFlow

## Functionalitati

- Chat conversational pentru generare diagrame UML din descrieri text
- Suport pentru 6 tipuri de diagrame: Class, Sequence, Use Case, Activity, State, ER
- Diagrame in stil Visual Paradigm (PlantUML) cu actori, include/extend, generalizare
- Download diagrame in format PNG, SVG, PDF
- Istoric conversatii persistent (salvat local in conversations.json)
- Redenumire conversatii
- 8 teme de culori (Violet, Blue, Green, Pink, Orange, Red, Teal, Gold)
- Sugestii de follow-up generate de AI

## Instalare si rulare

### 1. Cloneaza repository-ul
git clone https://github.com/PetreAlexandru/uml-ai-assistant.git
cd uml-ai-assistant

### 2. Creeaza un virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

### 3. Instaleaza dependentele
pip install streamlit groq requests

### 5. Ruleaza aplicatia
streamlit run app.py

Aplicatia se deschide la http://localhost:8501

## Demo online
Acceseaza aplicatia direct: https://uml-ai-assistant-fvwyf6hqsykzoujyvuxl8t.streamlit.app/

## API Key Groq (gratuit)
1. Mergi pe console.groq.com
2. Creeaza un cont si genereaza un API key
3. Introdu cheia (gsk_...) in sidebar-ul aplicatiei

## Structura proiectului
uml-ai-assistant/
├── app.py                    # Entry point — UI Streamlit
├── conversations.json        # Istoric conversatii (generat automat)
├── requirements.txt
├── .gitignore
├── README.md
└── utils/
    ├── __init__.py
    ├── constants.py          # System prompt si constante
    ├── groq_api.py           # Logica Groq API + fix PlantUML
    └── plantUML_renderer.py  # Randare PlantUML + download PNG/SVG/PDF

## Tehnologii
| Tehnologie | Rol |
|---|---|
| Python + Streamlit | Interfata utilizator |
| Groq API (Llama 3.3 70B) | Generare diagrame cu AI |
| PlantUML | Sintaxa diagrame UML |
| plantuml.com | Server public pentru randare vizuala |
```