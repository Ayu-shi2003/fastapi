#before_delete= runs just before a record is removed from db checking permssion before deleting something  i.e check
#after_delete = runs after the record is succsessfully deleted i.e confirm 

from sqlalchemy import create_engine,String,Integer,event
#create_engine=connection bet python and database,String & int=datatype,event=attach listeneer to database actions 
from sqlalchemy.orm import declarative_base,sessionmaker,Mapped,mapped_column,Mapper
#declarative_base=base class for all  database models, sessionmaker=creates session used to talk to db,Mapped=for orm columns,mapped_column=define
from sqlalchemy.engine import Connection

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:Ayushi%401234@localhost:5432/mydatabase" #connection path  for database
engine = create_engine(SQLALCHEMY_DATABASE_URL)   #creates engine bridge between python and database 

Session = sessionmaker(bind=engine) #sessionmaker=factory for sessions
session=Session()  #session=used to add,update,delete,commit data 

Base=declarative_base() #all database table will inherit from base class


class Student(Base): #student table model
    __tablename__ = "students3" #tablename in database 
 

    id:Mapped[int] = mapped_column(primary_key=True) #stores unique id
    name:Mapped[str] = mapped_column(String) #stores name 
    age:Mapped[int] = mapped_column(Integer) #stores age

Base.metadata.create_all(engine) #creates table in database 

def before_delete_listener(mapper:Mapper,connection:Connection,target:Student): #mapper=maps python class ->Db table,connection=active db connection,target=student object being deleted
    print("\n [ BEFORE DELETE ] checking student before deletion..") #message before deletion start

    if target.age < 18:  #checks student age 
        raise ValueError("cannot delete a minor student") #stop deletion if age is less than 18
    print(f"[BEFORE DELETE ] Alllowed to delete : {target.name}") #confirm deletion 

#runs after student is deleted
def after_delete_listener(mapper:Mapper,connection:Connection,target:Student):
    print(f"[AFTER DELETE ] student deleted successfully") #shows success message
    print(f"[AFTER DELETE ] deleted student id : {target.id }") #shows id of deleted student

event.listen(Student,"before_delete",before_delete_listener) #attach function to before_delete event
event.listen(Student,"after_delete",after_delete_listener) #attach function to after_delete event

#insert students
student1 = Student(name="Ayushi",age=22)
student2 = Student(name="Riya", age=23)
session.add_all([student1,student2]) #add to session 
session.commit() #save in database 

#delete student  by name
'''student_to_delete= session.query(Student).filter(Student.name == "Ayushi").first() #fetch student name= Ayushi
session.delete(student_to_delete) #marks this student for deletion 
session.commit() #save into database '''

#delete student by age
'''student_delete= session.query(Student).filter(Student.age == 23).first() #fetch student by their age 
session.delete(student_delete)
session.commit()'''

#deleting student with name and age
student_delete= session.query(Student).filter(Student.name =="Riya" and Student.age ==23).first() #fetch student with name and age 
session.delete(student_delete)
session.commit()