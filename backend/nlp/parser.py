import re
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from backend.database.query_engine import get_schema_info

# ─── INTENT MAPPING ───────────────────────────────────────────
INTENT_KEYWORDS = {
    "SELECT": ["show", "list", "get", "find", "display", "give", "fetch", "what", "which", "who"]
}

# ─── OPERATOR MAPPING ─────────────────────────────────────────
OPERATOR_MAP = {
    "greater than": ">",
    "more than": ">",
    "above": ">",
    "higher than": ">",
    "less than": "<",
    "below": "<",
    "lower than": "<",
    "equal to": "=",
    "equals": "=",
    "is": "=",
    "not equal to": "!=",
    "at least": ">=",
    "at most": "<=",
}

# ─── COLUMN ALIASES ───────────────────────────────────────────
COLUMN_ALIASES = {
    "cgpa": "gpa",
    "marks": "gpa",
    "score": "gpa",
    "year": "year_of_study",
    "dept": "department_id",
}

def detect_intent(text):
    text_lower = text.lower()
    for intent, keywords in INTENT_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower.split():
                return intent
    return "SELECT"  # default to SELECT

def detect_tables(text):
    text_lower = text.lower()
    schema = get_schema_info()
    found_tables = []
    for table in schema.keys():
        # Check singular too — "student" should match "students"
        if table in text_lower or table.rstrip('s') in text_lower:
            found_tables.append(table)
    return found_tables if found_tables else ["students"]  # default

def detect_columns(text, tables):
    text_lower = text.lower()
    schema = get_schema_info()
    found_columns = []

    for table in tables:
        if table in schema:
            for col in schema[table]:
                if col in text_lower:
                    found_columns.append((table, col))

    # Check aliases
    for alias, real_col in COLUMN_ALIASES.items():
        if alias in text_lower:
            for table in tables:
                if table in schema and real_col in schema[table]:
                    if (table, real_col) not in found_columns:
                        found_columns.append((table, real_col))

    return found_columns

def detect_conditions(text):
    text_lower = text.lower()
    conditions = []

    for phrase, operator in OPERATOR_MAP.items():
        if phrase in text_lower:
            # Find number after the operator phrase
            pattern = phrase + r"\s+(\d+\.?\d*)"
            match = re.search(pattern, text_lower)
            if match:
                value = match.group(1)
                conditions.append({
                    "operator": operator,
                    "value": value
                })

    return conditions

def parse_query(text):
    intent = detect_intent(text)
    tables = detect_tables(text)
    columns = detect_columns(text, tables)
    conditions = detect_conditions(text)

    return {
        "intent": intent,
        "tables": tables,
        "columns": columns,
        "conditions": conditions,
        "original": text
    }

def build_sql(parsed):
    intent = parsed['intent']
    tables = parsed['tables']
    columns = parsed['columns']
    conditions = parsed['conditions']

    if not tables:
        return None, "Could not identify any table from your query."

    # Build SELECT clause
    if columns:
        col_str = ", ".join([f"{t}.{c}" for t, c in columns])
        select_clause = f"SELECT {col_str}, {tables[0]}.name"
    else:
        select_clause = f"SELECT {tables[0]}.*"

    # Build FROM clause
    from_clause = f"FROM {tables[0]}"

    # Build WHERE clause
    where_parts = []
    for condition in conditions:
        for table, col in columns:
            where_parts.append(f"{table}.{col} {condition['operator']} {condition['value']}")

    where_clause = "WHERE " + " AND ".join(where_parts) if where_parts else ""

    sql = f"{select_clause} {from_clause} {where_clause}".strip()
    return sql, None

def natural_language_query(text):
    parsed = parse_query(text)
    sql, error = build_sql(parsed)

    if error:
        return {
            "success": False,
            "error": error,
            "sql": None,
            "rows": [],
            "count": 0
        }

    from backend.database.query_engine import run_query
    result = run_query(sql)
    result["sql"] = sql
    result["parsed"] = parsed
    return result

if __name__ == "__main__":
    test_sentences = [
        "show me all students with gpa greater than 8",
        "list all courses",
        "find students with gpa less than 7",
        "show all professors",
    ]

    for sentence in test_sentences:
        print(f"\nInput: '{sentence}'")
        result = natural_language_query(sentence)
        print(f"  SQL     : {result['sql']}")
        print(f"  Success : {result['success']}")
        print(f"  Count   : {result['count']}")
        for row in result['rows']:
            print(f"    {dict(row)}")