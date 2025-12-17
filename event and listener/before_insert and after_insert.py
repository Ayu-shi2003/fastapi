#event is lifecycle for database object,session and connection  where we can attach custom code that can run automatically,specific action happening insert,update,delete,commit
#listener is when the event occurs listener runs automatically
#listener are helpful for logging,validation,auto-updates or custom actions
#before_insert:validate and prepare data ,runs before the data is saved into the databaase
#after_insert:gives confirmation,it runs after the data saved into the database 


from datetime import datetime
from sqlalchemy import Date, create_engine,Column,Integer,String,event,DateTime
#createengine=connects database,event=attach listeners to events like insert,update and delete
from sqlalchemy.orm import declarative_base,sessionmaker,Mapped,mapped_column,Mapper
#declarative_base=base class to create models,sessionmaker=create session to interact with database
from sqlalchemy.engine import Connection


SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:Ayushi%401234@localhost:5432/mydatabase" #connection path  for database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

Session = sessionmaker(bind=engine) 
session=Session()

Base=declarative_base()


'''class User(Base):
    __tablename__ = "user3"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    age: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)'''
class Student(Base):
    __tablename__ = "students2"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    age: Mapped[int] = mapped_column(Integer)
    course: Mapped[str] = mapped_column(String)
    admission_date: Mapped[datetime] = mapped_column(DateTime)



Base.metadata.create_all(engine) #create table in database 

#This function will run before a new user is inserted [listener function]
'''def before_insert_listener(mapper:Mapper,connection:Connection,target:User): #mapper=internal mapper for class,connection=database connection object,target=the actual user object is being inserted(new_user)
    print(f"before inserting:{target.name},age:{target.age}") #shows the name and age before inserting into database
#mapper=maps your python class into database table

#attach listener to event
#before_insert=just before a new row is inserted into the table
event.listen(User,'before_insert',before_insert_listener)
#user=model/table we are attaching to the listener,before_insert=event_type,before_insert_listeenr=function to run when the event occures


#insert a new user
new_user=User(name="Ayushi",age=22)
session.add(new_user)
session.commit()'''

#after_insert this function will run after the user is saved in the database 
'''def after_insert_listener(mapper:Mapper, connection:Connection, target:User):
    print(f"After inserting: {target.name}, age: {target.age}")

event.listen(User, 'after_insert', after_insert_listener)

# Insert a new user
new_user = User(name="Ayushi", age=25)
session.add(new_user)
session.commit()  '''


#use case:college admission form 
#before_insert=validate & prepare data 
#runs before student data is saved 
def before_insert_listener(mapper:Mapper, connection:Connection, target:Student):#mapper=mapper=links your python class(Student) to dataabase table,connection=connection to database table,target=the student object being inserted
    print("\n[BEFORE_INSERT] Validating admission form...")

    # Age validation 
    if target.age < 18:#check if student age is 18 or above  if not it will raiseerror
        raise ValueError("Student must be at least 18 years old")

    # Format name
    target.name = target.name.title() #format name like the first letter should be capital if it is not in capital it will automatically convert into capital
 
    # Auto-fill admission date
    target.admission_date = datetime.now() #automatically sets the date and time 

    print(f"[BEFORE_INSERT] Form prepared for: {target.name}") #this is like checking the admission form before submission 

#after_insert=confirmation after successfull information 
#runs after student is successfully saved 
def after_insert_listener(mapper:Mapper, connection:Connection, target:Student):
    print("\n[AFTER_INSERT] Admission successful!") #shows success message
    print(f"[AFTER_INSERT] Student ID: {target.id}") #prints generated student_d
    print(f"[AFTER_INSERT] Course: {target.course}") #prints coursename
    print(f"[AFTER_INSERT] Admission Date: {target.admission_date}") #prints saved admission date 

# Attach listeners
event.listen(Student, "before_insert", before_insert_listener) #runs before saving in database
event.listen(Student, "after_insert", after_insert_listener) #runs after saving 

#creating student object not yet saved in datbase 
new_student = Student(
    name="ayushi parekh",
    age=22,
    course="MCA"
)

session.add(new_student) #add to table 
session.commit() #saved in database 

new_student2=Student(
    name="shreya parekh",
    age=27,
    course="MBBS"
)
session.add(new_student2) #add to table
session.commit()#saved in database 