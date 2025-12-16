from sqlalchemy import String,Integer,ForeignKey,create_engine,Table,Column #foreign key=creates reference from one table to another
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,relationship,sessionmaker

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


class User(Base):   #table model user
    __tablename__ = "userss"   #tablename users1

    id:Mapped[int] = mapped_column(primary_key=True) #created id with primary key
    name:Mapped[str] = mapped_column(String) #created username
    addresses: Mapped[list["Address"]] = relationship(back_populates="user",cascade="all, delete-orphan",passive_deletes=True)
    #list is used to addresses list belongs to particular user means 1 user can have multiple address
    #backpopulates user i.e link user field in address links to the user field in Address (two-way connection).
    #cascade=alldelete orphan is deletes linked addresses if user gets delete   
    #passive deletes tells SQLAlchemy that DB handles deletion (ondelete="CASCADE").

class Address(Base):
    __tablename__ = "addressess" #tablename addressess

    id:Mapped[int] = mapped_column(primary_key=True) #created id with primary key
    city:Mapped[str] = mapped_column(String) #created city 
    user_id: Mapped[int] = mapped_column(ForeignKey("userss.id", ondelete="CASCADE"))
    #user_id->links this address to user
    #foreign key= linking to userss.id
    #ondelete=cascade means postgresql will delete automatically all the addresses if user is delelted
    user:Mapped["User"]=relationship(back_populates="addresses")
    #User->connects back to user
    #backpopulates="addresses"->establishes the 2 way connecction i.e user->addresses,addresses->user

Base.metadata.create_all(engine)
#create tables in database

# Create user and addresses insert data in tables
'''u = User(name="Ayushi")
a1 = Address(city="Ahmedabad", user=u)
a2 = Address(city="Rajkot", user=u)'''
#creates a user object u
#creates 2 addresses a1 and a2 which links them to user u

#session.add(u) #add the data in user table and automatically addresses are linked to it alsoo gets the data
#session.commit() #saves the data in database 

#fetch all users with their addresses
'''users = session.query(User).all() #to take data from user table ,all=give all rows from user table
for user in users: #loop through each user in a list 
    print(f"User: {user.name}") #getting name column of current user
    for address in user.addresses: #user.addresses means in user table i have give addresses column that link that 1 user have list of addresses
        print(f"Address: {address.city}")''' #city column of address table 
 
#fetch all addresses with their username
'''addresses = session.query(Address).all() #taking address table
for addr in addresses: #loop through each address
    print(f"City: {addr.city}, User: {addr.user.name}")'''#printing cityname from address table,printing the user_name from address table taking user.name from usrr table

user_to_delete = session.query(User).filter_by(name="Ayushi").first()
if user_to_delete:
    session.delete(user_to_delete)
    session.commit()
    print("User and linked addresses deleted successfully")
else:
    print("User not found")