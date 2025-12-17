from sqlalchemy import create_engine,String,Integer,event
#create_engine=connects python to database,string & integer= column data types,event=allows u to attach custom functions to db actions.
from sqlalchemy.orm import declarative_base,sessionmaker,Mapped,mapped_column,Mapper
#declarative_base=base class for all sqlalchemy models,sessionmaker=used to interact with db,mapped&mapped_column=new way to define columns,mapper=represents the mapping between python class and db table used in lifecycle 
from sqlalchemy.engine import Connection #connecction=represnets db connection,used in events

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:Ayushi%401234@localhost:5432/mydatabase" #connection path  for database
engine = create_engine(SQLALCHEMY_DATABASE_URL)   #creates engine bridge between python and database 

Session = sessionmaker(bind=engine) #sessionmaker=factory for sessions
session=Session()  #session=used to add,update,delete,commit data 

Base=declarative_base() #all database table will inherit from base class

class Student(Base):
    __tablename__ = "studentseg"

    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String)
    age:Mapped[int] = mapped_column(Integer)

Base.metadata.create_all(engine)

#Insert events :-
#run before new row is inserted
def before_insert_listener(mapper:Mapper,connection:Connection,target:Student): #target=student object about to be inserted
    print(f"[ BEFORE INSERT ] preparing to insert : {target.name}") #prepare to insert 
    target.name = target.name.title() #capitilize the first letter of name
#runs after row is inserted into db
def after_insert_listener(mapper:Mapper,connection:Connection,target:Student):
    print(f"[ AFTER INSERT ] succesffuly inserted : {target.name} with ID: {target.id}") #shows successful message with student name and id.

#update events:-
#runs before updating a row
def before_update_listener(mapper:Mapper,connection:Connection,target:Student):
    print(f"[ BEFORE UPDATE ] updating student : {target.name}") #print updated students name
    if target.age < 18:                                           #put condition where student age should not be less than 18
        raise ValueError("student must be atleast18") #if age is less then that it wont get update and error message will be printed 

#runs after updating the row  
def after_update_listener(mapper:Mapper,connection:Connection,target:Student):
    print(f"[ AFTER UPDATE ] student updated: {target.name}") #prints message of success that student updated with name 

#delete events:-
#runs before deleting the row
def before_delete_listener(mapper:Mapper,connection:Connection,target:Student):
    print(f"[ BEFORE DELETE ] deleting student: {target.name}") #print message of student name
    if target.age < 18:    #checks whther student is below 18
        raise ValueError("cannot delete minor student") #if it is below 18 then that student wont be able to delete

#runs after deletion,confirmation
def after_delete_listener(mapper:Mapper,connection:Connection,target:Student):
    print(f"[ AFTER DELETE ] student deleted: {target.name}") #success message this student got delete with name

#load event:-
#runs when student is fetched from db
def load_listener(target:Student,context):
    print(f"[ load ] student loaded: {target.name}") 

#refresh event:-
#runs when session.refresh(student) is called and fetches latest db data.
def refresh_listener(target:Student,context,attrs):
    print(f"[ REFRESH ] student refreshed: {target.name},Age={target.age}")

#flush event:-
#runs before sql is sent to db
def before_flush_listener(session,flush_context,instances):
    print(f"[ BEFORE FLUSH ] preparing changes for db...")

#runs after sql is sent to db 
def after_flush_listener(session,flush_context):
    print(f"[ AFTER FLUSH ] chnages flushed to db..")

#commit event:-
#just before session commits
def before_commit_listener(session):
    print(f"[ BEFORE COMMIT ] About to commit changes")

#just after commit is successsful
def after_commit_listener(session):
    print(f" [ AFTER COMMIT ] changes committed successfully")

#rollback event:-
#runs after session.rollback(),triggered when ransaction fails or is cancelled
def after_rollback_listener(session):
    print(f" [ AFTER ROLLBACK ] Transaction rolled back ")

#Attach listeners to event:
#connects function to specific event
event.listen(Student,"before_insert",before_insert_listener)
event.listen(Student,"after_insert",after_insert_listener)
event.listen(Student,"before_update",before_update_listener)
event.listen(Student,"after_update",after_update_listener)
event.listen(Student,"before_delete",before_delete_listener)
event.listen(Student,"after_delete",after_delete_listener)
event.listen(Student,"load",load_listener)
event.listen(Student,"refresh",refresh_listener)
event.listen(session,"before_flush",before_flush_listener)
event.listen(session,"after_flush",after_flush_listener)
event.listen(session,"before_commit",before_commit_listener)
event.listen(session,"after_commit",after_commit_listener)
event.listen(session,"after_rollback",after_rollback_listener)

#Insert a student
student1= Student(name="ayushi parekh",age=23)
session.add(student1)
session.commit()

#update student
student1.age=24
session.commit()

#refresh student 
session.refresh(student1) #fetches latest value from db for this student 

#load students 
students=session.query(Student).all() #fetches all students from db 

#delete student
session.delete(student1) #deletes student1 from db
session.commit()

#rollback
student2 = Student( name= "shreya",age=15) #adds student to new session 
session.add(student2)
try:
    if student2.age < 18: #checks validation 
        raise ValueError("student must be atleast 18")
    session.commit() #saves data if no error then nothing happens 
except Exception as e:
    session.rollback() #if error occurs then all cancel chnages will be ssen 
    print("Error:",e)

#insert will trigger:
#before_commit->before_flush->before_insert->sql insert->after insert->after flush->after commit
#[BEFORE COMMIT] → session is about to save changes permanently,[BEFORE FLUSH] → session prepares the SQL statements (INSERT) before sending them to DB.,[BEFORE INSERT] → row-level check for this student → name is formatted to Ayushi Parekh.
#SQL INSERT happens → student is inserted into DB with ID 1,[AFTER INSERT] → confirms student inserted,[AFTER FLUSH] → all SQL statements sent to DB.
#[AFTER COMMIT] → transaction successfully saved permanently.

#update will trigger:
#beforecommit->beforeflush->refresh-> beforeupdate->afterupdate->afterflush->aftercommit->refresh
#[BEFORE COMMIT] → session about to save changes.[BEFORE FLUSH] → session prepares update SQL.[REFRESH] → session refreshes student object from DB (optional, ensures latest DB values).
#[BEFORE UPDATE] → validates update (age ≥ 18).SQL UPDATE happens → age is updated to 24.[AFTER UPDATE] → confirms student updated.
#[AFTER FLUSH] → changes sent to DB.[AFTER COMMIT] → transaction committed successfully.[REFRESH] → object refreshed again, shows latest age=24.

#delete will trigger:-
#beforecommit->beforeflush->beforedelete->sql-afterdelete-afterflush-aftercommit
#[BEFORE COMMIT] → preparing to save deletion.[BEFORE FLUSH] → preparing DELETE SQL.[BEFORE DELETE] → checks: can we delete? Age ≥ 18 → yes, proceed.
#SQL DELETE happens → student removed from DB.[AFTER DELETE] → confirms deletion.[AFTER FLUSH] → changes sent to DB.
#[AFTER COMMIT] → deletion permanently saved.

#insert another student:
#beforecommit-beforeflush-beforeinsert-sql-afterinsert-afterflush-aftercommit