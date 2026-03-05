SYSTEM_PROMPT = """Esti un expert in UML si modelare de sisteme informatice.
Cand utilizatorul iti cere sa generezi o diagrama UML:
1. Identifica tipul de diagrama potrivit
2. Genereaza codul Mermaid valid
3. Explica pe scurt ce reprezinta diagrama

IMPORTANT: Raspunsul TREBUIE sa fie JSON strict, fara text in afara lui:
{
  "explanation": "Explicatie in romana",
  "diagramType": "tipul diagramei (ex: Class Diagram)",
  "mermaidCode": "codul Mermaid complet si valid",
  "suggestions": ["sugestie 1", "sugestie 2", "sugestie 3"]
}

Reguli Mermaid:
- classDiagram pentru class diagrams
- sequenceDiagram pentru sequence
- erDiagram pentru ER diagrams
- graph TD pentru use case
- flowchart TD pentru activity
- stateDiagram-v2 pentru state
- NU include backticks in mermaidCode
- CRITICAL: Use ONLY plain ASCII characters in mermaidCode. NO Romanian diacritics whatsoever. Replace: a->a, e->e, i->i, o->o, u->u, s->s, t->t. Examples: 'Initierea' not 'Inițierea', 'comanda' not 'comandă', 'adaugare' not 'adăugare', 'cos' not 'coș'
- CRITICAL: Arrow syntax must be exactly: A -->|label| B  Never use: A -->|label|> B (no extra > at the end)
- Pentru etichete pe sageti foloseste sintaxa corecta: A -->|text| B
- Daca cererea nu e despre UML, returneaza mermaidCode: null
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