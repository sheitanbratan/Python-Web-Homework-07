import random
import logging
from faker import Faker

from models import (engine,
                    session,
                    Base,
                    Student,
                    Group,
                    Lecturer,
                    Subject,
                    Grade)

from default_data import (groups,
                          subjects,
                          faker_func,
                          groups_filling,
                          subject_lecturers,
                          grade_table_filling)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def students_table_filling(groups_dict):
    for group_name, names in groups_dict.items():
        for name in names:
            group = session.query(Group).filter_by(group_name=group_name).first()
            student = Student(name=name, group_id=group.id)
            session.add(student)
    session.commit()


def groups_table_filling(groups_dict):
    for group_name in groups_dict.keys():
        group = Group(group_name=group_name)
        session.add(group)
    session.commit()


def lecturers_table_filling(lecturers):
    for name in lecturers:
        lecturer = Lecturer(name=name)
        session.add(lecturer)
    session.commit()


def subjects_table_filling(subjects):
    for subject_name, lecturer_name in subjects.items():
        lecturer = session.query(Lecturer).filter_by(name=lecturer_name).first()
        subject = Subject(subject=subject_name, lecturer_id=lecturer.id)
        session.add(subject)
    session.commit()


def grades_table_filling(grades_dict):
    for student_name in grades_dict.keys():
        for subject_name in grades_dict[student_name]:
            for grade, date_ in zip(grades_dict[student_name][subject_name]['grades'],
                                    grades_dict[student_name][subject_name]['date']):
                student = session.query(Student).filter_by(name=student_name).first()
                subject = session.query(Subject).filter_by(subject=subject_name).first()
                new_grade = Grade(student_id=student.id,
                                  group_id=student.group_id,
                                  subject_id=subject.id,
                                  grade=grade,
                                  date=date_)
                merged_grade = session.merge(new_grade)
                session.add(merged_grade)
    session.commit()


if __name__ == "__main__":

    """ Default data making block """
    Faker.seed(1)
    students = faker_func(random.randint(35, 50))
    groups_filling(students)
    lecturers = faker_func(5)
    lecturers_dict = subject_lecturers(lecturers)
    grades_dict = grade_table_filling()

    """ Tables filling block """
    groups_table_filling(groups)
    lecturers_table_filling(lecturers)
    students_table_filling(groups)
    subjects_table_filling(subjects)
    grades_table_filling(grades_dict)

