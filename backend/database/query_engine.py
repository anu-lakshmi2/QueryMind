import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from backend.database.db import execute_query, execute_write

ALLOWED_TABLES = {"students", "courses", "departments", "professors", "enrollments"}

ALLOWED_KEYWORDS = {"SELECT", "FROM", "WHERE", "JOIN", "ON", "AND", "OR",
                    "ORDER", "BY", "GROUP", "HAVING", "LIMIT", "INNER",
                    "LEFT", "RIGHT", "LIKE", "IN", "NOT", "NULL", "IS",
                    "ASC", "DESC", "COUNT", "AVG", "MAX", "MIN", "SUM", "DISTINCT"}

def is_safe_query(sql):
    sql_upper = sql.upper().strip()

    # Block write operations
    forbidden = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE", "TRUNCATE"]
    for word in forbidden:
        if word in sql_upper:
            return False, f"Operation '{word}' is not allowed."

    # Must be a SELECT query
    if not sql_upper.startswith("SELECT"):
        return False, "Only SELECT queries are allowed."

    return True, "OK"

def run_query(sql, params=()):
    is_safe, message = is_safe_query(sql)
    if not is_safe:
        return {
            "success": False,
            "error": message,
            "rows": [],
            "count": 0
        }
    try:
        rows = execute_query(sql, params)
        return {
            "success": True,
            "error": None,
            "rows": rows,
            "count": len(rows)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "rows": [],
            "count": 0
        }

def get_schema_info():
    tables = {}
    for table in ALLOWED_TABLES:
        rows = execute_query(f"PRAGMA table_info({table})")
        tables[table] = [row['name'] for row in rows]
    return tables



if __name__ == "__main__":
    # Test safe query
    result = run_query("SELECT name, gpa FROM students WHERE gpa > ?", (8.0,))
    print("Success:", result['success'])
    print("Count:", result['count'])
    for row in result['rows']:
        print(row)

    # Test blocked query
    bad = run_query("DROP TABLE students")
    print("\nBlocked query result:", bad)

    # Test schema info
    print("\nSchema:")
    schema = get_schema_info()
    for table, columns in schema.items():
        print(f"  {table}: {columns}")