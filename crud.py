from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Grade, Group, Student, Subject, Teacher


@dataclass(frozen=True)
class ModelSpec:
    model: type
    fields: tuple[str, ...]


SPECS: dict[str, ModelSpec] = {
    "Group": ModelSpec(Group, ("name",)),
    "Teacher": ModelSpec(Teacher, ("name",)),
    "Student": ModelSpec(Student, ("name", "group_id")),
    "Subject": ModelSpec(Subject, ("name", "teacher_id")),
    "Grade": ModelSpec(Grade, ("grade", "received_on", "student_id", "subject_id")),
}


def format_row(obj: object) -> str:
    table = obj.__table__  # type: ignore[attr-defined]
    values = ", ".join(
        f"{column.name}={getattr(obj, column.name)}" for column in table.columns
    )
    return f"{type(obj).__name__}({values})"


def create(session: Session, model_name: str, values: dict) -> str:
    spec = SPECS[model_name]
    missing = [field for field in spec.fields if values.get(field) is None]
    if missing:
        raise ValueError(f"missing fields: {', '.join(missing)}")
    obj = spec.model(**{field: values[field] for field in spec.fields})
    session.add(obj)
    session.flush()
    return format_row(obj)


def list_all(session: Session, model_name: str) -> list[str]:
    spec = SPECS[model_name]
    rows = session.scalars(select(spec.model).order_by(spec.model.id)).all()
    return [format_row(row) for row in rows]


def update(session: Session, model_name: str, row_id: int, values: dict) -> str:
    spec = SPECS[model_name]
    obj = session.get(spec.model, row_id)
    if obj is None:
        raise LookupError(f"{model_name} id={row_id} not found")
    changes = {
        field: values[field]
        for field in spec.fields
        if values.get(field) is not None
    }
    if not changes:
        raise ValueError("nothing to update")
    for field, value in changes.items():
        setattr(obj, field, value)
    session.flush()
    return format_row(obj)


def remove(session: Session, model_name: str, row_id: int) -> str:
    spec = SPECS[model_name]
    obj = session.get(spec.model, row_id)
    if obj is None:
        raise LookupError(f"{model_name} id={row_id} not found")
    session.delete(obj)
    return f"{model_name} id={row_id} removed"
