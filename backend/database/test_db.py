import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from backend.database.db import execute_query

# Test 1 — Get all students
students = execute_query("SELECT name, gpa FROM students WHERE gpa > 8")
print("\n--- Students with GPA > 8 ---")
for s in students:
    print(s['name'], "-", s['gpa'])

# Test 2 — Parameterized query
dept_students = execute_query("""
    SELECT students.name, students.gpa, departments.name as dept
    FROM students
    JOIN departments ON students.department_id = departments.id
    WHERE departments.name = ?
""", ("Computer Science",))

print("\n--- CS Department Students ---")
for s in dept_students:
    print(s['name'], "-", s['gpa'], "-", s['dept'])