from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas
from app.core.security import get_password_hash
from app.db.session import get_db
from app.api.api_v1.routers.users import users_router as app





def get_user_by_email(db: Session, email: str) -> schemas.UserInDB:
    return db.query(models.User).filter(models.User.email == email).first()
@app.post("/users/", response_model=schemas.UserInDB)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=get_password_hash(user.password),  # Implement password hashing
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        user_type='user'
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/", response_model=List[schemas.UserInDB])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

@app.get("/users/{user_id}", response_model=schemas.UserInDB)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Teacher CRUD
@app.post("/teachers/", response_model=schemas.UserInDB)
def create_teacher(teacher: schemas.TeacherCreate, db: Session = Depends(get_db)):
    db_teacher = models.Teacher(
        email=teacher.email,
        first_name=teacher.first_name,
        last_name=teacher.last_name,
        hashed_password=get_password_hash(teacher.password),
        subject=teacher.subject,
        is_active=teacher.is_active,
        is_superuser=teacher.is_superuser,
        user_type='teacher'
    )
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher

@app.get("/teachers/", response_model=List[schemas.UserInDB])
def read_teachers(db: Session = Depends(get_db)):
    teachers = db.query(models.Teacher).all()
    return teachers

# Course CRUD
@app.post("/courses/", response_model=schemas.CourseInDB)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    db_course = models.Course(
        name=course.name,
        date=course.date,
        teacher_id=course.teacher_id
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@app.get("/courses/", response_model=List[schemas.CourseInDB])
def read_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    courses = db.query(models.Course).offset(skip).limit(limit).all()
    return courses

# Course Enrollment CRUD
@app.post("/enrollments/")
def create_enrollment(enrollment: schemas.CourseEnrollmentCreate, db: Session = Depends(get_db)):
    db_enrollment = models.CourseEnrollment(
        course_id=enrollment.course_id,
        student_id=enrollment.student_id,
        grade=enrollment.grade
    )
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment

@app.get("/enrollments/")
def read_enrollments(course_id: Optional[int] = None, student_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(models.CourseEnrollment)
    if course_id:
        query = query.filter(models.CourseEnrollment.course_id == course_id)
    if student_id:
        query = query.filter(models.CourseEnrollment.student_id == student_id)
    return query.all()


"""

def get_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_user_by_email(db: Session, email: str) -> schemas.UserBase:
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(
    db: Session, skip: int = 0, limit: int = 100
) -> t.List[schemas.UserOut]:
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    return user


def edit_user(
    db: Session, user_id: int, user: schemas.UserEdit
) -> schemas.User:
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    update_data = user.dict(exclude_unset=True)

    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(user.password)
        del update_data["password"]

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
"""
