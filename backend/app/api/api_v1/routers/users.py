from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import app.db.models as models
import app.db.schemas as schemas
from  app.core.cloud import upload_file_to_cloud
from app.db.session import get_db


users_router=app = APIRouter()


# User CRUD
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

# get courses by teacher
@app.get("/teachers/{teacher_id}/courses", response_model=List[schemas.CourseInDB])
def get_courses_by_teacher(teacher_id: int, db: Session = Depends(get_db)):
    teacher = db.query(User).filter(User.id == teacher_id, User.user_type == "teacher").first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    courses = db.query(Course).filter(Course.teacher_id == teacher_id).all()
    return courses

# get studnets by teacher and course
@app.get("/teachers/{teacher_id}/courses", response_model=List[schemas.CourseInDB])
def get_courses_by_teacher(teacher_id: int, db: Session = Depends(get_db)):
    teacher = db.query(User).filter(User.id == teacher_id, User.user_type == "teacher").first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    courses = db.query(Course).filter(Course.teacher_id == teacher_id).all()
    return courses

# get studnets by teacher and course
@app.get("/teachers/{teacher_id}/courses/{course_id}/students", response_model=List[schemas.UserBase])
def get_students_by_teacher_and_course(teacher_id: int, course_id: int, db: Session = Depends(get_db)):
    teacher = db.query(User).filter(User.id == teacher_id, User.user_type == "teacher").first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    course = db.query(Course).filter(Course.id == course_id, Course.teacher_id == teacher_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found or not taught by this teacher")

    students = db.query(User).join(CourseEnrollment).filter(CourseEnrollment.course_id == course_id).all()
    return students


@app.get("/teachers/", response_model=List[schemas.UserInDB])
def read_teachers(db: Session = Depends(get_db)):
    teachers = db.query(models.Teacher).all()
    return teachers

# Course CRUD
@app.post("/teachers/{teacher_id}/courses", response_model=schemas.CourseInDB)
def create_course_by_teacher(teacher_id: int, course: CourseCreate, db: Session = Depends(get_db)):
    teacher = db.query(User).filter(User.id == teacher_id, User.user_type == "teacher").first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    new_course = Course(**course.dict(), teacher_id=teacher_id)
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

@app.get("/courses/", response_model=List[schemas.CourseInDB])
def read_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    courses = db.query(models.Course).offset(skip).limit(limit).all()
    return courses

@app.post("/enrollments/")
def create_enrollment(enrollment: schemas.CourseEnrollmentCreate, db: Session = Depends(get_db)):
    db_enrollment = models.CourseEnrollment(
        course_id=enrollment.course_id,
        student_id=enrollment.student_id,
    )
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment

@app.post("/courses/{course_id}/enroll")
def enroll_student(
    course_id: int,
    student_id: int,
    db: Session = Depends(get_db)
):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    existing_enrollment = db.query(models.CourseEnrollment).filter(
        models.CourseEnrollment.course_id == course_id,
        models.CourseEnrollment.student_id == student_id
    ).first()
    if existing_enrollment:
        raise HTTPException(status_code=400, detail="Student already enrolled")

    enrollment = models.CourseEnrollment(
        course_id=course_id,
        student_id=student_id,
        is_payed=False
    )
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return {"detail": "Student enrolled successfully"}

@app.get("/enrollments/")
def read_enrollments(course_id: Optional[int] = None, student_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(models.CourseEnrollment)
    if course_id:
        query = query.filter(models.CourseEnrollment.course_id == course_id)
    if student_id:
        query = query.filter(models.CourseEnrollment.student_id == student_id)
    return query.all()

@app.put("/course-enrollment/{course_id}/{student_id}")
async def set_is_payed(
    course_id: int,
    student_id: int,
    is_payed: bool = True,
    db: Session = Depends(get_db),
    current_user =  schemas.UserBase
):
    if current_user.user_type != "teacher":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You must be a teacher to update payment status.",
        )

    enrollment = db.query(CourseEnrollment).filter(
        CourseEnrollment.course_id == course_id,
        CourseEnrollment.student_id == student_id
    ).first()

    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )

    enrollment.is_payed = is_payed

    db.commit()
    db.refresh(enrollment)

    return {"message": "Payment status updated successfully", "is_payed": enrollment.is_payed}


# seance CRUD

# get seance by teacher 
@app.get("/teachers/{teacher_id}/seances", response_model=List[schemas.SeanceBase])
def get_seances_by_teacher(teacher_id: int, db: Session = Depends(get_db)):
    teacher = db.query(User).filter(User.id == teacher_id, User.user_type == "teacher").first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    seances = db.query(Seance).join(Course).filter(Course.teacher_id == teacher_id).all()
    return seances

# get seance by student
@app.get("/students/{student_id}/seances", response_model=List[schemas.SeanceBase])
def get_seances_by_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(User).filter(User.id == student_id, User.user_type == "student").first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    seances = db.query(Seance).join(CourseEnrollment).filter(CourseEnrollment.student_id == student_id, CourseEnrollment.course_id == Seance.course_id).all()
    return seances

@router.post("/teachers/{teacher_id}/courses/{course_id}/seances", response_model=schemas.SeanceBase)
def add_seance_by_teacher(teacher_id: int, course_id: int, seance: SeanceCreate, db: Session = Depends(get_db)):
    teacher = db.query(User).filter(User.id == teacher_id, User.user_type == "teacher").first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    course = db.query(Course).filter(Course.id == course_id, Course.teacher_id == teacher_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found or not taught by this teacher")

    new_seance = Seance(**seance.dict(), course_id=course_id)
    db.add(new_seance)
    db.commit()
    db.refresh(new_seance)
    return new_seance
# files crud 
@router.post("/courses/{course_id}/files", response_model=schemas.FileInDB)
def create_file(
    course_id: int,
    current_user: schemas.TeacherCreate,
    db: Session = Depends(get_db)
):
    # Verify course exists and current user is the teacher
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    if course.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to add files to this course")

    # if link = upload_file_to_cloud(file_data.file, file_data.filename)

    new_file = File(
        filename=file_data.filename,
        filelink=link,
        course_id=course_id
    )

    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    return new_file

@router.get("/courses/{course_id}/files", response_model=List[schemas.FileInDB])
def get_files_by_course(
    course_id: int,
    db: Session = Depends(get_db)
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    files = db.query(File).filter(File.course_id == course_id).all()

    return files
