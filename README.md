# QueryMind 🧠
### Natural Language to SQL Query Engine

QueryMind lets you query a database using plain English. 
Type "show students with GPA greater than 8" and get real results instantly — 
no SQL knowledge required.

**Live Demo:** [coming soon after deployment]  
**Built by:** Anulakshmi | [github.com/anu-lakshmi2](https://github.com/anu-lakshmi2)

---

## What It Does

- Accepts natural language questions about a university database
- Parses intent, tables, columns, and conditions from plain English
- Dynamically generates and safely executes SQL queries
- Displays results in a clean table with CSV export
- Shows the generated SQL and a plain-English explanation of the query

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI (Python) |
| Database | SQLite with normalized schema |
| NLP | Rule-based parser with spaCy |
| Frontend | Vanilla HTML, CSS, JavaScript |
| Deployment | Render.com (coming soon) |

---

## Architecture

User Input (plain English)
↓
NLP Parser (parser.py)

Intent detection
Table & column extraction
Condition parsing
Text match detection
↓
SQL Generator (build_sql)
Dynamic JOIN generation
Parameterized queries
Safety validation
↓
Query Engine (query_engine.py)
SQL injection protection
Connection management
Rollback on failure
↓
FastAPI Backend (/query endpoint)
↓
Frontend (results table + SQL display)

---

## Database Schema

5-table normalized university database (3NF):

- `departments` — faculty departments
- `professors` — teaching staff, linked to departments
- `students` — enrolled students with GPA and year
- `courses` — offered courses with credits
- `enrollments` — junction table linking students ↔ courses

---

## Sample Queries You Can Try

show all students
list courses with credits above 3
show students with gpa greater than 8
find students in Computer Science department
show all professors
list students with age above 20

---

## Known Limitations

- Numeric values must be written as digits (e.g. "8", not "eight")
- Complex multi-condition queries ("gpa > 8 AND age < 22") not yet supported
- Limited to the university database schema (not a general-purpose engine)

---

## Setup & Run Locally

```bash
# Clone the repo
git clone https://github.com/anu-lakshmi2/QueryMind.git
cd QueryMind

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Seed the database
python backend/database/seed.py

# Run backend
uvicorn backend.main:app --reload

# Run frontend (new terminal)
cd frontend
python -m http.server 5500

# Open browser at http://127.0.0.1:5500
```

---

## Running Tests

```bash
python tests/test_queries.py
```

17/17 tests passing ✅

---

## Project Structure

QueryMind/
├── backend/
│   ├── database/
│   │   ├── schema.sql        # Normalized DB schema
│   │   ├── seed.py           # Sample data loader
│   │   ├── db.py             # Connection manager
│   │   └── query_engine.py   # Safe query executor
│   ├── nlp/
│   │   └── parser.py         # NLP → SQL pipeline
│   └── main.py               # FastAPI app
├── frontend/
│   ├── index.html
│   ├── styl.css
│   └── script.js
├── tests/
│   └── test_queries.py
└── README.md

---