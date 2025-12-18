from sqlalchemy import create_engine,String,Integer,ForeignKey
#create_engine=connects python to database,string & integer= column data types,event=allows u to attach custom functions to db actions.
from sqlalchemy.orm import declarative_base,sessionmaker,Mapped,mapped_column,relationship
from sqlalchemy.ext.hybrid import hybrid_property

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:Ayushi%401234@localhost:5432/mydatabase" #connection path  for database
engine = create_engine(SQLALCHEMY_DATABASE_URL)   #creates engine bridge between python and database 

Session = sessionmaker(bind=engine) #sessionmaker=factory for sessions
session=Session()  #session=used to add,update,delete,commit data 

Base=declarative_base() #all database table will inherit from base class

class User(Base):
    __tablename__ = "users10"

    id:Mapped[int]= mapped_column(primary_key=True)
    first_name:Mapped[str] = mapped_column(String)
    last_name:Mapped[str] = mapped_column(String)

    @hybrid_property
    def full_name(self):
        return self.first_name + " " + self.last_name

    @full_name.expression
    def full_name(cls):
        return cls.first_name + " " + cls.last_name

Base.metadata.create_all(engine)

u1 = User(first_name="Ayushi", last_name="Parekh")
u2 = User(first_name="Riya", last_name="Shah")

session.add_all([u1, u2])
session.commit()

print(u1.full_name)

users = session.query(User).filter(User.full_name == "Ayushi Parekh").all()

