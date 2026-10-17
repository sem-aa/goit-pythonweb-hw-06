from __future__ import annotations

from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, String, MetaData

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=NAMING_CONVENTION)


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)

    students: Mapped[list[Student]] = relationship(
        back_populates="group",
        cascade="all, delete-orphan",
    )


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))

    group_id: Mapped[int] = mapped_column(
        ForeignKey("groups.id", ondelete="CASCADE"),
        index=True,
    )

    group: Mapped[Group] = relationship(back_populates="students")
    grades: Mapped[list[Grade]] = relationship(
        back_populates="student",
        cascade="all, delete-orphan",
    )


class Teacher(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))

    subjects: Mapped[list[Subject]] = relationship(
        back_populates="teacher",
        cascade="all, delete-orphan",
    )


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))

    teacher_id: Mapped[int] = mapped_column(
        ForeignKey("teachers.id", ondelete="CASCADE"),
        index=True,
    )

    teacher: Mapped[Teacher] = relationship(back_populates="subjects")
    grades: Mapped[list[Grade]] = relationship(
        back_populates="subject",
        cascade="all, delete-orphan",
    )


class Grade(Base):
    __tablename__ = "grades"

    id: Mapped[int] = mapped_column(primary_key=True)
    grade: Mapped[int] = mapped_column(Integer)
    received_on: Mapped[date] = mapped_column(Date)

    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id", ondelete="CASCADE"),
        index=True,
    )
    subject_id: Mapped[int] = mapped_column(
        ForeignKey("subjects.id", ondelete="CASCADE"),
        index=True,
    )

    student: Mapped[Student] = relationship(back_populates="grades")
    subject: Mapped[Subject] = relationship(back_populates="grades")
