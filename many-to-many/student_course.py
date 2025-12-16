from sqlalchemy import String,Integer,ForeignKey,create_engine,Table,Column,select #foreign key=creates reference from one table to another
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

#2 students are getting enrolled for one course 
s1=Student(name="shruti") #student1
s2=Student(name="sneha")  #student2
c1=Course(coursename="MCA")  #course

c1.student.extend([s1,s2])
#c1=course object .student=relationship link generated for student course and extend=to add multiple items at once 
session.add(c1) 
#we will add c1 so automaticallyy s1 and s2 will get added as it our linked with each other
session.commit() #saves the data into database


#with select query new modern way 
stmt = select(Student.name, Course.coursename).join(Student.course) #select statemnet start noe we are taking name from student table and coursename from course table and we are joining student_course table
#student,course both are the class name it is used because it internally connect the student_course as we are using secondary filed in our this tables so it gets connection through it 
result = session.execute(stmt).all()
for student_name, course_name in result:
    print(f"Student: {student_name}, Course: {course_name}")



#manual way creating with join old method
result = (
    session.query(Student.name, Course.coursename) #session.query=start a database session and start a select query ,student.name=select students name means from student table take name,Course.coursename=select course table coursename
    .join(student_course, Student.id == student_course.c.Student_id) #after selecting both columns from 2 tables and linking to our middle table using join student table with student_course table ,.c=accesse column of table object ,student_id=column inside student_course 
    #.c is important as it reference to the column of middle table as middle table doest not have model it is table so we used c to access the column from that particular table
    .join(Course, Course.id == student_course.c.course_id) #join course table into student_course table match course id with student_course id 
    .all() #excute the query and fetching all the rows and give return
)

for row in result: #loop through each row returned from database 
    print(row)

#backpopulates:-
#Its a two way connection 
#student.course=a studnet enrolled in many course
#course.student=In one course many students are enrolled
#backpopulates its a sync between both table 
#if we add student automatically in course table updation is seen
#in above example i have given that s1=one studentname im adding and c1=1 courssename im adding now if i will append or extend and wirte s1 then automatically c1 will also get updated beacuse of backpopulate
#backpopulate is a link between 2 tables 

#get all students with their courses
'''students=session.query(Student).all() #take student table
for student in students:  #student=randomvariable name,students=above it is mention that only we need to take for the query
    print(student.name)   #print the name of the student
    for course in student.course:  #by using for loop student.course=current student enrolled in how many courses .course=already mention in our student table we have given backpopulates
        print("enrolled in ",course.coursename)''' #printing the coursename for that particular student

#get all courses with enrolled students
'''course=session.query(Course).all() #select course table 
for c in course:
    print(c.coursename) #print coursename
    for student in c.student: #c.student=student we are having in our course table that is backpopulates we have used 
        print("student:",student.name) #print student name so we will get for this course this student is enrooled'''

#find course of specific student
'''student=session.query(Student).filter_by(name="shruti").first()
for course in student.course:
    print(course.coursename)'''

#find students enrooled in specific course
'''course=session.query(Course).filter_by(coursename="MCA").first()
for student in course.student:
    print(student.name)'''

#count how many courses a student has
student = session.query(Student).filter_by(name="Ayushi").first()
print(len(student.course))

#Count how many students are in a course
course = session.query(Course).filter_by(coursename="MCA").first()
print(len(course.student))



