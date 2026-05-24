create TABLE IF NOT EXISTS departments (
    id integer primary key autoincrement,
    name text not null unique,
    building text,
    established_year integer
);
create table  IF NOT EXISTS professors(
    id integer primary key autoincrement,
    name text not null,
    email text unique not null,
    department_id integer not null,
    designation text,
    foreign key (department_id) references departments(id)
);
create table IF NOT EXISTS students(
    id integer primary key autoincrement,
    name text not null,
    email text unique not null,
    age integer,
    gpa real,
    department_id integer not null,
    year_of_study integer,
    foreign key (department_id) references departments(id)
);
CREATE TABLE IF NOT EXISTS courses(
    id integer primary key autoincrement,
    name text not null,
    credits integer not null,
    department_id integer not null,
    professor_id integer,
    foreign key (department_id) references departments(id),
    foreign key (professor_id) references professors(id)
);
create table IF NOT EXISTS enrollments(
    id integer primary key autoincrement,
    student_id integer not null,
    course_id integer not null,
    grade text,
    semester text not null,
    foreign key (student_id) references students(id),
    foreign key (course_id) references courses (id),
    unique (student_id, course_id, semester)
);
