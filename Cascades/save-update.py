#save-update=automatically adds or updates child  when u add or update the parent 
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

    children = relationship(
        "Child",
        back_populates="parent",
        cascade="save-update"  # add/update child automatically
    )

class Child(Base):
    __tablename__ = "children"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    parent_id: Mapped[int] = mapped_column(ForeignKey("parents.id"))
    parent = relationship("Parent", back_populates="children")

Base.metadata.create_all(engine)

# Create parent and child
p1 = Parent(name="Parent1")
c1 = Child(name="Child1")
p1.children.append(c1)

session.add(p1)  # only add parent
session.commit()  # child is added automatically