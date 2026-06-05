import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "querymind.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("\n--- STUDENTS ---")
cursor.execute("SELECT name, gpa, year_of_study FROM students")
for row in cursor.fetchall():
    print(row)

print("\n--- COURSES ---")
cursor.execute("SELECT name, credits FROM courses")
for row in cursor.fetchall():
    print(row)

print("\n--- ENROLLMENTS WITH NAMES ---")
cursor.execute("""
    SELECT students.name, courses.name, enrollments.grade
    FROM enrollments
    JOIN students ON enrollments.student_id = students.id
    JOIN courses ON enrollments.course_id = courses.id
""")
for row in cursor.fetchall():
    print(row)


print("\n--- STUDENTS WITH GPA GREATER THAN 8 ---")
cursor.execute("""
    SELECT students.name, students.gpa, departments.name
    FROM students join departments on students.department_id = departments.id
    WHERE students.gpa > 8 AND departments.name = 'Computer Science'
""")
for row in cursor.fetchall():
    print(row)

conn.close()