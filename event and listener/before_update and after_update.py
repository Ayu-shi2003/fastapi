#before_update = check & prepare date i.e check
#after_update= confirm and log update i.e confirm

from sqlalchemy import create_engine,String,Integer,event  
#create_engine=connection bet python and database,String & int=datatype,event=attach listeneer to database actions 
from sqlalchemy.orm import declarative_base,sessionmaker,Mapped,mapped_column,Mapper
#declarative_base=base class for all  database models, sessionmaker=creates session used to talk to db,Mapped=for orm columns,mapped_column=defines table columns
from sqlalchemy.engine import Connection

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:Ayushi%401234@localhost:5432/mydatabase" #connection path  for database
engine = create_engine(SQLALCHEMY_DATABASE_URL)   #creates engine bridge between python and database 

Session = sessionmaker(bind=engine) #sessionmaker=factory for sessions
session=Session()  #session=used to add,update,delete,commit data 

Base=declarative_base()  #all database table will inherit from base class

class Student(Base): #student table model
    __tablename__ = "students2"  #tablename in database 
 
    id:Mapped[int]=mapped_column(primary_key=True) #stores unique id for each row
    name:Mapped[str] = mapped_column(String) #stores student name
    age:Mapped[int] = mapped_column(Integer)  #stores student age
    course:Mapped[str] = mapped_column(String) #stores student course 


Base.metadata.create_all(engine)  #creates table in database 

#before_update_listener runs before it updates row in db
def before_update_listener(mapper:Mapper,connection:Connection,target:Student):   #mapper=maps python class ->Db table,connection=active db connection,target=student object being updated
    print("\n[BEFORE UPDATE ] validating update") #message before update happpens
    if target.age < 18:                              #checks updated age
        raise ValueError("Age cannot be less then 18") #stops update if age is invalid & db will not update
    target.name = target.name.title()  #converts name to proper format 

#after_update_listener=runs after update is successful and runs after the db row has been updated 
def after_update_listener(mapper:Mapper,connection:Connection,target:Student): 
    print("\n [AFTER UPDATE ]update completed") #shows confirmation message
    print(f"Student {target.id} updated successfully") #shows student id that has been updated 

event.listen(Student,"before_update",before_update_listener) #attach before_update_listener to student table
event.listen(Student,"after_update",after_update_listener) #attach after_update_listener

#Insert student details
student=Student(name="ayushi",age=22,course="MCA")
s1=Student(name="shreya",age=27,course="MBA")
s2=Student(name="sejal",age=50,course="Mcom")
session.add(student) #added 
session.add_all([s1,s2])
session.commit() #saved in db

#update student age 
'''student.age = 23 #updated age
session.commit() #saved in database

student.course="BCA"
session.commit()'''

students = session.query(Student).filter(Student.age > 25).all() #checks first where age>25
for stud in students: #go through for 
    stud.course="MCA" #and if the age > 25 make update with their course to mca
session.commit() #saves the data in db