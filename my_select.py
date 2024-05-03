from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from models import (session,
                    Student,
                    Grade,
                    Subject,
                    Lecturer,
                    Group)


def select_1():
    """Знайти 5 студентів із найбільшим середнім балом з усіх предметів."""
    query = session.query(Student, func.avg(Grade.grade).label('average_grade')) \
        .join(Grade, Grade.student_id == Student.id) \
        .group_by(Student.id) \
        .order_by(func.avg(Grade.grade).desc()) \
        .limit(5)
    result = [(student.name, round(average_grade, 2)) for student, average_grade in query.all()]
    return result


def select_2(subject_name):
    """Знайти студента із найвищим середнім балом з певного предмета."""
    query = session.query(Student, func.avg(Grade.grade).label('average_grade')) \
        .join(Grade, Grade.student_id == Student.id) \
        .join(Subject, Subject.id == Grade.subject_id) \
        .filter(Subject.subject == subject_name) \
        .group_by(Student.id) \
        .order_by(func.avg(Grade.grade).desc()) \
        .first()
    student_name, average_grade = query[0].name, round(query[1], 2)
    return f'Найвищий середній бал з {subject_name}: {student_name} | {average_grade}'


def select_3(subject_name):
    """Знайти середній бал у групах з певного предмета."""
    query = session.query(Group.group_name, func.avg(Grade.grade).label('average_grade')) \
        .join(Grade) \
        .join(Subject) \
        .filter(Subject.subject == subject_name) \
        .group_by(Group.group_name) \
        .all()
    return [f'Group: {i[0]}, grade: {round(i[1], 3)}' for i in query]


def select_4():
    """Знайти середній бал на потоці (по всій таблиці оцінок)."""
    query = session.query(func.avg(Grade.grade).label('average_grade')).scalar()
    return f'Cередній бал на потоці: {round(query, 3)}'


def select_5(lecturer_id):
    """Знайти які курси читає певний викладач."""
    query = session.query(Subject.subject) \
        .filter(Subject.lecturer_id == lecturer_id) \
        .distinct() \
        .all()
    return [course.subject for course in query]


def select_6(group_id):
    """Знайти список студентів у певній групі."""
    query = session.query(Student.name) \
        .filter(Student.group_id == group_id) \
        .all()
    return [student.name for student in query]


def select_7(group_id, subject_name):
    """Знайти оцінки студентів у окремій групі з певного предмета."""
    query = session.query(Student.name, Grade.grade) \
        .join(Grade) \
        .join(Subject) \
        .filter(Student.group_id == group_id, Subject.subject == subject_name) \
        .all()
    return query


def select_8(lecturer_id):
    """Знайти середній бал, який ставить певний викладач зі своїх предметів."""
    query = session.query(func.avg(Grade.grade).label('average_grade')) \
        .join(Subject) \
        .join(Lecturer) \
        .filter(Subject.lecturer_id == lecturer_id) \
        .scalar()
    return query


def select_9(student_id):
    """Знайти список курсів, які відвідує певний студент."""
    query = session.query(Subject.subject) \
        .join(Grade) \
        .join(Student) \
        .filter(Student.id == student_id) \
        .distinct() \
        .all()
    return [course.subject for course in query]


def select_10(student_id, lecturer_id):
    """Список курсів, які певному студенту читає певний викладач."""
    query = session.query(Subject.subject) \
        .join(Grade) \
        .join(Student) \
        .join(Lecturer) \
        .filter(Student.id == student_id, Lecturer.id == lecturer_id) \
        .distinct() \
        .all()
    return [course.subject for course in query]
