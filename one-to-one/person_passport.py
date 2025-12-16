from sqlalchemy import String, Integer, ForeignKey, create_engine, Table, Column  #imported all sqlalchemy tools needed
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship,sessionmaker




# Database URL
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:Ayushi%401234@localhost:5432/mydatabase" #connection path  for database
engine = create_engine(SQLALCHEMY_DATABASE_URL)  #main connection to talk with database
#create_engine reads our connection url that is pw,host,user,port and return an engine object
#engine is object that knows how to talk with DB driver as it knows how to call database connection.
#basically in easy terms engine means it connects our python code  and postgressql database without engine we cant connect to database

Session = sessionmaker(bind=engine)  #sessionmaker creates a class that makes session object
#Session means create session

session=Session()   #session is the object which is used for insert,update,delete query data 
#main tool to talk to the database 

#engine=connect to database
#Session=blueprint to create session
#session=actual object that talks to db



class Base(DeclarativeBase):  #All tables that we will be creating in database will inherit from base class means starts with this base class due to this it will tell sqlalchemy that these class will become the database table
    pass

#One-to-one relationship:-
class Person(Base): #table model name Person
    __tablename__ = "persons"  #tablename persons

    id:Mapped[int] = mapped_column(primary_key=True)  #created id column for person it is given primary key means unique key
    name:Mapped[str] = mapped_column(String)    #created name column for person
    passport: Mapped["Passport"] = relationship(back_populates="person",uselist=False) #creates 1:1 relationship where uselist=false means one passport for each person and backpopulates="person"means  it connects with passport.personmeans one passport for one person and one person has one passport cant have multiple passport
    #passport in person table gives passport related to that person
    #Mapped[Passport]=taken from model class and backpopulates="person"=taken from passport table is having person field and vice versa for passport table too.

class Passport(Base):  #table model name Passport
    __tablename__ = "passports"   # create tablename passports

    id:Mapped[int] = mapped_column(primary_key=True) #createdd passport id with primary key
    passport_number : Mapped[str] = mapped_column(String) #created passport number 
    person_id : Mapped[int] = mapped_column(ForeignKey("persons.id")) #creates a foreign key to persons.id means it connects that this passport belongs to this particular person so it is connected with persons table id
    person:Mapped["Person"] = relationship(back_populates="passport") #creates 1:1 relationship ,backpopulates=passport means it take this attribute used in person table 
    
    #basicalyy backpopulates its an automatic synchronization for eg when i load person-passport automatically gets sync and same way.
    #person in passport table gets the person who owns the passport

Base.metadata.create_all(engine) #sqlalchemy will create all tables in database it is compulsoryy without this statement the table wont be created in database

#inserting data into database
p=Person(name="Ayushi") #Person=model or class name
pp = Passport(passport_number="IND12345",person=p) #passport=model or class name,person=p means it automatically sets the personsid
session.add_all([p,pp]) #add and save data in database
session.commit() #commit saves them permanently in database

#get passport that belongs to one person
'''person=session.query(Person).first()
print(person.passport.passport_number)

#get person who has passport
passport=session.query(Passport).first()
print(passport.person.name)'''

result = (
    session.query(Person.name, Passport.passport_number)
    .join(Passport, Person.id == Passport.person_id)
    .all()
)
for row in result:
    print(row)
