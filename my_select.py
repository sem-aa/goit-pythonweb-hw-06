from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from models import Grade, Group, Student, Subject, Teacher


# Five students with the highest average grade across all subjects.
def select_1(session: Session):
    statement = (
        select(
            Student.name,
            func.round(func.avg(Grade.grade), 2).label("avg_grade"),
        )
        .join(Grade)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .limit(5)
    )
    return session.execute(statement).all()


# The student with the highest average grade in the given subject.
def select_2(session: Session, subject_id: int):
    statement = (
        select(
            Student.name,
            func.round(func.avg(Grade.grade), 2).label("avg_grade"),
        )
        .join(Grade)
        .where(Grade.subject_id == subject_id)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .limit(1)
    )
    return session.execute(statement).first()


# Average grade of each group in the given subject.
def select_3(session: Session, subject_id: int):
    statement = (
        select(
            Group.name,
            func.round(func.avg(Grade.grade), 2).label("avg_grade"),
        )
        .select_from(Group)
        .join(Student)
        .join(Grade)
        .where(Grade.subject_id == subject_id)
        .group_by(Group.id)
        .order_by(Group.name)
    )
    return session.execute(statement).all()


# Average grade across the whole grades table.
def select_4(session: Session):
    statement = select(func.round(func.avg(Grade.grade), 2))
    return session.scalar(statement)


# Subject names taught by the given teacher.
def select_5(session: Session, teacher_id: int):
    statement = (
        select(Subject.name)
        .join(Teacher)
        .where(Teacher.id == teacher_id)
        .order_by(Subject.name)
    )
    return session.scalars(statement).all()


# Student names in the given group.
def select_6(session: Session, group_id: int):
    statement = (
        select(Student.name)
        .where(Student.group_id == group_id)
        .order_by(Student.name)
    )
    return session.scalars(statement).all()


# Grades of students in the given group for the given subject.
def select_7(session: Session, group_id: int, subject_id: int):
    statement = (
        select(Student.name, Grade.grade, Grade.received_on)
        .join(Grade)
        .where(Student.group_id == group_id, Grade.subject_id == subject_id)
        .order_by(Student.name, Grade.received_on)
    )
    return session.execute(statement).all()


# Average grade given by the teacher across their subjects.
def select_8(session: Session, teacher_id: int):
    statement = (
        select(func.round(func.avg(Grade.grade), 2))
        .select_from(Grade)
        .join(Subject)
        .where(Subject.teacher_id == teacher_id)
    )
    return session.scalar(statement)


# Subject names attended by the given student.
def select_9(session: Session, student_id: int):
    statement = (
        select(Subject.name)
        .join(Grade)
        .where(Grade.student_id == student_id)
        .distinct()
        .order_by(Subject.name)
    )
    return session.scalars(statement).all()


# Subjects that the given teacher teaches to the given student.
def select_10(session: Session, student_id: int, teacher_id: int):
    statement = (
        select(Subject.name)
        .join(Grade)
        .where(
            Grade.student_id == student_id,
            Subject.teacher_id == teacher_id,
        )
        .distinct()
        .order_by(Subject.name)
    )
    return session.scalars(statement).all()


# Average grade the given teacher gives the given student.
def select_11(session: Session, teacher_id: int, student_id: int):
    statement = (
        select(func.round(func.avg(Grade.grade), 2))
        .select_from(Grade)
        .join(Subject)
        .where(
            Grade.student_id == student_id,
            Subject.teacher_id == teacher_id,
        )
    )
    return session.scalar(statement)


# Grades in a group for a subject on the latest lesson date.
def select_12(session: Session, group_id: int, subject_id: int):
    last_lesson = (
        select(func.max(Grade.received_on))
        .join(Student)
        .where(Student.group_id == group_id, Grade.subject_id == subject_id)
        .scalar_subquery()
    )
    statement = (
        select(Student.name, Grade.grade, Grade.received_on)
        .join(Grade)
        .where(
            Student.group_id == group_id,
            Grade.subject_id == subject_id,
            Grade.received_on == last_lesson,
        )
        .order_by(Student.name)
    )
    return session.execute(statement).all()
