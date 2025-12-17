#flush = sqlalchemy sends changes to database,but does not permanently save them yet
#before_flush = runs just before sqlalchemy sends insert/update/delete to DB , last chance to to edit data
#after_flush = runs after sql is sent  but before commit  ,sql already sent
#this is session level concept as it works on many records together

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
    __tablename__ = "students4"

    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String)
    age:Mapped[int] = mapped_column(Integer)

Base.metadata.create_all(engine)

#whats happening here is before sqlalchemy sends the data to the db,checks and fix student names and after sql is sent,just inform me and this checking is happen automatically without calling function.
#defining a function that will run before the data gets flush into db 
def before_flush_listener(session,flush_context,instances): #session=current session that holds new,updated and delete object,flush_context=internal sqlalchemy function,instances=specific object being flushed 
    print(f"[BEFORE FLUSH ] checking student data") #prints message before sending to db

    for obj in session.new: #loop through all new objects added to session
        if isinstance(obj,Student): #checks that is this object is student
            obj.name = obj.name.title() #fix the student name 
            print(f"[BEFORE FLUSH ] fixed name-> {obj.name}") #show confirmation that the name was corrected

#define function that runs after sql is sent to db
def after_flush_listener(session,flush_context):
    print("[AFTER FLUSH ] sql sent to database ") #just a message that data is being sent to db

event.listen(session,"before_flush",before_flush_listener) #attach ur function to before_flush event,session when you are about to flush,call before_flush_listener
event.listen(session,"after_flush",after_flush_listener)#attach ur function to after_flush event,session,after flushing call after_flush_listener

#insert data in session 
student=Student(name="ayushi parekh",age=23)
session.add(student) #put into session meemory
session.flush()
