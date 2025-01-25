from pydantic import BaseModel, EmailStr,ConfigDict
from typing import Optional, List
import typing as t
from datetime import date ,datetime

class UserBase(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: int
    user_type: str

    class Config:
        orm_mode = True

class TeacherCreate(UserCreate):
    subject: Optional[str] = None

class FileBase(BaseModel):
    filename: str
    filelink: str
    course_id: int
    model_config = ConfigDict(from_attributes=True)

class FileCreate(FileBase):
    pass

class FileInDB(FileBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class SeanceBase(BaseModel):
    id: int
    course_id: int
    start_time: datetime
    end_time: datetime
    location: str

    class Config:
        orm_mode = True

class CourseBase(BaseModel):
    name: str
    teacher_id: Optional[int] = None
    start: datetime
    end: datetime
    model_config = ConfigDict(from_attributes=True)

class CourseCreate(CourseBase):
    start: datetime = datetime.now()
    end: datetime = datetime.now()

class CourseInDB(CourseBase):
    id: int
    teacher: Optional[UserBase] = None
    seances: List[SeanceBase] = []
    files: List[FileInDB] = []
    model_config = ConfigDict(from_attributes=True)


class CourseEnrollmentCreate(BaseModel):
    course_id: int
    student_id: int
    is_payed : Optional[bool] = False

