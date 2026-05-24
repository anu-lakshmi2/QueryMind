import sqlite3
import os

# Build the path to our database file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "querymind.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def create_tables(conn):
    with open(SCHEMA_PATH, "r") as f:
        schema = f.read()
    conn.executescript(schema)
    print("✅ Tables created.")

def seed_data(conn):
    cursor = conn.cursor()

    # Departments
    departments = [
        ("Computer Science", "Tech Block A", 1985),
        ("Mathematics", "Science Block B", 1970),
        ("Electronics", "Tech Block C", 1990),
        ("Physics", "Science Block A", 1965),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO departments (name, building, established_year) VALUES (?,?,?)",
        departments
    )

    # Professors
    professors = [
        ("Dr. Arjun Menon", "arjun@univ.edu", 1, "Associate Professor"),
        ("Dr. Priya Nair", "priya@univ.edu", 1, "Professor"),
        ("Dr. Ramesh Kumar", "ramesh@univ.edu", 2, "Assistant Professor"),
        ("Dr. Lakshmi Iyer", "lakshmi@univ.edu", 3, "Professor"),
        ("Dr. Suresh Pillai", "suresh@univ.edu", 4, "Associate Professor"),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO professors (name, email, department_id, designation) VALUES (?,?,?,?)",
        professors
    )

    # Students
    students = [
        ("Arun Krishnan", "arun@student.edu", 20, 8.5, 1, 2),
        ("Meera Suresh", "meera@student.edu", 21, 9.1, 1, 3),
        ("Vishnu Prasad", "vishnu@student.edu", 19, 7.8, 2, 1),
        ("Anjali Das", "anjali@student.edu", 22, 8.9, 3, 4),
        ("Rahul Nair", "rahul@student.edu", 20, 6.5, 1, 2),
        ("Sneha Menon", "sneha@student.edu", 21, 9.5, 4, 3),
        ("Kiran Thomas", "kiran@student.edu", 23, 7.2, 2, 4),
        ("Divya Pillai", "divya@student.edu", 19, 8.1, 1, 1),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO students (name, email, age, gpa, department_id, year_of_study) VALUES (?,?,?,?,?,?)",
        students
    )

    # Courses
    courses = [
        ("Data Structures", 4, 1, 1),
        ("Database Management", 4, 1, 2),
        ("Linear Algebra", 3, 2, 3),
        ("Digital Electronics", 4, 3, 4),
        ("Quantum Physics", 3, 4, 5),
        ("Operating Systems", 4, 1, 1),
        ("Calculus", 3, 2, 3),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO courses (name, credits, department_id, professor_id) VALUES (?,?,?,?)",
        courses
    )

    # Enrollments
    enrollments = [
        (1, 1, "A", "2024-S1"),
        (1, 2, "B+", "2024-S1"),
        (2, 1, "A+", "2024-S1"),
        (2, 6, "A", "2024-S1"),
        (3, 3, "B", "2024-S1"),
        (3, 7, "A", "2024-S1"),
        (4, 4, "A+", "2024-S1"),
        (5, 1, "C+", "2024-S1"),
        (5, 2, "B", "2024-S1"),
        (6, 5, "A+", "2024-S1"),
        (7, 3, "B+", "2024-S1"),
        (8, 1, "A", "2024-S1"),
        (8, 2, "A", "2024-S1"),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO enrollments (student_id, course_id, grade, semester) VALUES (?,?,?,?)",
        enrollments
    )

    conn.commit()
    print("✅ Seed data inserted.")

if __name__ == "__main__":
    conn = get_connection()
    create_tables(conn)
    seed_data(conn)
    conn.close()
    print("✅ Database ready at:", DB_PATH)