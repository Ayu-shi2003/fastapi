#refresh=refresh event runs when SQLAlchemy reloads an already-existing object from the database again.

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
    __tablename__ = "students8"

    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String)
    age:Mapped[int] = mapped_column(Integer)

Base.metadata.create_all(engine)

def refresh_listener(target, context, attrs): #context=extra information abt refresh function
    print("\n[REFRESH EVENT] Student refreshed from database") #prints message
    print(f"ID: {target.id}, Name: {target.name}, Age: {target.age}") 

event.listen(Student, "refresh", refresh_listener) #attach the listneer to event

session = Session() #new db session 
student = Student(name="Ayushi", age=23) #new data
session.add(student)
session.commit() #saves to db

session.execute(            #executes raw sql using sqlalcmy,does not update python object automatically
    Student.__table__.update() #direct sql update on table
    .where(Student.id == student.id) #condition that update on this row
    .values(age=26) #change age colum  to 25
)
session.commit() #saves updated value in db
session.refresh(student)   #go to db and reload the latest data for this studnet object 
