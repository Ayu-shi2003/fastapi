from sqlalchemy import String,ForeignKey,create_engine #string=for text columns,foreignkey=to link two tables,create_engine=creates connection to postgresql
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,relationship,sessionmaker,joinedload,selectinload,subqueryload
#declarativebase=base class for all models,Mappedd=tells sqlalchemy that this data is mapped toDB,mapped_column=creates a column,relationship=creates relationship between tables,sessionmaker=creates session to talk to db
#joinedload=eagerloading option

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

class Base(DeclarativeBase): #all models inherit from base class
    pass

class User(Base): #model class
    __tablename__ = "user1" #table

    id: Mapped[int] = mapped_column(primary_key=True) #id with primary key
    name: Mapped[str] = mapped_column(String)  #name with string

    '''addresses: Mapped[list["Address"]] = relationship(
        "Address",
        back_populates="user",
        lazy="select"   # default lazy loading
    )'''
    #select= one user-> many addresses,addresses load only when accessed

    ''' addresses:Mapped[list["Address"]]=relationship("Address",back_populates="user",lazy="selectin")'''
    #selectin= loads user first then load all addresses  for all users in 1 query

    addresses:Mapped[list["Address"]]=relationship("Address",back_populates="user",lazy="joined")
    #joined user+addresses loaded together using sql join 


class Address(Base): #model class
    __tablename__ = "address1"  #tablename

    id: Mapped[int] = mapped_column(primary_key=True)  #id
    city: Mapped[str] = mapped_column(String) #city
    user_id: Mapped[int] = mapped_column(ForeignKey("user1.id"))
    #foreign key linking address1->user1.id

    user: Mapped["User"] = relationship(
        back_populates="addresses"
    )
    #each address belongs to one user


Base.metadata.create_all(engine)
#create tables in database

u1=User(name="Ayushi") #adding data in usertable
a1=Address(city="jamnagar",user=u1)  #adding address in address tabe
a2=Address(city="Ahemdabad",user=u1) #same adding data in address table

session.add(u1)  #adding u1 will automatically update address as it is link with each other 
session.commit() #saves data into database 

'''user=session.get(User,5) #fetching user from database the user having id=6
print(user.addresses) '''#you are printing addresses the address that belongs to user having id as 6

'''user=session.query(User).all()
for u in user:
        print(u.addresses)'''
#fetch all users and print their addresses

#select=1 query for users + 1 query for  each users address for select query we face problem i.e if we have 100 users then 1 query for user will be generated and 100 for qqueries for address will generated and that is inefficient.
#selectin = 1 query for users + 1 query for all addresses at once . we have advantage for it in just 2 queries everything we will get all the addresess of user will be get.
#so selectin used for 1-many relationship

'''user = session.get(User, 6)
print(user.addresses)
#single query user+address loaded '''

'''user=session.query(User).options(joinedload(User.addresses)).all()
#session.query=tells database to give all rows from user table,options=control how relatiionship are loaded,joinedload(user.addresses)=means load user and their addres stogether with join query,all=execute the query
for u in user:   #loop each user
    print(u.name,u.addresses)
#u.name=print username,u.addresses=user address'''

'''user=session.query(User).options(selectinload(User.addresses)).all()
#seelctinload=1 query will run for user and 2 query for the address belongs to that particular user best for 1-many relationship
for u in user:
    print(u.name,u.addresses)'''

user=session.query(User).options(subqueryload(User.addresses)).all()
for u in user:
    print(u.name,u.addresses)
