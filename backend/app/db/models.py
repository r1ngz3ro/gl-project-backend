from sqlalchemy import Column, Integer, String, Boolean, Date ,DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from typing import Optional, List
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    user_type = Column(String, nullable=False)
    
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': user_type
    }

class Teacher(User):
    __mapper_args__ = {
        'polymorphic_identity': 'teacher'
    }
    subject = Column(String)
    courses = relationship("Course", back_populates="teacher")

class Student(User):
    __mapper_args__ = {
        'polymorphic_identity': 'student'
    }
    enrollments = relationship("CourseEnrollment", back_populates="student")

class File(Base):
    __tablename__ = 'files'
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    filelink = Column(String, nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    
    course = relationship("Course", back_populates="files")

class Course(Base):
    __tablename__ = 'courses'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    teacher_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    start = Column(DateTime, nullable=False, default=datetime.date.today())
    end = Column(DateTime, nullable=False, default=datetime.date.today())
    
    teacher = relationship("Teacher", back_populates="courses")
    enrollments = relationship("CourseEnrollment", back_populates="course")
    seances = relationship("Seance", back_populates="course", cascade="all, delete-orphan")
    files = relationship("File", back_populates="course")  # New relationship

class Seance(Base):
    __tablename__ = "seances"

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)  # Foreign key linking to Course
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    location = Column(String, nullable=False)

    # Relationship: A seance belongs to one course
    course = relationship("Course", back_populates="seances")

class CourseEnrollment(Base):
    __tablename__ = 'course_enrollments'
    
    course_id = Column(Integer, ForeignKey('courses.id'), primary_key=True)
    student_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    is_payed = Column(Boolean, nullable=True, default=False)
    
    course = relationship("Course", back_populates="enrollments")
    student = relationship("Student", back_populates="enrollments")



