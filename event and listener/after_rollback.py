#rollback=cancel everything and go back to previous safe state
#rollback happens when an error occurs,validation fails or else we manually call session.rollback
#after_rollback = runs automatically after a transaction is cancelled
#it runs when commit fails ,exception occurs in simple way something went wrong cleanup and inform.

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
    __tablename__ = "students6"

    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String)
    age:Mapped[int] = mapped_column(Integer)

Base.metadata.create_all(engine)

def after_rollback_listener(session):
    print("\n [AFTER ROLLBACK] Transaction failed! ")
    print("[AFTER ROLLBACK] changes were cancelled")

event.listen(session,"after_rollback",after_rollback_listener)

student = Student(name="Riya", age=19)
session.add(student)

try:
    # Validation: raise error if underage
    if student.age < 18:
        raise ValueError("Student must be at least 18 years old")
    
    session.commit()  # commit will succeed if age >= 18
except Exception as e:
    session.rollback()  # triggers after_rollback listener
    print("Error:", e)
