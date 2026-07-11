import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.nlp.parser import natural_language_query, parse_query, build_sql

def test(description, condition):
    status = "✅ PASS" if condition else "❌ FAIL"
    print(f"{status} — {description}")

print("\n=== QueryMind Test Suite ===\n")

# ── PARSER TESTS ──────────────────────────────────────────────
r = parse_query("show all students")
test("Detects 'students' table", "students" in r['tables'])
test("Intent is SELECT", r['intent'] == "SELECT")

r = parse_query("show students with gpa greater than 8")
test("Detects 'gpa' column", any(c[1] == 'gpa' for c in r['columns']))
test("Detects '>' operator", any(c['operator'] == '>' for c in r['conditions']))
test("Detects value '8'", any(c['value'] == '8' for c in r['conditions']))

r = parse_query("show students in Computer Science department")
test("Detects department text match", len(r['text_matches']) > 0)
test("Text match value is Computer Science", r['text_matches'][0]['value'] == "Computer Science")

# ── SQL GENERATION TESTS ───────────────────────────────────────
parsed = parse_query("show all courses")
sql, err = build_sql(parsed)
test("Generates valid SQL for courses", sql is not None)
test("SQL contains FROM courses", "courses" in sql)

parsed = parse_query("show students in Computer Science department")
sql, err = build_sql(parsed)
test("JOIN generated for department query", "JOIN" in sql)
test("WHERE clause contains Computer Science", "Computer Science" in sql)

# ── FULL PIPELINE TESTS ────────────────────────────────────────
result = natural_language_query("show all professors")
test("Pipeline success for professors query", result['success'])
test("Returns 5 professors", result['count'] == 5)

result = natural_language_query("show students with gpa greater than 8")
test("Pipeline success for GPA filter", result['success'])
test("Returns correct count (5 students)", result['count'] == 5)

result = natural_language_query("asdkjhasd")
test("Nonsense input returns failure", not result['success'])
test("Error message present", result['error'] is not None)

print("\n=== Done ===\n")