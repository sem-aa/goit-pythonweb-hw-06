from __future__ import annotations

from faker import Faker
from sqlalchemy.orm import Session

from db import get_session
from models import Grade, Group, Student, Subject, Teacher

GROUPS = ["Group 1", "Group 2", "Group 3"]
SUBJECT_NAMES = [
    "Mathematics",
    "Physics",
    "Chemistry",
    "History",
    "Literature",
    "English",
    "Biology",
    "Computer Science",
]
STUDENTS = 40
TEACHERS = 4
SUBJECTS = 6
MAX_GRADES_PER_STUDENT = 20


def seed(session: Session) -> None:
    fake = Faker("en_US")
    Faker.seed(7)

    groups = [Group(name=name) for name in GROUPS]
    session.add_all(groups)

    teachers = [Teacher(name=fake.name()) for _ in range(TEACHERS)]
    session.add_all(teachers)

    subject_names = fake.random_elements(SUBJECT_NAMES, length=SUBJECTS, unique=True)
    subjects: list[Subject] = []
    for index, name in enumerate(subject_names):
        subject = Subject(name=name)
        teachers[index % len(teachers)].subjects.append(subject)
        subjects.append(subject)

    students: list[Student] = []
    for _ in range(STUDENTS):
        student = Student(name=fake.name())
        fake.random_element(groups).students.append(student)
        students.append(student)

    for student in students:
        for _ in range(fake.random_int(1, MAX_GRADES_PER_STUDENT)):
            student.grades.append(
                Grade(
                    grade=fake.random_int(1, 100),
                    received_on=fake.date_between(start_date="-1y", end_date="today"),
                    subject=fake.random_element(subjects),
                )
            )


if __name__ == "__main__":
    with get_session() as session:
        seed(session)
