#expunge=removes child from session if parents is removed from session

from sqlalchemy import create_engine,String,Integer,ForeignKey
#create_engine=connects python to database,string & integer= column data types,event=allows u to attach custom functions to db actions.
from sqlalchemy.orm import declarative_base,sessionmaker,Mapped,mapped_column,relationship

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:Ayushi%401234@localhost:5432/mydatabase" #connection path  for database
engine = create_engine(SQLALCHEMY_DATABASE_URL)   #creates engine bridge between python and database 

Session = sessionmaker(bind=engine) #sessionmaker=factory for sessions
session=Session()  #session=used to add,update,delete,commit data 

Base=declarative_base() #all database table will inherit from base class

class Parent(Base):
    __tablename__ = "parents"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)

    children = relationship(  #relationship is used to link bet 2 tables 
        "Child",  #child name of class
        back_populates="parent", #parent table has all child objects that linked to parent 
        cascade="all,expunge"  # add/update child automatically
    )

class Child(Base):
    __tablename__ = "children"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    parent_id: Mapped[int] = mapped_column(ForeignKey("parents.id"))
    parent = relationship("Parent", back_populates="children") #child table has a information of parent link to parent 
    #2 way link: from parent->child,from child->get parent

Base.metadata.create_all(engine)

p4 = Parent(name="Parent4")
c4 = Child(name="Child4")
p4.children.append(c4)
session.add(p4)
session.commit()

session.expunge(p4)
print(list(session.identity_map.values()))


