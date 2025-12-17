#after_load= this event runs when data is read from the database means fetch/select

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

class Student(Base):
    __tablename__ = "students7"

    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String)
    age:Mapped[int] = mapped_column(Integer)

Base.metadata.create_all(engine)

#this function runs only when a student row is fetched in db
def load_listener(target:Student,mapper:Mapper): #target:student the actual object stored in db
    print("\n [LOAD EVENT ] student loaded from database ") #prints message
    print(f"ID:{target.id},Name:{target.name},Age:{target.age}") #prints message and proves that data came from db.

event.listen(Student,"load",load_listener) #event.listen=connects an event with function,student=attach event to student table,load=eventname,loadlistener=function to run

#insert data
student1=Student(name="Ayushi",age=23)
student2=Student(name="Shreya",age=27)
session.add_all([student1,student2])
session.commit() #saves in db
session.close() #to clears session  cache

session=Session() #new session 
#students= session.query(Student).all()
#student = session.query(Student).filter(Student.name == "Ayushi").first()
students = session.query(Student).filter(Student.age > 20).all()
