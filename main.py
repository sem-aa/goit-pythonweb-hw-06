import argparse
import sys
from datetime import date

from sqlalchemy.exc import IntegrityError

from crud import SPECS, create, list_all, remove, update
from db import get_session


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="CRUD for the university database")
    parser.add_argument(
        "-a",
        "--action",
        required=True,
        choices=["create", "list", "update", "remove"],
    )
    parser.add_argument("-m", "--model", required=True, choices=sorted(SPECS))
    parser.add_argument("--id", type=int)
    parser.add_argument("-n", "--name")
    parser.add_argument("--group-id", type=int)
    parser.add_argument("--teacher-id", type=int)
    parser.add_argument("--student-id", type=int)
    parser.add_argument("--subject-id", type=int)
    parser.add_argument("--grade", type=int)
    parser.add_argument("--received-on", type=date.fromisoformat)
    return parser


def values_from(args: argparse.Namespace) -> dict:
    return {
        "name": args.name,
        "group_id": args.group_id,
        "teacher_id": args.teacher_id,
        "student_id": args.student_id,
        "subject_id": args.subject_id,
        "grade": args.grade,
        "received_on": args.received_on,
    }


def main() -> None:
    args = build_parser().parse_args()
    values = values_from(args)
    try:
        with get_session() as session:
            if args.action == "create":
                print(create(session, args.model, values))
            elif args.action == "list":
                rows = list_all(session, args.model)
                print("\n".join(rows) if rows else "(empty)")
            elif args.action == "update":
                if args.id is None:
                    raise ValueError("update requires --id")
                print(update(session, args.model, args.id, values))
            else:
                if args.id is None:
                    raise ValueError("remove requires --id")
                print(remove(session, args.model, args.id))
    except (ValueError, LookupError) as error:
        print(error, file=sys.stderr)
        sys.exit(1)
    except IntegrityError:
        print("database rejected the row: check ids and unique names", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
