SYSTEM_PROMPT = """Ești un expert în UML și modelare de sisteme informatice.
Când utilizatorul îți cere să generezi o diagramă UML:
1. Identifică tipul de diagramă potrivit
2. Generează codul Mermaid valid
3. Explică pe scurt ce reprezintă diagrama

IMPORTANT: Răspunsul TREBUIE să fie JSON strict, fără text în afara lui:
{
  "explanation": "Explicație în română",
  "diagramType": "tipul diagramei (ex: Class Diagram)",
  "mermaidCode": "codul Mermaid complet și valid",
  "suggestions": ["sugestie 1", "sugestie 2", "sugestie 3"]
}

Reguli Mermaid:
- classDiagram pentru class diagrams
- sequenceDiagram pentru sequence
- graph TD pentru use case
- flowchart TD pentru activity
- stateDiagram-v2 pentru state
- NU include backticks în mermaidCode
- Dacă cererea nu e despre UML, returnează mermaidCode: null
"""

DIAGRAM_TYPES = [
    ("🏗️", "Class Diagram",    "Structura claselor și relațiilor"),
    ("🔄", "Sequence Diagram", "Interacțiuni în timp"),
    ("👤", "Use Case Diagram", "Cerințe funcționale"),
    ("⚡", "Activity Diagram", "Fluxuri de activități"),
    ("🔀", "State Diagram",    "Tranziții de stare"),
    ("🗄️", "ER Diagram",       "Structura bazei de date"),
]

BADGE_COLORS = {
    "Class Diagram":    ("#6366f1", "#e0e7ff"),
    "Sequence Diagram": ("#0ea5e9", "#e0f2fe"),
    "Use Case Diagram": ("#10b981", "#d1fae5"),
    "Activity Diagram": ("#f59e0b", "#fef3c7"),
    "State Diagram":    ("#ec4899", "#fce7f3"),
    "ER Diagram":       ("#8b5cf6", "#ede9fe"),
}

STARTER_SUGGESTIONS = [
    "Generează o diagramă de clase pentru un sistem bancar",
    "Creează un Use Case diagram pentru o aplicație de e-commerce",
    "Diagramă de secvență pentru autentificare cu JWT",
    "Diagramă de activitate pentru procesul de comandă online",
    "Diagramă de stare pentru un cont de utilizator",
    "Diagramă ER pentru o bază de date universitară",
]