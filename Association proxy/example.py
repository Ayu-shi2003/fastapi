#Association proxy=it helps u to directly access the value of related table without using middle table

from sqlalchemy import create_engine,String,Integer,ForeignKey
#create_engine=connects python to database,string & integer= column data types,event=allows u to attach custom functions to db actions.
from sqlalchemy.orm import declarative_base,sessionmaker,Mapped,mapped_column,relationship
from sqlalchemy.ext.associationproxy import association_proxy

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:Ayushi%401234@localhost:5432/mydatabase" #connection path  for database
engine = create_engine(SQLALCHEMY_DATABASE_URL)   #creates engine bridge between python and database 

Session = sessionmaker(bind=engine) #sessionmaker=factory for sessions
session=Session()  #session=used to add,update,delete,commit data 

Base=declarative_base() #all database table will inherit from base class

class Student(Base):
    __tablename__ = "students10"

    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String)
    enrollments = relationship(
        "Enrollment",
        back_populates="student",
        cascade="all, delete-orphan"
    )


    courses = association_proxy("enrollments", "course")

class Course(Base):
    __tablename__ = "courses10"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)

    enrollments = relationship(
        "Enrollment",
        back_populates="course"
    )

class Enrollment(Base):
    __tablename__ = "enrollments"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students10.id"))
    course_id: Mapped[int] = mapped_column(ForeignKey("courses10.id"))

    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")

Base.metadata.create_all(engine)

# Create courses
python = Course(name="Python")
java = Course(name="Java")

# Create student
student = Student(name="Ayushi")

# Link student and courses via enrollment
student.enrollments.append(Enrollment(course=python))
student.enrollments.append(Enrollment(course=java))

session.add(student)
session.commit()

student = session.query(Student).first()

print("Student Name:", student.name)
print("Courses enrolled:")

for course in student.courses:
    print("-", course.name)
