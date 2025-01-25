#!/usr/bin/env python3

from app.db.session import get_db
from app.db.crud import create_user , create_course
from app.db.schemas import UserCreate , CourseCreate
from app.db.session import SessionLocal
import datetime


def init() -> None:
    db = SessionLocal()
    create_course(
        db,
        CourseCreate(
            name="tbanyit",
            start=datetime.date.fromisoformat("2021-09-01"),
            teacher_id=1,
        ),
    )

"""    create_user(
        db,
        UserCreate(
            email="admin@name.com",
            password="fckyou",
            is_active=True,
            is_superuser=True,
        ),
    ) """



if __name__ == "__main__":
    print("Creating superuser admin@name.com")
    init()
    print("Superuser created")
