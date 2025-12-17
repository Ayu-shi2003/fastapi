#commit= saves the data permanently into the db
#before_commit = runs just before data is permanently saved
#after_commit = runs just after data is successfully saved

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
    __tablename__ = "students5"

    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String)
    age:Mapped[int] = mapped_column(Integer)

Base.metadata.create_all(engine)

def before_commit_listener(session):
    print("\n [BEFORE COMMIT ] final check before saving..")

    for obj in session.new:
        if isinstance(obj,Student):
            if obj.age < 18:
                raise ValueError("student must be 18+ to commit ")
            
            obj.name=obj.name.title()
            print(f"[BEFORE COMMIT ] ready to save: {obj.name}")

def after_commit_listener(session):
    print(f"[AFTER COMMIT ] Data succesffuly saved ")

event.listen(session,"before_commit",before_commit_listener)
event.listen(session,"after_commit",after_commit_listener)

student = Student(name="ayushi parekh", age=22)
session.add(student)
session.commit()

