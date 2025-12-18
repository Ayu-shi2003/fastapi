from sqlalchemy import create_engine,String,Integer,ForeignKey
#create_engine=connects python to database,string & integer= column data types,event=allows u to attach custom functions to db actions.
from sqlalchemy.orm import declarative_base,sessionmaker,Mapped,mapped_column,relationship
from sqlalchemy.ext.hybrid import hybrid_method

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:Ayushi%401234@localhost:5432/mydatabase" #connection path  for database
engine = create_engine(SQLALCHEMY_DATABASE_URL)   #creates engine bridge between python and database 

Session = sessionmaker(bind=engine) #sessionmaker=factory for sessions
session=Session()  #session=used to add,update,delete,commit data 

Base=declarative_base() #all database table will inherit from base class

class Employee(Base): #table model
    __tablename__ = "employees10" #tablename

    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String)
    salary:Mapped[int] = mapped_column(Integer)

    @hybrid_method #works like normal python and also work inside sql query  
    def salary_above(self, amount):#self=current employee object,amount=value passed
        return self.salary > amount #checks employee salary is greater  than amount 

    @salary_above.expression #this is used for sql query 
    def salary_above(cls, amount): #cls=employee table,amount=value passed in query 
        return cls.salary > amount

Base.metadata.create_all(engine) #create table

#create employee objects
e1 = Employee(name="Ayushi", salary=50000)
e2 = Employee(name="Riya", salary=20000)

session.add_all([e1, e2])
session.commit() #saves in db

#use hybrid method in python 
print(e1.salary_above(30000))  # True #checks that 50000>30000
print(e2.salary_above(30000))  # False checks 20000>30000

#hybrid method in sql query 
rich_employees = session.query(Employee).filter(     #seelct employee from employee table 
    Employee.salary_above(30000)  #call hybrid method in sql form give me only those employees having salary>30000
).all()

for e in rich_employees:
    print(e.name)

