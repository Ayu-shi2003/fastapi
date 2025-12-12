from sqlalchemy import String,Integer,ForeignKey,create_engine,Table,Column #foreign key=creates reference from one table to another
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,relationship,sessionmaker

# Database URL
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:Ayushi%401234@localhost:5432/mydatabase" #connection path  for database
engine = create_engine(SQLALCHEMY_DATABASE_URL)  #main connection to talk with database
#create_engine reads our connection url that is pw,host,user,port and return an engine object
#engine is object that knows how to talk with DB driver as it knows how to call database connection.
#basically in easy terms engine means it connects our python code  and postgressql database without engine we cant connect to database

Session = sessionmaker(bind=engine)  #sessionmaker creates a class that makes session object
#Session means create session

session=Session()   #session is the object which is used for insert,update,delete query data 
#main tool to talk to the database 

#engine=connect to database
#Session=blueprint to create session
#session=actual object that talks to db



class Base(DeclarativeBase):  #All tables that we will be creating in database will inherit from base class means starts with this base class due to this it will tell sqlalchemy that these class will become the database table
    pass

#This is called association table or can say middle table that connects many students<-> many courses
student_course=Table(                    #creates a table object not model class
    "student_course",        #for database table name so basically tablename=student_course
    Base.metadata,           #resgisters in sqlalchmey for generating this table in database
    Column("Student_id",ForeignKey("students.id"),primary_key=True),
    #student_id=creates columname in database,foreignkey=pointing to students table id
    Column("course_id",ForeignKey("courses.id"),primary_key=True)
    #course_id=columname in database,foreignkey=pointing courses table id or linking to courseid
    #primary key is used for unique values stored i.e each(student,course) is unique in the table
)

class Student(Base): #models
    __tablename__="students"  #tablename

    id:Mapped[int]=mapped_column(primary_key=True)  #created id with primary key
    name:Mapped[str] = mapped_column(String) #created name 
    course:Mapped[list["Course"]]=relationship(secondary=student_course,back_populates="student")
    #secondary=student_course table that link to student and courses
    #backpopulates=student links with course and course with student its bidirectional relationship
    #eg: From student table ->students.course will give list of courses in which  student have  enrolled
    #From course table ->Course.student will give list of students who have enrolled for course

class Course(Base):  #models
    __tablename__ = "courses" #tablename

    id:Mapped[int] = mapped_column(primary_key=True) #course id
    coursename:Mapped[str] = mapped_column(String)  #coursename
    student:Mapped[list["Student"]]=relationship(secondary=student_course,back_populates="course")
    #secondary=student_course table that link to student and 
    #From course table ->Course.student will give list of students who have enrolled for course

Base.metadata.create_all(engine) #create table in database

'''s1=Student(name="Ayushi") #entering student name
c1=Course(coursename="python") #entering coursename
c2=Course(coursename="java") #entering coursename

s1.course.extend([c1,c2])
#s1.course is a relationship extend add both the courses in studentlist
session.add(s1) #will addstudent and courses as s1 is link with c1
#When you add c1, SQLAlchemy sees that c1 is linked to s1 → adds s1 also It also adds c2 because it is part of s1.course
session.commit() #saves the data in database'''

s1=Student(name="shruti")
s2=Student(name="sneha")
c1=Course(coursename="MCA")

c1.student.extend([s1,s2])
session.add(c1)
session.commit()